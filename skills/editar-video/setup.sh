#!/usr/bin/env bash
# Bootstrap da máquina para a skill editar-video.
# Instala TUDO fora da pasta de projetos, em ~/.olv-studio (ou $OLV_HOME).
set -euo pipefail

OLV_HOME="${OLV_HOME:-$HOME/.olv-studio}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$OLV_HOME/venv"
MODEL="small"
WARM=1

for arg in "$@"; do
  case "$arg" in
    --no-model) WARM=0 ;;
    --model=*) MODEL="${arg#*=}" ;;
    -h|--help)
      cat <<EOF
Uso: ./setup.sh [--no-model] [--model=small|base|medium|large-v3]

  --no-model     não baixa o modelo do Whisper agora (baixa na 1ª transcrição)
  --model=NAME   modelo a pré-baixar (padrão: small)

Destino: \$OLV_HOME (padrão: ~/.olv-studio)
EOF
      exit 0 ;;
  esac
done

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }
warn() { printf '  ! %s\n' "$*"; }
ok() { printf '  ✓ %s\n' "$*"; }

say "1/5 Ambiente"
if command -v node >/dev/null 2>&1; then
  NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
  if [ "$NODE_MAJOR" -ge 22 ]; then ok "node $(node -v)"; else warn "node $(node -v) — a skill pede >= 22"; fi
else
  warn "node não encontrado (instale Node >= 22)"
fi
if command -v ffmpeg >/dev/null 2>&1; then ok "ffmpeg $(ffmpeg -version | head -1 | cut -d' ' -f3)"; else warn "ffmpeg não encontrado"; fi

say "2/5 Pastas fora dos projetos"
mkdir -p "$OLV_HOME"/{bin,tools,models/hf,cache,logs}
ok "$OLV_HOME"
cp "$SKILL_DIR/tools/transcribe.py" "$SKILL_DIR/tools/tts.py" "$OLV_HOME/tools/"
chmod +x "$OLV_HOME/tools/"*.py

say "3/5 Python isolado + faster-whisper + edge-tts"
if [ -x "$VENV/bin/python" ] && "$VENV/bin/python" -c 'import sys; sys.exit(0 if (3,9) <= sys.version_info[:2] <= (3,13) else 1)' 2>/dev/null; then
  ok "venv existente: $("$VENV/bin/python" -V 2>&1)"
else
  rm -rf "$VENV"
  if command -v uv >/dev/null 2>&1; then
    uv venv --python 3.12 "$VENV" >/dev/null
    ok "venv criado com Python 3.12 (uv)"
  else
    PY=""
    for c in python3.12 python3.11 python3.13 python3.10 python3; do
      if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if (3,9) <= sys.version_info[:2] <= (3,13) else 1)' 2>/dev/null; then
        PY="$c"; break
      fi
    done
    if [ -z "$PY" ]; then
      warn "nenhum Python 3.9–3.13 encontrado. Instale o uv (recomendado) ou um Python compatível."
      exit 1
    fi
    "$PY" -m venv "$VENV"
    ok "venv criado com $("$VENV/bin/python" -V 2>&1)"
  fi
fi

if command -v uv >/dev/null 2>&1; then
  uv pip install --python "$VENV/bin/python" --quiet --upgrade faster-whisper edge-tts "av<16"
else
  "$VENV/bin/python" -m pip install --quiet --upgrade pip >/dev/null 2>&1 || true
  "$VENV/bin/python" -m pip install --quiet --upgrade faster-whisper edge-tts "av<16"
fi
ok "faster-whisper $(HF_HOME="$OLV_HOME/models/hf" "$VENV/bin/python" -c 'import importlib.metadata as m; print(m.version("faster-whisper"))')"
ok "edge-tts $(HF_HOME="$OLV_HOME/models/hf" "$VENV/bin/python" -c 'import importlib.metadata as m; print(m.version("edge-tts"))')"

say "4/5 Atalhos em $OLV_HOME/bin"
write_wrapper() {
  local name="$1" script="$2"
  cat > "$OLV_HOME/bin/$name" <<EOF
#!/usr/bin/env bash
set -euo pipefail
OLV_HOME="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")/.." && pwd)"
export HF_HOME="\${HF_HOME:-\$OLV_HOME/models/hf}"
export XDG_CACHE_HOME="\${XDG_CACHE_HOME:-\$OLV_HOME/cache}"
exec "\$OLV_HOME/venv/bin/python" "\$OLV_HOME/tools/$script" "\$@"
EOF
  chmod +x "$OLV_HOME/bin/$name"
}
write_wrapper olv-asr transcribe.py
write_wrapper olv-tts tts.py
cat > "$OLV_HOME/bin/olv-doctor" <<EOF
#!/usr/bin/env bash
set -euo pipefail
OLV_HOME="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")/.." && pwd)"
echo "OLV_HOME  \$OLV_HOME"
echo "node      \$(node -v 2>/dev/null || echo 'não encontrado')"
echo "ffmpeg    \$(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f3 || echo 'não encontrado')"
echo "python    \$("\$OLV_HOME/venv/bin/python" -V 2>&1)"
HF_HOME="\$OLV_HOME/models/hf" "\$OLV_HOME/venv/bin/python" -c 'import importlib.metadata as m; print("whisper   faster-whisper", m.version("faster-whisper")); print("tts       edge-tts", m.version("edge-tts"))' 2>/dev/null || echo "pacotes   não instalados"
echo "modelos   \$(du -sh "\$OLV_HOME/models" 2>/dev/null | cut -f1)"
echo "cache     \$(du -sh "\$OLV_HOME/cache" 2>/dev/null | cut -f1)"
EOF
chmod +x "$OLV_HOME/bin/olv-doctor"
ok "olv-asr, olv-tts, olv-doctor"

say "5/5 Modelo do Whisper"
if [ "$WARM" = "1" ]; then
  printf '  baixando/validando "%s" em %s (só na primeira vez)\n' "$MODEL" "$OLV_HOME/models/hf"
  if HF_HOME="$OLV_HOME/models/hf" XDG_CACHE_HOME="$OLV_HOME/cache" "$VENV/bin/python" - "$MODEL" <<'PY'
import sys
from faster_whisper import WhisperModel
WhisperModel(sys.argv[1], device="auto", compute_type="int8")
PY
  then ok "modelo $MODEL pronto"; else warn "não deu para baixar o modelo agora; ele baixa na 1ª transcrição"; fi
else
  warn "modelo não baixado (--no-model)"
fi

say "Pronto"
cat <<EOF
  Ferramentas da máquina:  $OLV_HOME
  Transcrição:             $OLV_HOME/bin/olv-asr audio.wav -l pt -m small
  Narração:                $OLV_HOME/bin/olv-tts "texto" -v pt-BR-FranciscaNeural -o voz.mp3
  Diagnóstico:             $OLV_HOME/bin/olv-doctor

  Projetos continuam limpos: nada disso é gravado na pasta do vídeo.
  Se $OLV_HOME/bin não estiver no PATH:
    echo 'export PATH="\$HOME/.olv-studio/bin:\$PATH"' >> ~/.zshrc
EOF
