#!/usr/bin/env bash
# Verifica as receitas de tela sem depender de projeto real:
# monta um filme temporário com as 6 cenas e roda o lint do HyperFrames.
#   bash tests/run.sh          # lint (rápido, sem navegador)
#   CHECK=1 bash tests/run.sh  # também roda o check completo (precisa de Chrome)
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RECEITAS="$RAIZ/skills/editar-video/receitas"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "→ projeto temporário em $TMP"
( cd "$TMP" && npx --yes hyperframes@0.9.40 init filme --non-interactive --resolution portrait >/dev/null )

mkdir -p "$TMP/filme/compositions"
cp "$RECEITAS"/*.html "$TMP/filme/compositions/"

python3 - "$TMP/filme/index.html" "$TMP/filme/compositions" <<'PY'
import pathlib, sys
index, comps = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
nomes = sorted(p.stem for p in comps.glob("*.html"))
durs = {"pergunta": 4.5, "numero": 5, "lista": 5.5, "produto": 5, "editorial": 4.5, "cta": 4}
t, hosts = 0.0, []
for n in nomes:
    d = durs.get(n, 5)
    hosts.append(
        f'    <div id="{n}" data-composition-id="{n}" data-composition-src="compositions/{n}.html"\n'
        f'         data-start="{t}" data-duration="{d}" data-track-index="1"\n'
        f'         data-width="1080" data-height="1920"></div>'
    )
    t += d
index.write_text(f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0b0b12; }}
      #root {{ position:relative; width:100%; height:100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{t}"
         data-width="1080" data-height="1920">
{chr(10).join(hosts)}
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused:true }});</script>
  </body>
</html>
''')
print(f"→ {len(nomes)} receitas montadas · {t:g}s")
PY

cd "$TMP/filme"
npx --yes hyperframes@0.9.40 lint
if [ "${CHECK:-0}" = "1" ]; then
  npx --yes hyperframes@0.9.40 check
fi
echo "✓ receitas ok"
