# OLV Studio — a skill de vídeo para agentes de IA

Um roteiro e um áudio viram um vídeo pronto. **OLV Studio** é uma skill que qualquer
agente de IA (OpenCode, Claude Code, Cursor…) usa para produzir vídeos de social com
padrão de estúdio: motion graphics com movimento de verdade, legenda palavra por palavra
e entrega no formato do Reels, do Stories ou do Short.

## O que você recebe

- **Vídeo 9:16 renderizado (MP4 1080×1920)** — cenas em motion graphics sincronizadas
  frame a frame com a fala, nunca tela parada.
- **Legenda karaokê** — palavra ativa destacada no ritmo da voz (transcrição com
  timestamps por palavra).
- **Voz de IA em pt-BR** ou a sua narração tratada (ruído, volume, cortes no silêncio).
- **Estrutura pronta para publicar** — gancho, chamada única e checklist das regras
  atuais do Instagram e do YouTube (templates 2026/2027).
- **Instalação limpa** — tudo se instala uma vez, fora da pasta do projeto, em
  `~/.olv-studio`. Seus projetos nunca misturam dependência com entrega.

## Como funciona

```
seu texto + áudio (ou voz de IA)
        │
        ▼
 1  briefing — formato, objetivo, dor, prova e chamada (uma rodada de perguntas)
 2  roteiro aprovado por você — bloco a bloco, no template do formato
 3  produção — cena por cena em HTML + GSAP (HyperFrames)
 4  verificação — lint, contraste e snapshot frame a frame
 5  entrega — MP4 mixado (−14 LUFS) + plano de pós-publicação
```

## Instalação (3 passos)

```bash
# 1) A skill
git clone https://github.com/fernandooliveiradev/olv-editor-skill
cp -r olv-editor-skill/skills/editar-video ~/.config/opencode/skills/
#   (outro harness: copie para a pasta de skills dele — Claude Code usa .claude/skills/,
#    Cursor e afins: anexe SKILL.md + motion-style.md + templates-gravacao.md)

# 2) O motor de render (HyperFrames)
npx hyperframes skills

# 3) O estúdio: transcrição, voz de IA e modelos — fora dos projetos
bash skills/editar-video/setup.sh
```

## Uso

Peça o vídeo em linguagem natural:

> “Faz um Reels de 30 s sobre IA organizando as perguntas do dia a dia do negócio.
>  CTA é chamar no direct.”

O agente faz uma rodada curta de perguntas, mostra o roteiro para você aprovar, produz o
vídeo, confere frame a frame e entrega o MP4 com a checklist do formato (gancho, cortes,
legenda, chamada, capa, hashtags).

## O que vive onde

| Onde | O quê |
|---|---|
| `~/.olv-studio` | Python isolado, faster-whisper, edge-tts, modelo do Whisper, cache |
| `~/.cache` e `~/.npm` | navegador e pacotes do HyperFrames |
| a pasta do seu projeto | **só o vídeo**: `index.html`, `compositions/`, `assets/`, `renders/`, `plano.md` |

Comandos do estúdio (depois do `setup.sh`):

```bash
olv-asr  audio.wav -l pt -m small -o assets/audio/transcript.json   # transcrição
olv-tts  "texto da narração" -v pt-BR-FranciscaNeural -o voz.mp3    # voz + palavras
olv-doctor                                                     # diagnóstico
```

## Conteúdo da skill

| Arquivo | Função |
|---|---|
| `SKILL.md` | o fluxo completo: briefing, produção por modo (A/B/C), verificação, entrega |
| `motion-style.md` | padrão de movimento, layout em zonas e regras de GSAP |
| `templates-gravacao.md` | estruturas de Reels, Stories e Shorts (2026/2027) |
| `setup.sh` + `tools/` | bootstrap da máquina e os comandos `olv-*` |

## Requisitos

- Node.js ≥ 22 e FFmpeg no PATH
- Internet no primeiro uso (baixa o HyperFrames, o Python 3.12 via `uv` e o modelo do Whisper ≈ 500 MB)
- Python 3.9–3.13 (com `uv` não precisa instalar nada: ele traz o próprio)

## Licença

MIT — use, modifique e distribua livremente. Veja `LICENSE`.

> As skills do HyperFrames (motor de render) têm licença própria, do projeto HyperFrames.
