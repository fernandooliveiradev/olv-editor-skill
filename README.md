# Kit — Estúdio de vídeo (skill portátil)

Este pacote leva a capacidade de produção de vídeo (motion graphics + edição) para **qualquer harness de IA**.
Ele tem duas partes: a **skill do estúdio** (nossa, calibrada) e as instruções para instalar as **skills do fabricante** (HyperFrames) na máquina de destino.

```
kit-skill-olv/
├── README.md                  ← este arquivo
├── skills/editar-video/       ← a skill do estúdio (copie a pasta inteira)
│   ├── SKILL.md
│   ├── motion-style.md
│   ├── templates-gravacao.md
│   ├── setup.sh               ← bootstrap da máquina (~/.olv-studio)
│   └── tools/
│       ├── transcribe.py      ← faster-whisper com timestamps por palavra
│       └── tts.py             ← edge-tts com palavras cronometradas
└── vendor-skills-lock.json    ← referência de versões das skills do HyperFrames
```

## 1. Pré-requisitos da máquina de destino

- Node.js >= 22 e FFmpeg no PATH
- Rede para o primeiro `npx` (baixa o HyperFrames e o Chrome headless que ele usa) e para o `edge-tts`
- `uv` recomendado (instala um Python 3.12 isolado sem mexer no sistema); sem ele, um Python 3.9–3.13
- Um harness com **execução de shell** e **escrita de arquivos** (ver §5)

## 2. Instalação do motor

```bash
# 1) O motor (HyperFrames)
npx hyperframes init meu-video        # cria o projeto
npx hyperframes doctor                # confere ambiente

# 2) Skills do fabricante (contrato, CLI, catálogo, mídia…)
npx hyperframes skills                # instala o conjunto completo nos harnesses suportados
npx hyperframes skills check          # confere se estão atualizadas
npx hyperframes skills update <nome>  # instala/atualiza uma skill específica (on-demand)
```

> Instalar de novo na máquina destino é melhor do que copiar pastas antigas: as skills do fabricante evoluem com o CLI e são atualizadas pela pessoa (nunca pelo agente).

## 3. Bootstrap do estúdio (primeira vez na máquina)

Rode o setup que vem dentro da skill. Ele instala as ferramentas da máquina **fora da pasta de projetos**, em `~/.olv-studio` (ou `$OLV_HOME`):

```bash
bash skills/editar-video/setup.sh          # baixa tudo e o modelo small do Whisper
bash skills/editar-video/setup.sh --no-model   # adia o modelo (~500 MB) para a 1ª transcrição
```

| O quê | Onde |
|---|---|
| Python 3.12 isolado (via `uv`) | `~/.olv-studio/venv` |
| faster-whisper + edge-tts | `~/.olv-studio/venv` |
| modelo do Whisper | `~/.olv-studio/models/hf` |
| cache de modelos | `~/.olv-studio/cache` |
| `olv-asr`, `olv-tts`, `olv-doctor` | `~/.olv-studio/bin` |

```bash
~/.olv-studio/bin/olv-asr audio.wav -l pt -m small -o assets/audio/transcript.json
~/.olv-studio/bin/olv-tts "texto da narração" -v pt-BR-FranciscaNeural -o assets/audio/voz.mp3
~/.olv-studio/bin/olv-doctor
```

O `olv-tts` grava também `voz.words.json` com os tempos por palavra — serve para sincronizar cenas e legendas. Adicione `~/.olv-studio/bin` ao PATH para chamar sem o caminho completo.

> **A pasta do projeto continua limpa:** ela guarda só `index.html`, `compositions/`, `assets/`, `renders/` e `plano.md`. Nada de `venv/`, `node_modules/`, modelos ou caches dentro do vídeo.

## 4. Instalar a skill do estúdio no harness

Copie a pasta **inteira** `skills/editar-video/` (`SKILL.md`, `motion-style.md`, `templates-gravacao.md`, `setup.sh` e `tools/` — o `SKILL.md` referencia os outros por caminho relativo).

| Harness | Onde colocar |
|---|---|
| OpenCode | `.opencode/skills/editar-video/` |
| Claude Code | `.claude/skills/editar-video/` |
| Cursor | anexar como regra: `.cursor/rules/editar-video.mdc` (SKILL.md como corpo + caminhos de motion-style.md e templates-gravacao.md) |
| Codex / harness com AGENTS.md | referenciar no `AGENTS.md` do projeto: “siga `skills/editar-video/SKILL.md` + `motion-style.md` + `templates-gravacao.md`” |
| Qualquer outro | colar `SKILL.md` + `motion-style.md` + `templates-gravacao.md` como instruções de sistema/contexto do agente |

## 5. O que o harness precisa saber fazer

| Capacidade | Sem ela |
|---|---|
| Escrever arquivos (HTML/CSS/JS) | Não produz o projeto |
| Rodar shell (`npx hyperframes check/snapshot/render`) | Modo degradado: escreve o projeto, mas não verifica nem renderiza — a pessoa roda os comandos |
| Ler imagens (snapshots) | Perde a verificação visual por frame (a mais importante) |
| Rede no primeiro uso | Sem ela, rode o setup numa máquina com rede e copie `~/.olv-studio` |

## 6. O que NÃO vai no pacote

- Projetos, renders e entregas (`projeto*/`, `saida/`) — cada vídeo nasce de um `npx hyperframes init` novo
- Assets de clientes (fotos, logo, trilhas) — cada projeto monta o próprio `assets/`
- Dependências da máquina (Python, faster-whisper, edge-tts, modelos) — o `setup.sh` instala em `~/.olv-studio`
- Chaves/credenciais — nenhuma é necessária para o fluxo local (o `edge-tts` usa a API pública da Microsoft)

## 7. Fluxo depois de instalado

1. Peça o vídeo em linguagem natural — a skill entrevista o usuário (formato, nicho, dor, prova, chamada), escolhe o template de Reels/Stories/Shorts e escreve o roteiro para aprovação
2. O agente escreve as composições, roda `npm run check`, tira snapshots e confere frame a frame
3. Renderiza com `npm run render` e entrega o MP4 em `saida/`

## Licença

MIT — use, modifique e distribua livremente, mantendo o aviso de copyright. Veja `LICENSE`.

> As skills do fabricante (HyperFrames) instaladas via `npx hyperframes skills` têm licença própria (MIT do projeto HyperFrames); esta licença cobre este kit.
