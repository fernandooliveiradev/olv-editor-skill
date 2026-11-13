# OLV Studio

**Transforme um roteiro e um áudio em vídeo pronto para postar.**

OLV Studio é uma skill de vídeo para agentes de IA. Você conta o que quer, aprova o roteiro e recebe
o vídeo vertical no formato do Reels, do Stories ou do Short — com cenas animadas, legenda acompanhando
a fala e trilha escolhida a dedo.

Funciona no OpenCode, no Claude Code e no Cursor.

## O que você recebe

- **O vídeo pronto** — MP4 vertical (1080×1920), com cenas animadas no ritmo da fala.
- **Legenda na tela** — a palavra falada acende no momento exato, com o texto do roteiro aprovado.
- **Voz** — narração por IA em português do Brasil, ou a sua gravação tratada (ruído, volume, pausas).
- **Trilha** — escolhida numa biblioteca de 72 músicas por clima e andamento, baixa sob a voz.
- **O que postar** — gancho, chamada, capa e uma lista do que conferir antes de publicar.

## Como funciona

1. **Você conta o que quer.** Formato, público, a dor que o vídeo resolve e a chamada. Cinco perguntas,
   uma mensagem só. Se você já tem perfil de marca salvo, ele nem pergunta de novo.
2. **O roteiro volta para você aprovar.** Palavra por palavra, no tempo de cada bloco. Nada é produzido
   antes do seu "ok" — e o que você aprovou é o que vai para o vídeo.
3. **O vídeo é montado.** Cena por cena, no ritmo da fala: título, número, lista, CTA — cada tela com
   movimento de verdade, nunca um slide parado.
4. **Você recebe e confere.** O MP4, a prévia editável e o que fazer depois de publicar.

## Instalar

```bash
# 1. A skill (copie para a pasta de skills do seu agente)
git clone https://github.com/fernandooliveiradev/olv-editor-skill
cp -r olv-editor-skill/skills/editar-video ~/.config/opencode/skills/

# 2. O motor de vídeo
npx hyperframes skills

# 3. O estúdio: voz, transcrição e biblioteca (fora dos seus projetos)
bash skills/editar-video/setup.sh
~/.olv-studio/bin/olv-doctor --selftest
```

O último comando testa de verdade: grava uma frase com a voz de IA e transcreve de volta. Se passar,
está tudo pronto.

## Pedir um vídeo

> "Faz um Reels de 30 segundos sobre IA organizando as perguntas do dia a dia do negócio.
> A chamada é chamar no direct."

O estúdio pergunta o que falta, mostra o roteiro, produz e entrega.

## Trilhas prontas

A biblioteca tem 72 músicas instrumentais, medidas uma vez (andamento, duração, volume, respiro) para
o agente escolher rápido — sem abrir arquivo por arquivo.

```bash
olv-musica sync --de <sua pasta de músicas>   # ou baixe a pasta do Drive (link em musica.md)
olv-musica index
olv-musica listar --bpm 100-125
```

Colocar no vídeo é um comando: `olv-musica usar "Sunday in Salvador" --projeto .`

## Se você é técnico

A skill é texto, não código: cada arquivo rege uma parte do trabalho.

| Arquivo | O que rege |
|---|---|
| `SKILL.md` | as 8 etapas, com gate entre elas (roteiro → ativos → sincronia → cenas → verificação → render) |
| `motion-style.md` | movimento, ritmo, layout em zonas, regras de animação |
| `templates-gravacao.md` | estrutura de roteiro de Reels, Stories e Shorts |
| `midia.md` | as regras de vídeo, áudio e legenda que quebram o render |
| `musica.md` | a biblioteca de trilhas: medir, escolher, mixar |
| `robustez.md` | como verificar a entrega com evidência (inclusive sem ver imagem) e `olv-confere`, que transcreve o MP4 final e compara com o roteiro palavra por palavra |
| `plano-template.md` | o documento que registra cada decisão do projeto |
| `receitas/` | seis telas prontas para copiar (pergunta, número, lista, produto, editorial, CTA) |

Testado de ponta a ponta: motion puro, vídeo gravado com cortes, Stories em telas separadas, trilha
sob a voz, prévia no navegador e diagnóstico da máquina. As receitas são verificadas a cada alteração
por uma checagem automática no repositório.

## Requisitos

- Node.js 22 ou mais novo, e FFmpeg
- Internet no primeiro uso (baixa o motor, o Python do estúdio e o modelo de transcrição)
- Nada é instalado dentro da pasta do seu projeto

## Licença

MIT. Use, modifique e distribua. As skills do motor de vídeo (HyperFrames) têm licença própria.
