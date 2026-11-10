# Kit — Estúdio de vídeo (skill portátil)

Este pacote leva a capacidade de produção de vídeo (motion graphics + edição) para **qualquer harness de IA**.
Ele tem duas partes: a **skill do estúdio** (nossa, calibrada) e as instruções para instalar as **skills do fabricante** (HyperFrames) na máquina de destino.

```
kit-skill-olv/
├── README.md                  ← este arquivo
├── skills/editar-video/       ← a skill do estúdio (copie a pasta inteira)
│   ├── SKILL.md
│   ├── motion-style.md
│   └── templates-gravacao.md
└── vendor-skills-lock.json    ← referência de versões das skills do HyperFrames
```

## 1. Pré-requisitos da máquina de destino

- Node.js >= 22 e FFmpeg no PATH
- Rede para o primeiro `npx` (baixa o HyperFrames e o Chrome headless que ele usa)
- Um harness com **execução de shell** e **escrita de arquivos** (ver §4)

## 2. Instalação

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

## 3. Instalar a skill do estúdio no harness

Copie a pasta **inteira** `skills/editar-video/` (os três arquivos juntos — o `SKILL.md` referencia `motion-style.md` e `templates-gravacao.md` por caminho relativo).

| Harness | Onde colocar |
|---|---|
| OpenCode | `.opencode/skills/editar-video/` |
| Claude Code | `.claude/skills/editar-video/` |
| Cursor | anexar como regra: `.cursor/rules/editar-video.mdc` (SKILL.md como corpo + caminhos de motion-style.md e templates-gravacao.md) |
| Codex / harness com AGENTS.md | referenciar no `AGENTS.md` do projeto: “siga `skills/editar-video/SKILL.md` + `motion-style.md` + `templates-gravacao.md`” |
| Qualquer outro | colar `SKILL.md` + `motion-style.md` + `templates-gravacao.md` como instruções de sistema/contexto do agente |

## 4. O que o harness precisa saber fazer

| Capacidade | Sem ela |
|---|---|
| Escrever arquivos (HTML/CSS/JS) | Não produz o projeto |
| Rodar shell (`npx hyperframes check/snapshot/render`) | Modo degradado: escreve o projeto, mas não verifica nem renderiza — a pessoa roda os comandos |
| Ler imagens (snapshots) | Perde a verificação visual por frame (a mais importante) |

## 5. O que NÃO vai no pacote

- Projetos, renders e entregas (`projeto*/`, `saida/`) — cada vídeo nasce de um `npx hyperframes init` novo
- Assets de clientes (fotos, logo, trilhas) — cada projeto monta o próprio `assets/`
- Chaves/credenciais — nenhuma é necessária para o fluxo local

## 6. Fluxo depois de instalado

1. Peça o vídeo em linguagem natural — a skill entrevista o usuário (formato, nicho, dor, prova, chamada), escolhe o template de Reels/Stories/Shorts e escreve o roteiro para aprovação
2. O agente escreve as composições, roda `npm run check`, tira snapshots e confere frame a frame
3. Renderiza com `npm run render` e entrega o MP4 em `saida/`

## Licença

MIT — use, modifique e distribua livremente, mantendo o aviso de copyright. Veja `LICENSE`.

> As skills do fabricante (HyperFrames) instaladas via `npx hyperframes skills` têm licença própria (MIT do projeto HyperFrames); esta licença cobre este kit.
