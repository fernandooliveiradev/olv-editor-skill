#!/usr/bin/env python3
"""Gera narração com edge-tts (vozes neurais da Microsoft) e timestamps por palavra.

Saída: MP3 em `--out` e, se pedido, JSON de palavras [{id, text, start, end}] em `--words-out`.
As palavras vêm dos eventos WordBoundary da própria síntese — não precisa transcrever de novo.
"""
import argparse
import asyncio
import json
import pathlib
import sys

import edge_tts

DEFAULT_VOICE = "pt-BR-FranciscaNeural"


async def list_voices(prefix: str) -> None:
    voices = await edge_tts.list_voices()
    for v in sorted(voices, key=lambda x: x["ShortName"]):
        if v["ShortName"].lower().startswith(prefix.lower()):
            print(f'{v["ShortName"]:34} {v.get("Gender", ""):7} {v.get("Locale", "")}')


async def synth(text: str, voice: str, rate: str, pitch: str, volume: str, media: pathlib.Path, words_out):
    kwargs = dict(rate=rate, pitch=pitch, volume=volume)
    try:
        communicate = edge_tts.Communicate(text, voice, boundary="WordBoundary", **kwargs)
    except TypeError:  # edge-tts antigo (< 7): não expõe o parâmetro boundary
        communicate = edge_tts.Communicate(text, voice, **kwargs)
    words = []
    media.parent.mkdir(parents=True, exist_ok=True)
    with media.open("wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start = chunk["offset"] / 10_000_000
                dur = chunk["duration"] / 10_000_000
                words.append(
                    {
                        "id": f"w{len(words)}",
                        "text": chunk["text"],
                        "start": round(start, 3),
                        "end": round(start + dur, 3),
                    }
                )
    if words_out:
        out = pathlib.Path(words_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(words, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return words


def main() -> int:
    ap = argparse.ArgumentParser(description="Narração com edge-tts + palavras cronometradas.")
    ap.add_argument("text", nargs="?", help="texto a falar (ou use --text-file)")
    ap.add_argument("--text-file", help="arquivo .txt com o texto")
    ap.add_argument("-v", "--voice", default=DEFAULT_VOICE, help=f"voz (padrão: {DEFAULT_VOICE})")
    ap.add_argument("-o", "--out", default="assets/audio/narracao.mp3", help="MP3 de saída")
    ap.add_argument("--words-out", default=None, help="JSON de palavras (padrão: ao lado do MP3)")
    ap.add_argument("--rate", default="+0%", help='velocidade, ex.: "+8%%" ou "-5%%"')
    ap.add_argument("--pitch", default="+0Hz", help='tom, ex.: "-10Hz"')
    ap.add_argument("--volume", default="+0%", help='volume, ex.: "+5%%"')
    ap.add_argument("--list", action="store_true", help="lista vozes (filtra por --lang-prefix)")
    ap.add_argument("--lang-prefix", default="pt-BR", help="prefixo do idioma para --list")
    args = ap.parse_args()

    if args.list:
        asyncio.run(list_voices(args.lang_prefix))
        return 0

    text = args.text
    if args.text_file:
        text = pathlib.Path(args.text_file).read_text(encoding="utf-8")
    if not text or not text.strip():
        print("Passe o texto (argumento ou --text-file).", file=sys.stderr)
        return 2

    media = pathlib.Path(args.out)
    words_out = args.words_out or str(media.with_suffix(".words.json"))
    words = asyncio.run(
        synth(text.strip(), args.voice, args.rate, args.pitch, args.volume, media, words_out)
    )
    dur = words[-1]["end"] if words else 0
    print(f"{len(words)} palavras · {dur:.1f}s · voz {args.voice}")
    print(f"áudio em {media}")
    print(f"palavras em {words_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
