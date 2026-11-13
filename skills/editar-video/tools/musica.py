#!/usr/bin/env python3
"""Biblioteca de trilhas do estúdio: indexa, mede e escolhe música por características.

O agente não "escuta" como uma pessoa: ele mede (bpm, duração, loudness, faixa dinâmica),
lê o nome e as tags que você anotar, e escolhe por critério. Se o modelo tiver áudio, use
`amostra` para ouvir um trecho.

Comandos:
  sync    copia uma pasta (ou baixa a pasta do Drive com gdown) para ~/.olv-studio/musicas
  index   mede cada faixa e grava musica.json (cache por data de modificação)
  listar  filtra por bpm, duração, loudness, faixa dinâmica e texto
  usar    extrai o áudio, copia para o projeto e imprime o trecho de HTML + crédito
  amostra extrai um trecho curto para escutar
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

MIDIA = {".mp4", ".m4a", ".mp3", ".wav", ".aac", ".flac", ".ogg", ".opus", ".mov"}
AUDIO = {".m4a", ".mp3", ".wav", ".aac", ".flac", ".ogg", ".opus"}


def home() -> pathlib.Path:
    return pathlib.Path(os.environ.get("OLV_HOME", pathlib.Path.home() / ".olv-studio"))


def lib() -> pathlib.Path:
    return pathlib.Path(os.environ.get("OLV_MUSICAS", home() / "musicas"))


def indice() -> pathlib.Path:
    return lib() / "musica.json"


def rodar(cmd: list[str], **kw) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw).stdout


def titulo(p: pathlib.Path) -> str:
    return re.sub(r"[_]+", " ", p.stem).strip()


def duracao(p: pathlib.Path) -> float:
    return float(rodar(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)]).strip())


def loudness(p: pathlib.Path) -> dict:
    saida = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(p),
         "-af", "loudnorm=print_format=json", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", saida, re.S)
    if not m:
        return {}
    d = json.loads(m.group(0))
    return {"lufs": float(d["input_i"]), "lra": float(d["input_lra"]), "tp": float(d["input_tp"])}


def bpm(p: pathlib.Path) -> float | None:
    """Usa o HyperFrames para detectar o andamento; sem ele, segue sem bpm."""
    for base in (["hyperframes"], ["npx", "--yes", "hyperframes"]):
        try:
            out = rodar(base + ["beats", str(p), "--json"])
            return float(json.loads(out)["bpm"])
        except (FileNotFoundError, subprocess.CalledProcessError, KeyError, ValueError, json.JSONDecodeError):
            continue
    return None


def extrair_audio(origem: pathlib.Path, destino: pathlib.Path) -> pathlib.Path:
    """Extrai só o áudio (cópia do codec, sem re-encode) de um mp4/mov."""
    rodar(["ffmpeg", "-v", "error", "-y", "-i", str(origem), "-vn", "-c:a", "copy", str(destino)])
    return destino


def medir(p: pathlib.Path) -> dict:
    audio = p
    if p.suffix.lower() in {".mp4", ".mov"}:
        extraido = p.with_suffix(".m4a")
        if not extraido.exists() or extraido.stat().st_mtime < p.stat().st_mtime:
            extrair_audio(p, extraido)
        audio = extraido
    d = {"arquivo": p.name, "audio": audio.name, "titulo": titulo(p), "duracao": round(duracao(audio), 2)}
    d.update({k: round(v, 2) for k, v in loudness(audio).items()})
    b = bpm(audio)
    if b:
        d["bpm"] = round(b, 1)
    return d


def gravar(idx: dict) -> None:
    indice().write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")


def cmd_sync(args) -> int:
    origem = pathlib.Path(args.de).expanduser()
    lib().mkdir(parents=True, exist_ok=True)
    if str(origem).startswith("http"):
        print("Para a pasta do Drive, use o gdown (uma vez):")
        print(f'  uvx gdown --folder "{origem}" -O "{lib()}"')
        print("Depois: olv-musica index")
        return 0
    if not origem.is_dir():
        print(f"pasta não encontrada: {origem}", file=sys.stderr)
        return 2
    n = 0
    originais = {f.stem for f in origem.rglob("*") if f.is_file() and f.suffix.lower() in MIDIA - AUDIO}
    for f in sorted(origem.rglob("*")):
        if f.is_file() and f.suffix.lower() in MIDIA:
            if f.suffix.lower() in AUDIO and f.stem in originais:
                continue  # áudio extraído de um vídeo: o original já cobre
            destino = lib() / f.name
            if not destino.exists() or destino.stat().st_size != f.stat().st_size:
                shutil.copy2(f, destino)
                n += 1
    print(f"{n} arquivo(s) sincronizado(s) em {lib()}")
    return 0


def cmd_index(args) -> int:
    lib().mkdir(parents=True, exist_ok=True)
    idx = {}
    if indice().exists() and not args.forcar:
        idx = json.loads(indice().read_text())
    todos = [f for f in sorted(lib().iterdir())
             if f.is_file() and f.suffix.lower() in MIDIA]
    originais = {f.stem for f in todos if f.suffix.lower() in MIDIA - AUDIO}
    arquivos = [f for f in todos
                if not (f.suffix.lower() in AUDIO and f.stem in originais)]
    pendentes = []
    for f in arquivos:
        reg = idx.get(f.name)
        if reg and reg.get("_mtime") == f.stat().st_mtime:
            continue
        pendentes.append(f)
    print(f"{len(arquivos)} faixa(s) · {len(pendentes)} para medir", flush=True)

    def trabalho(f):
        try:
            reg = medir(f)
            reg["_mtime"] = f.stat().st_mtime
            return f.name, reg
        except Exception as e:  # noqa: BLE001 — uma faixa quebrada não derruba o índice
            print(f"  ! {f.name}: {e}", file=sys.stderr)
            return f.name, None

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for i, (nome, reg) in enumerate(pool.map(trabalho, pendentes), 1):
            if reg:
                idx[nome] = reg
            if i % 10 == 0 or i == len(pendentes):
                gravar(idx)
                print(f"  {i}/{len(pendentes)}", flush=True)
    gravar(idx)
    print(f"índice em {indice()}")
    return 0


def carregar() -> list[dict]:
    if not indice().exists():
        print("índice vazio — rode: olv-musica index", file=sys.stderr)
        sys.exit(2)
    return list(json.loads(indice().read_text()).values())


def intervalo(txt: str | None, campo: str) -> tuple[float, float] | None:
    if not txt:
        return None
    m = re.fullmatch(r"\s*(-?\d+(?:\.\d+)?)\s*(?:-\s*(-?\d+(?:\.\d+)?))?\s*", txt)
    if not m:
        print(f"--{campo} espera N ou N-M (ex.: 85-105)", file=sys.stderr)
        sys.exit(2)
    a = float(m.group(1))
    b = float(m.group(2)) if m.group(2) else a
    return (min(a, b), max(a, b))


def dentro(v, r) -> bool:
    return r is None or (v is not None and r[0] <= v <= r[1])


def cmd_listar(args) -> int:
    faixas = carregar()
    tags = {}
    extra = lib() / "musica.tags.json"
    if extra.exists():
        tags = json.loads(extra.read_text())
    fbpm, fdur = intervalo(args.bpm, "bpm"), intervalo(args.dur, "dur")
    flufs, flra = intervalo(args.lufs, "lufs"), intervalo(args.lra, "lra")
    achados = []
    for f in faixas:
        if not dentro(f.get("bpm"), fbpm):
            continue
        if not dentro(f.get("duracao"), fdur):
            continue
        if not dentro(f.get("lufs"), flufs):
            continue
        if not dentro(f.get("lra"), flra):
            continue
        if args.busca:
            alvo = " ".join([f.get("titulo", ""), " ".join(tags.get(f["arquivo"], {}).get("tags", []))]).lower()
            if args.busca.lower() not in alvo:
                continue
        achados.append((f, tags.get(f["arquivo"], {})))
    if args.json:
        print(json.dumps([dict(f, tags=t.get("tags", [])) for f, t in achados], ensure_ascii=False, indent=1))
        return 0
    if not achados:
        print("nenhuma faixa nesse filtro")
        return 0
    print(f"{'arquivo':46} {'bpm':>6} {'dur':>7} {'LUFS':>7} {'LRA':>5}  tags")
    for f, t in sorted(achados, key=lambda x: (x[0].get("bpm") or 0)):
        print(f"{f['arquivo'][:46]:46} {f.get('bpm', 0):6.1f} {f.get('duracao', 0):7.1f} "
              f"{f.get('lufs', 0):7.1f} {f.get('lra', 0):5.1f}  {', '.join(t.get('tags', []))}")
    return 0


def achar(nome: str) -> dict:
    faixas = carregar()
    exatos = [f for f in faixas if nome in (f["arquivo"], f.get("audio"), f["titulo"])]
    if len(exatos) == 1:
        return exatos[0]
    parciais = [f for f in faixas if nome.lower() in f["titulo"].lower()]
    if len(parciais) == 1:
        return parciais[0]
    if not parciais:
        print(f"nenhuma faixa para: {nome}", file=sys.stderr)
    else:
        print("ambíguo — candidatos:", file=sys.stderr)
        for f in parciais[:15]:
            print(f"  {f['arquivo']}  ({f.get('bpm')} bpm)", file=sys.stderr)
    sys.exit(2)


def duracao_do_filme(projeto: pathlib.Path) -> float | None:
    """Lê o data-duration da raiz do index.html, se existir."""
    index = projeto / "index.html"
    if not index.exists():
        return None
    m = re.search(r'data-composition-id="main"[^>]*data-duration="([\d.]+)"', index.read_text(encoding="utf-8"))
    if not m:
        m = re.search(r'data-duration="([\d.]+)"[^>]*data-composition-id="main"', index.read_text(encoding="utf-8"))
    return float(m.group(1)) if m else None


def cmd_usar(args) -> int:
    f = achar(args.faixa)
    origem = lib() / f.get("audio", f["arquivo"])
    if not origem.exists():
        origem = lib() / f["arquivo"]
        if origem.suffix.lower() in {".mp4", ".mov"}:
            origem = extrair_audio(origem, origem.with_suffix(".m4a"))
    projeto = pathlib.Path(args.projeto).expanduser()
    destino_dir = projeto / "assets" / "audio"
    destino_dir.mkdir(parents=True, exist_ok=True)
    nome = args.como or re.sub(r"[^a-z0-9]+", "-", f["titulo"].lower()).strip("-")
    destino = destino_dir / f"{nome}.m4a"
    shutil.copy2(origem, destino)
    dur = args.dur or duracao_do_filme(projeto) or f.get("duracao") or duracao(destino)
    snippet = (f'<audio id="trilha" class="clip" src="assets/audio/{destino.name}"\n'
               f'       data-start="0" data-duration="{dur}" data-volume="{args.volume}"\n'
               f'       data-fade-in="0.6" data-fade-out="1.2"></audio>')
    credito = f"- Trilha: {f['titulo']} ({f['arquivo']}) · {f.get('bpm', '?')} bpm · biblioteca do estúdio"
    creditos = projeto / "CREDITOS.md"
    texto = creditos.read_text(encoding="utf-8") if creditos.exists() else "# Créditos\n\n"
    if credito not in texto:
        creditos.write_text(texto + credito + "\n", encoding="utf-8")
    print(f"trilha: {f['titulo']} · {f.get('bpm', '?')} bpm · {dur}s · {f.get('lufs', '?')} LUFS")
    print(f"copiada para {destino}")
    print(f"crédito em {creditos}")
    print("\nno index.html (dentro do root):")
    print(snippet)
    print("\nlembrete: música entra baixa sob a voz; a mixagem final leva o filme a -14 LUFS.")
    return 0


def cmd_amostra(args) -> int:
    f = achar(args.faixa)
    origem = lib() / f.get("audio", f["arquivo"])
    if not origem.exists():
        origem = lib() / f["arquivo"]
    destino = pathlib.Path(args.saida or "/tmp/olv-trilha-amostra.m4a")
    rodar(["ffmpeg", "-v", "error", "-y", "-ss", str(args.de), "-t", str(args.seg),
           "-i", str(origem), "-vn", str(destino)])
    print(f"amostra de {args.seg}s ({args.de}s dianteiros): {destino}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Biblioteca de trilhas do estúdio.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sync", help="copia pasta local (ou mostra o comando do Drive)")
    s.add_argument("--de", required=True, help="pasta local ou URL da pasta")
    s.set_defaults(func=cmd_sync)

    s = sub.add_parser("index", help="mede as faixas e grava musica.json")
    s.add_argument("--jobs", type=int, default=4)
    s.add_argument("--forcar", action="store_true")
    s.set_defaults(func=cmd_index)

    s = sub.add_parser("listar", help="filtra as faixas")
    s.add_argument("--bpm", help="ex.: 85-105")
    s.add_argument("--dur", help="duração em segundos, ex.: 30-120")
    s.add_argument("--lufs", help="ex.: -16--10")
    s.add_argument("--lra", help="faixa dinâmica, ex.: 5-12")
    s.add_argument("--busca", help="texto no título ou nas tags")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_listar)

    s = sub.add_parser("usar", help="copia a trilha para o projeto e imprime o HTML")
    s.add_argument("faixa")
    s.add_argument("--projeto", required=True)
    s.add_argument("--volume", default="0.15")
    s.add_argument("--dur", type=float, help="duração do clip no filme (padrão: a do filme)")
    s.add_argument("--como", help="nome do arquivo no projeto")
    s.set_defaults(func=cmd_usar)

    s = sub.add_parser("amostra", help="extrai um trecho para escutar")
    s.add_argument("faixa")
    s.add_argument("--de", type=float, default=0)
    s.add_argument("--seg", type=float, default=15)
    s.add_argument("--saida")
    s.set_defaults(func=cmd_amostra)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
