# OLV Studio — a skill de vídeo para agentes de IA

Um roteiro e um áudio viram um vídeo pronto. **OLV Studio** é uma skill que qualquer
agente de IA (OpenCode, Claude Code, Cursor…) usa para produzir vídeos de social com
padrão de estúdio: motion graphics com movimento de verdade, legenda palavra por palavra
e entrega no formato do Reels, do Stories ou do Short.

## O que você recebe

- **Vídeo 9:16 renderizado (MP4 1080×1920)** — cenas em motion graphics sincronizadas
  frame a frame com a fala, nunca tela parada.
- **Legenda karaokê** — palavra ativa destacada no ritmo da voz, com o texto do **roteiro
  aprovado** (a transcrição só fornece o tempo).
- **Voz de IA em pt-BR** ou a sua narração tratada (ruído, volume, cortes no silêncio).
- **Estrutura pronta para publicar** — gancho, chamada única e checklist das regras
  atuais do Instagram e do YouTube.
- **Receitas de tela verificadas** — seis cenas HTML+GSAP prontas para copiar (pergunta,
  número, lista, produto, editorial, CTA), testadas com `lint` e `check` limpos.
- **Instalação limpa** — tudo se instala uma vez, fora da pasta do projeto, em
  `~/.olv-studio`. Seus projetos nunca misturam dependência com entrega.

## Como funciona

```
seu texto + áudio (ou voz de IA)
        │
        ▼
  0  pré-voo — máquina e modelos, uma vez
  1  briefing — formato, objetivo, dor, prova e chamada (perfil de marca evita reperguntar)
  2  roteiro aprovado por você — bloco a bloco, no template do formato     ← gate
  3  ativos — voz/TTS, música, imagens, cortes do vídeo gravado            ← gate
  4  sincronia — cues, beatmap e o texto da legenda travados               ← gate
  5  cenas — receita por cena em HTML + GSAP (HyperFrames)
  6  verificação — check, folha de revisão, celular e motion sidecar       ← gate
  7  mixagem + render — −14 LUFS, MP4 conferido no ffprobe
  8  entrega — arquivos, relato do que foi verificado e pós-publicação
```

Cada etapa tem uma saída concreta e um gate; a skill **proíbe adiantar etapa** (roteiro antes do
formato, cena antes do ativo, render antes da verificação). O vídeo é feito numa ordem só.

## Instalação (3 passos)

```bash
# 1) A skill
git clone https://github.com/fernandooliveiradev/olv-editor-skill
cp -r olv-editor-skill/skills/editar-video ~/.config/opencode/skills/
#   (outro harness: copie para a pasta de skills dele — Claude Code usa .claude/skills/,
#    Cursor e afins: anexe SKILL.md + os arquivos companheiros)

# 2) O motor de render (HyperFrames)
npx hyperframes skills

# 3) O estúdio: transcrição, voz de IA e modelos — fora dos projetos
bash skills/editar-video/setup.sh
~/.olv-studio/bin/olv-doctor --selftest   # testa síntese de voz e transcrição de verdade
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
| `~/.olv-studio` | Python isolado, faster-whisper, edge-tts, modelo do Whisper, cache, perfis de marca |
| `~/.olv-studio/perfis/<cliente>.json` | o perfil da marca: cores, fontes, chamada, provas, o que não usar |
| `~/.cache` e `~/.npm` | navegador e pacotes do HyperFrames |
| a pasta do seu projeto | **só o vídeo**: `index.html`, `compositions/`, `assets/`, `renders/`, `plano.md` |

Comandos do estúdio (depois do `setup.sh`):

```bash
olv-asr  audio.wav -l pt -m small -o assets/audio/transcript.json   # transcrição
olv-tts  --text-file roteiro.txt -v pt-BR-FranciscaNeural -o voz.mp3 # voz + palavras
olv-doctor --selftest                                               # diagnóstico real (síntese + ASR)
```

## Conteúdo da skill

| Arquivo | Função |
|---|---|
| `SKILL.md` | as 8 etapas com gate, o mapa de skills do HyperFrames e o que não se adianta |
| `motion-style.md` | dicionário de motion, ritmo, layout em zonas, receitas de tela, regras de GSAP |
| `templates-gravacao.md` | estruturas de Reels, Stories e Shorts (roteiro, gancho, chamada, entregável) |
| `midia.md` | as regras de `<video>`/`<audio>`/`.clip` que quebram o render, e a mixagem |
| `robustez.md` | processo e verificação para qualquer modelo (sem impor visual) |
| `plano-template.md` | o esqueleto do `plano.md`: estado retomável, tokens, layout em px, cues, cortes |
| `receitas/` | seis cenas HTML+GSAP verificadas, uma por tipo de tela |
| `perfis/brand.example.json` | modelo do perfil de marca (evita repetir o briefing toda semana) |
| `setup.sh` + `tools/` | bootstrap da máquina, comandos `olv-*` e autoteste |

## Requisitos

- Node.js ≥ 22 e FFmpeg no PATH
- Internet no primeiro uso (baixa o HyperFrames, o Python 3.12 via `uv` e o modelo do Whisper ≈ 500 MB)
- Python 3.9–3.13 (com `uv` não precisa instalar nada: ele traz o próprio)

## Verificação — o que foi testado, e como

| Fluxo | Evidência |
|---|---|
| Receitas de tela | `lint` 0 erros/0 avisos e `check` 0 erros nas seis; olhadas em folha de contato |
| Instalação | `setup.sh` com Python 3.12 via `uv`, faster-whisper 1.2.1, edge-tts 7.3.1 |
| Diagnóstico | `olv-doctor --selftest`: síntese de voz ✓ e transcrição ✓; detecta ferramenta velha após atualizar a skill |
| Modo B (motion puro) | 12 s, 3 cenas + legenda karaokê; `check` 0 erros; render 1080×1920; mix −14,0 LUFS |
| Modo A (vídeo gravado) | bruto de 16,3 s com dois silêncios → 3 cortes (9,5 s) → 3 `<video>` com `data-media-start`; áudio do MP4 renderizado transcrito **na ordem certa**; `check` 0 erros; −14,0 LUFS |
| Stories | 3 MP4 de 8 s (1080×1920) + master de 24 s; `data-hold` nas telas estáticas |
| `media-use` | SFX do pacote local resolvido em `.media/` e renderizado com áudio |
| Preview | Studio em `:3002`, HTTP 200, `preview --context --json` respondendo |
| Portabilidade do `setup.sh` | caminho `sha256sum` e caminho `shasum -a 256` (macOS) testados, inclusive o aviso de drift |
| CI | `.github/workflows/verify.yml` roda sintaxe + lint das receitas a cada push e PR (`tests/run.sh`) |

**Não coberto:** Windows e macOS reais (só Linux + o caminho `shasum` simulado); música/imagem do
catálogo HeyGen (exigem login na conta do usuário; SFX local é offline).

## Licença

MIT — use, modifique e distribua livremente. Veja `LICENSE`.

> As skills do HyperFrames (motor de render) têm licença própria, do projeto HyperFrames.
