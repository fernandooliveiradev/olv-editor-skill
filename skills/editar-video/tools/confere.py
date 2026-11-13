#!/usr/bin/env python3
"""Confere o áudio do vídeo final contra o roteiro aprovado, palavra por palavra.

É a verificação que quase ninguém faz: depois do render, transcreve o MP4 e compara com
o texto que o cliente aprovou. Pega o que o olho não vê — TTS que comeu uma palavra,
corte que engoliu meia frase, áudio que sumiu no meio, take errado.

Uso:
  olv-confere video.mp4 --roteiro roteiro.txt
  olv-confere video.mp4 --roteiro roteiro.txt --max-erro 5 --json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import unicodedata
from difflib import SequenceMatcher

UNIDADES = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove",
            "dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete",
            "dezoito", "dezenove"]
DEZENAS = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
CENTENAS = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos",
            "setecentos", "oitocentos", "novecentos"]


def _ate_999(n: int) -> str:
    if n == 0:
        return ""
    if n == 100:
        return "cem"
    partes = []
    c, resto = divmod(n, 100)
    if c:
        partes.append(CENTENAS[c])
    if resto:
        if resto < 20:
            partes.append(UNIDADES[resto])
        else:
            d, u = divmod(resto, 10)
            partes.append(DEZENAS[d] + (" e " + UNIDADES[u] if u else ""))
    return " e ".join(partes)


def numero_para_palavras(txt: str) -> str:
    """Converte 5, 68, 4.200, 3,5 e 30% para como o TTS fala."""
    txt = txt.strip()
    if "," in txt and re.fullmatch(r"\d{1,3}(\.\d{3})*,\d+", txt):
        inteiro, dec = txt.split(",")
        return f"{numero_para_palavras(inteiro)} vírgula {' '.join(UNIDADES[int(d)] for d in dec)}"
    txt = txt.replace(".", "")
    if not txt.isdigit():
        return txt
    n = int(txt)
    if n < 1000:
        return _ate_999(n) or "zero"
    milhares, resto = divmod(n, 1000)
    prefixo = "mil" if milhares == 1 else f"{_ate_999(milhares)} mil"
    return prefixo + (" e " + _ate_999(resto) if resto else "")


def normalizar(texto: str) -> list[str]:
    t = unicodedata.normalize("NFC", texto).lower()
    t = t.replace("%", " por cento ").replace("r$", " ").replace("$", " ")
    t = re.sub(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?", lambda m: numero_para_palavras(m.group(0)), t)
    t = re.sub(r"[^\wà-ÿ\s]", " ", t, flags=re.UNICODE)
    t = re.sub(r"_", " ", t)
    return re.sub(r"\s+", " ", t).strip().split()


def transcrever(caminho: pathlib.Path, modelo: str, idioma: str) -> list[dict]:
    from faster_whisper import WhisperModel

    m = WhisperModel(modelo, device="auto", compute_type="int8")
    segmentos, _ = m.transcribe(str(caminho), language=idioma, word_timestamps=True,
                                vad_filter=True, beam_size=5)
    palavras = []
    for seg in segmentos:
        for w in seg.words or []:
            txt = w.word.strip()
            if txt:
                palavras.append({"text": txt, "start": float(w.start), "end": float(w.end)})
    return palavras


def fmt(t: float) -> str:
    return f"{int(t // 60):d}:{t % 60:04.1f}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Confere o áudio do vídeo contra o roteiro aprovado.")
    ap.add_argument("video", help="MP4 (ou o áudio) já renderizado")
    ap.add_argument("--roteiro", required=True, help="arquivo .txt com o texto aprovado")
    ap.add_argument("--modelo", default="small", help="modelo do Whisper (padrão: small)")
    ap.add_argument("--idioma", default="pt")
    ap.add_argument("--max-erro", type=float, default=5.0, help="%% máximo de divergência (padrão: 5)")
    ap.add_argument("--estrito", action="store_true", help="falha em qualquer divergência")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    roteiro = pathlib.Path(args.roteiro).read_text(encoding="utf-8")
    ref = normalizar(roteiro)
    if not ref:
        print("roteiro vazio", file=sys.stderr)
        return 2

    saida = transcrever(pathlib.Path(args.video), args.modelo, args.idioma)
    hip = normalizar(" ".join(p["text"] for p in saida))
    if not hip:
        print("nenhuma fala detectada no vídeo — áudio mudo ou fora do idioma", file=sys.stderr)
        return 1

    sm = SequenceMatcher(a=ref, b=hip, autojunk=False)
    trocas, faltando, sobrando = [], [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        trecho_ref = " ".join(ref[i1:i2])
        trecho_hip = " ".join(hip[j1:j2])
        if tag == "replace":
            trocas.append({"roteiro": trecho_ref, "audio": trecho_hip})
        elif tag == "delete":
            faltando.append(trecho_ref)
        else:
            sobrando.append(trecho_hip)

    erros = len(trocas) + sum(len(f.split()) for f in faltando) + sum(len(s.split()) for s in sobrando)
    wer = 100.0 * erros / len(ref)
    ok = wer <= args.max_erro

    if args.json:
        print(json.dumps({"ok": ok, "palavras_roteiro": len(ref), "palavras_audio": len(hip),
                          "divergencia_pct": round(wer, 2), "trocas": trocas,
                          "faltando": faltando, "sobrando": sobrando}, ensure_ascii=False, indent=1))
        return 0 if ok else 1

    print(f"roteiro: {len(ref)} palavras · áudio: {len(hip)} palavras · divergência: {wer:.1f}% "
          f"(limite {args.max_erro:.0f}%)")
    for t in trocas[:12]:
        print(f"  ≠  roteiro \"{t['roteiro']}\"  →  áudio \"{t['audio']}\"")
    for f in faltando[:12]:
        print(f"  −  faltou no áudio: \"{f}\"")
    for s in sobrando[:12]:
        print(f"  +  não está no roteiro: \"{s}\"")
    if len(trocas) + len(faltando) + len(sobrando) > 12:
        print("  … (lista truncada; use --json para ver tudo)")
    if args.estrito and erros:
        ok = False
    if ok and erros:
        print(f"⚠ {len(trocas) + len(faltando) + len(sobrando)} divergência(s) abaixo do limite — leia a lista: "
              "pode ser o ASR ouvindo errado, ou o áudio errado de verdade")
    print("✓ áudio confere com o roteiro" if ok else "✗ áudio diverge do roteiro — corrija antes de entregar")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
