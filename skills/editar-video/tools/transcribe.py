#!/usr/bin/env python3
"""Transcreve áudio com faster-whisper e grava o JSON de palavras do HyperFrames.

Saída: lista [{id, text, start, end}] em `--out` (padrão: assets/audio/transcript.json).
"""
import argparse
import json
import pathlib
import re
import sys
import time

# Tokens que o Whisper inventa sobre música/silêncio. Nunca viram legenda.
MUSIC_TOKEN = re.compile(r"^[♪♫♬♩�\s\u266a-\u266f\-–—.]+$")


def is_music_token(text: str) -> bool:
    return bool(MUSIC_TOKEN.match(text))


def main() -> int:
    ap = argparse.ArgumentParser(description="Transcrição com timestamps por palavra (faster-whisper).")
    ap.add_argument("audio", help="arquivo de áudio ou vídeo")
    ap.add_argument("-l", "--language", default="pt", help="idioma (padrão: pt)")
    ap.add_argument("-m", "--model", default="small", help="modelo: tiny, base, small, medium, large-v3")
    ap.add_argument("-o", "--out", default=None, help="JSON de saída (padrão: assets/audio/transcript.json)")
    ap.add_argument("--device", default="auto", help="auto, cpu ou cuda")
    ap.add_argument("--compute-type", default="int8", help="int8, float16, float32")
    ap.add_argument("--text-out", default=None, help="também grava o texto corrido neste .txt")
    ap.add_argument("--prompt", default=None, help="dica de vocabulário para o ASR (ex.: nomes próprios, termos do nicho)")
    ap.add_argument("--keep-noise", action="store_true", help="mantém tokens não-palavra (♪, �) em vez de filtrar")
    args = ap.parse_args()

    from faster_whisper import WhisperModel

    t0 = time.time()
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    segments, info = model.transcribe(
        args.audio,
        language=args.language,
        word_timestamps=True,
        vad_filter=True,
        beam_size=5,
        initial_prompt=args.prompt,
    )

    raw, words = 0, []
    for seg in segments:
        for w in seg.words or []:
            raw += 1
            text = w.word.strip()
            if not text:
                continue
            noise = is_music_token(text)
            if noise and not args.keep_noise:
                continue
            words.append(
                {
                    "id": f"w{len(words)}",
                    "text": text,
                    "start": round(float(w.start), 3),
                    "end": round(float(w.end), 3),
                }
            )

    if not words:
        print("Nenhuma palavra transcrita — confira o áudio e o idioma.", file=sys.stderr)
        return 1

    # Gate de qualidade (o mesmo do media-use): transcrição ruim gera legenda sem sentido.
    dropped = raw - len(words)
    ratio = dropped / raw if raw else 0
    short = [w for w in words if w["end"] - w["start"] < 0.05]
    if ratio > 0.20:
        print(
            f"AVISO: {dropped}/{raw} tokens ({ratio:.0%}) eram música/ruído — a transcrição provavelmente "
            "falhou. Repita com modelo maior (medium) ou entregue o texto de referência antes de gerar legenda.",
            file=sys.stderr,
        )
    elif dropped:
        print(f"{dropped} token(s) de música/ruído removido(s).", file=sys.stderr)
    if len(short) > max(3, len(words) * 0.05):
        print(
            f"AVISO: {len(short)} palavra(s) com menos de 0,05 s — timestamps instáveis; "
            "confira a legenda contra o áudio.",
            file=sys.stderr,
        )

    out = pathlib.Path(args.out or "assets/audio/transcript.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(words, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.text_out:
        txt = pathlib.Path(args.text_out)
        txt.parent.mkdir(parents=True, exist_ok=True)
        txt.write_text(" ".join(w["text"] for w in words) + "\n", encoding="utf-8")

    print(
        f"idioma {info.language} · áudio {info.duration:.1f}s · {len(words)} palavras · "
        f"modelo {args.model} · {time.time() - t0:.1f}s"
    )
    print(f"salvo em {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
