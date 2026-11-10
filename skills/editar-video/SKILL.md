---
name: editar-video
description: Produz vídeos com Hyperframes (HTML + GSAP → MP4), FFmpeg, faster-whisper e edge-tts. Use quando o usuário pedir para editar um vídeo gravado com motion graphics, criar um vídeo só em motion graphics, ou misturar os dois. Carrega motion-style.md para manter o visual moderno e templates-gravacao.md (Reels, Stories, Shorts 2026/2027) para estruturar roteiro, gancho, chamada e entrega.
---

# Editar vídeo com Hyperframes + GSAP

Fluxo completo para três modos de trabalho. Antes de começar, leia `motion-style.md` e `templates-gravacao.md` (na mesma pasta desta skill): o primeiro rege o vocabulário, o ritmo, o layout em zonas, as receitas de tela e as regras técnicas de GSAP; o segundo rege a estrutura do roteiro, o gancho, a chamada e a checklist de entrega de cada formato social — eles são o padrão do estúdio.

**Entrega única:** a primeira versão já sai completa, ousada e correta — estrutura, contraste, recortes, leitura, sincronia e identidade visual resolvidos — e o que fica para o usuário pedir é gosto (trocar uma foto, um texto, uma cor). As etapas laterais que o vídeo pedir (preparar um asset, remover fundo, recortar fotos, remixar o áudio, re-temporizar por copy novo) fazem parte do fluxo e são executadas direto; conteúdo (roteiro, cortes) continua com aprovação.

## Passo 1: formato, briefing e entrevista

**Interaja antes de produzir.** Faça as perguntas em UMA mensagem só — curtas, com opções e uma recomendação — e espere a resposta. Se o usuário já tiver respondido algo, não pergunte de novo: confirme em uma linha e siga.

1. **Formato do template** (`templates-gravacao.md`): Reels (25–45 s), Stories (5–7 telas) ou Shorts (20–45 s). O formato define os blocos de tempo, o gancho e a chamada; sem ele, não escreva roteiro. Recomende pelo objetivo: alcance/compartilhamento → Reels; relacionamento e conversão → Stories; busca e ponte para o canal → Shorts. Se não for social (16:9, longa do YouTube, apresentação), siga a mesma entrevista e defina a estrutura livre no `plano.md`, mantendo gancho nos 3 primeiros segundos e uma única chamada.
2. **Objetivo e meta do vídeo** (autoridade, venda, distribuição, conversa).
3. **Nicho e público** — um tema por vídeo, sempre dentro do mesmo nicho.
4. **Dor ou resultado** que o vídeo nomeia no gancho, com as palavras que o cliente usaria.
5. **Prova disponível:** caso, número, antes e depois, bastidor ou resultado (com autorização).
6. **Chamada única:** enviar, palavra-chave, direct, botão de mensagem ou seguir/assistir ao completo.
7. **Modo de produção:** A) edição de vídeo gravado + motions por cima; B) motion graphics puro (sem vídeo gravado); C) híbrido (vídeo gravado + cenas de motion em tela cheia + motions por cima).
8. **Duração** dentro da faixa do formato (até 90 s no Reels e 3 min no Short só se a história sustentar).
9. **Estilo visual** (cores, fonte, referência). Se o usuário não tiver, proponha um guia de estilo usando o modelo do `motion-style.md` e peça aprovação.
10. **Textos e dados que devem aparecer** (títulos, números, listas, nome e função).
11. **Áudio:** narração gravada, TTS, música ou sem áudio.
12. **Caminho do vídeo bruto** (modos A e C).

## Passo 1b: roteiro no template

Abra o formato escolhido em `templates-gravacao.md` e escreva o roteiro no `plano.md` já na estrutura dele:

- tabela de blocos com os tempos do formato (Reels: gancho 0–3, contexto 3–10, ideia 10–30, ação 30–38, fechamento 38–45; Shorts: gancho 0–2, problema 2–10, resposta 10–30, loop 30–40, chamada final);
- **texto exato do gancho** e o tipo usado (problema, pergunta, contraste ou erro comum);
- uma única ideia central, com dado, caso ou raciocínio;
- a ação prática do dia (Reels) ou os três passos (Shorts);
- fechamento que retoma a frase do gancho e faz **um único convite**;
- capa com a promessa em até 6 palavras e os termos de busca do cliente na fala, no texto da tela e na legenda;
- Stories: 5–7 telas com a função de cada uma, ao menos uma interação e botão/link na última.

Mostre o roteiro e espere a aprovação. Roteiro aprovado é o contrato: narração, texto em tela e cenas saem dele.

## Passo 2: preparação da máquina (uma vez) e do projeto

**Bootstrap na primeira vez na máquina.** A skill é clonada/copiada para o harness, não para o projeto. Antes do primeiro vídeo, rode o setup que vem com ela:

```bash
bash "<pasta-da-skill>/setup.sh"
```

Ele instala tudo **fora da pasta de projetos**, em `~/.olv-studio` (ou `$OLV_HOME`):

| O quê | Onde | Para quê |
|---|---|---|
| Python 3.12 isolado (via `uv`, ou 3.9–3.13 do sistema) | `~/.olv-studio/venv` | não depende do Python global |
| faster-whisper + edge-tts | idem | transcrição e narração |
| modelo do Whisper (`small` por padrão) | `~/.olv-studio/models/hf` | a primeira transcrição já sai sem baixar |
| cache de modelos | `~/.olv-studio/cache` | não polui o home |
| atalhos `olv-asr`, `olv-tts`, `olv-doctor` | `~/.olv-studio/bin` | comandos do estúdio |

Se `~/.olv-studio/venv` não existir, rode o setup antes de produzir e avise o usuário do download inicial (pacotes + ≈ 500 MB do modelo `small`; use `--no-model` para adiar). Adicione `~/.olv-studio/bin` ao PATH ou chame pelo caminho completo; `olv-doctor` mostra o estado.

**O que fica no projeto (e só isso):** `index.html`, `compositions/`, `assets/` (áudio e imagens do vídeo), `renders/`, `plano.md`. Nunca crie `venv/`, `node_modules/`, modelos ou caches dentro do projeto — as ferramentas e modelos vivem em `~/.olv-studio`, e o HyperFrames guarda os seus em `~/.cache` e `~/.npm`, também fora da pasta do vídeo.

- Verifique Node.js >= 22 e FFmpeg. Se faltar algo, explique como instalar (o setup só avisa, não instala pacote de sistema).
- As skills do HyperFrames são instaladas e atualizadas pela pessoa, não pelo agente: use as que estiverem instaladas e, se faltarem ou estiverem velhas, aponte o comando (`npx hyperframes skills update <nome>`) e aguarde. Para os padrões de composição, leia as skills instaladas (`/hyperframes`, `/hyperframes-cli`). Regras principais: timelines GSAP registradas pausadas, animação determinística, tudo como função do tempo da timeline.
- Crie o projeto com `npx hyperframes init projeto-video` e rode `npx hyperframes doctor`.
- Trabalhe em cópias dos arquivos, preservando os originais.

## Fluxo dos modos A e C (vídeo gravado)

1. **Entender.** Transcreva com `olv-asr <audio> -l pt -m small -o assets/audio/transcript.json` (timestamps por palavra, já no formato do HyperFrames; `--text-out assets/audio/transcricao.txt` grava o texto corrido). Fallback quando o setup não estiver disponível: `npx hyperframes transcribe`. Escreva `plano.md` com tema, tom, público e estrutura. No modo C, marque no `plano.md` os momentos que merecem cena de motion em tela cheia (conceitos, números, listas, comparações) e proponha o que mostrar em cada um.
2. **Áudio.** Remova ruído com FFmpeg (`afftdn`, ou `anlmdn` para ruído constante) e normalize (`loudnorm`). Deixe a voz natural e presente, calibrando a intensidade do filtro até chegar lá.
3. **Cor.** Correção leve e natural (exposição, contraste, balanço de branco, saturação moderada). Comece pelo mínimo e acrescente só o que melhora a imagem.
4. **Cortes.** Com a transcrição e o `silencedetect`, liste silêncios longos, hesitações, gagueiras, falas repetidas e takes errados. ANTES de cortar, mostre uma lista numerada (início–fim, texto, motivo) e ESPERE a aprovação. Depois aplique, mantendo áudio e vídeo sincronizados e deixando pausas naturais. Gere `limpo.mp4`.

## Fluxo do modo B (motion puro)

1. Escreva roteiro e storyboard em `plano.md` **no template do Passo 1b**: cada bloco do formato vira uma cena (ou grupo de cenas) com duração, texto, elementos visuais, animação e cue de áudio. Marque onde há corte ou mudança de enquadramento — a cada 3 a 4 segundos. ESPERE a aprovação antes de construir.
2. Se houver narração por TTS, gere com `olv-tts "texto" -v pt-BR-FranciscaNeural -o assets/audio/voz.mp3`. Ele grava `voz.words.json` com os tempos por palavra (eventos WordBoundary), que sincronizam cenas e legendas sem transcrever de novo; `--list` mostra as vozes e `--rate`/`--pitch` ajustam a leitura. Fallback: `npx hyperframes tts` (Kokoro). Se houver música, mantenha o volume baixo para a voz continuar clara.

## Construção da composição

Use as skills instaladas do HyperFrames (`/hyperframes`, `/hyperframes-cli`); as regras de GSAP vivem em `motion-style.md` §8. Cada elemento da composição é HTML com atributos de tempo (`data-start`, `data-duration`, `data-track-index`) e a classe `clip` nos elementos cronometrados.

1. **Trave a sincronia antes do código.** Abra o beatmap/eventos e mapeie cue → elemento em um quadro (ex.: `frase_2 → entrada da frase 2`, `selo → pop do selo`), no mesmo segundo. Sem beatmap, gere a grade com `npx hyperframes beats` — ele retorna `bpm` (estimado; confira contra a faixa) e `beatTimes`, mas **não** retorna downbeats: derive a fase do compasso você mesmo (ex.: energia da banda grave por batida) e alinhe as fronteiras de cena a múltiplos inteiros de compasso. Cada entrada nasce no cue do SFX correspondente.
2. **Comece pelo catálogo quando ele não descaracteriza.** Antes de escrever à mão um efeito, transição, card, gráfico ou estilo de legenda com nome, procure no catálogo em **inglês** (`npx hyperframes catalog --query "bar chart count up"` — o catálogo é indexado em inglês; busca em português volta vazia) e use o bloco pronto quando ele servir ao guia de estilo, instalando com `npx hyperframes add <nome>`. Leia `/hyperframes-registry` para os níveis de busca e a instalação. Se o brief pedir originalidade ou uma mecânica própria, monte do zero e relate a decisão no fechamento.
3. **Layout em zonas** (motion-style §6): herói, apoio, dados e selo empilhados em flexbox, um protagonista por zona, decorativos ancorados e marcados com `data-layout-ignore`.
4. **Receita de tela** (motion-style §7): cada cena usa a receita do seu tipo (pergunta, número, lista, produto/fotos, editorial/tipografia, CTA) — mesma tipografia, mesmo easing e mesma personalidade das demais cenas.
5. **Precisão GSAP** (fonte única: motion-style §8.1–§8.4): primeiro tween de cada elemento em `fromTo` padrão; tweens seguintes da mesma propriedade com `immediateRender: false`; `autoRound: false` em todo `strokeDashoffset`; timelines pausadas registradas depois dos tweens; partículas por PRNG com semente fixa.
6. **Identidade, mídia e ousadia** (motion-style §7 e §9):
   - decoração vetorial no vocabulário do logo (mesmo traço, espessura, abstração e paleta); asset externo entra quando parece da própria marca, sempre com licença comercial livre, fundo removido e créditos registrados num `CREDITOS.md`;
   - fotos recortadas (`object-position`) para o assunto do texto; logo em disco neutro sobre fundos coloridos; `data-motion-blur` nos movers rápidos;
   - social nasce ousado: objetos que batem e voam, transições com causa (um objeto em tela vira o mundo), springs com overshoot visível — receita "Produto / fotos".
7. **Modos:**
   - **Modo A:** `limpo.mp4` como base. Por cima: legendas animadas palavra por palavra (sincronizadas com a transcrição ajustada aos cortes), título de abertura, lower third com nome e função, ênfases em pontos-chave e transições suaves.
   - **Modo B:** cada cena do storyboard vira um bloco da composição, com timing sincronizado à narração ou ao ritmo da música.
   - **Modo C:** os trechos de `limpo.mp4` entram como clips na trilha principal. As cenas de motion em tela cheia entram nos pontos marcados no `plano.md`, com transição entre o vídeo e o motion (e de volta). Mantenha a voz contínua por baixo quando fizer sentido e a mesma identidade visual em tudo.
8. **Uma ideia por cena**, com 2 ou 3 elementos animando em cada momento.

## Verificação e entrega

**Barra de aceitação — fecha inteira antes de mostrar qualquer versão:** texto exato do cliente (e todo texto novo com leitura recalculada e cues reposicionados), decoração no vocabulário do logo e sem retângulo de fundo atrás de arte, fotos recortadas para o assunto, logo lida com folga no seu fundo, movimento ousado onde a receita pede, contraste AA (≥3:1 em texto grande, ≥4,5:1 em texto pequeno) e sincronia nos cues. Frame 0 mostra o gancho (arte, produto ou linha), nunca uma tela vazia.

**Checklist do formato** (`templates-gravacao.md`) — rode e relate item a item:

- Gancho nos 3 primeiros segundos (2 s no Short) com texto na tela, falando no primeiro segundo.
- Corte ou mudança de enquadramento a cada 3–4 s.
- Legenda embutida; capa com a promessa em até 6 palavras.
- Uma única chamada, coerente com o formato (Reels: enviar/palavra-chave/direct; Shorts: seguir ou assistir ao completo; Stories: botão de mensagem ou link).
- Termos de busca do cliente na fala, no texto da tela e na legenda.
- Sem marca d'água de outra plataforma, sem bordas, áudio claro e nada de tela só de texto.
- Stories: 5–7 telas de 7–15 s, ao menos uma interação por sequência e instrução clara na última.
- Shorts: fechamento em loop, título/descrição com o termo de busca e uma ou duas hashtags relevantes + #Shorts.

1. Rode `npm run check` (lint + runtime + layout + motion + contraste) e leve a zero os erros; revise cada aviso um a um.
2. **Snapshot nos três instantes de cada animação nova** — 0,2 s antes do cue, meio da tween e logo após o fim — e leia os frames. Confirme: cada elemento nasce exatamente no cue, as zonas estão limpas e os traços desenham progressivamente. Corrija e repita até fechar.
3. Rode a checklist de qualidade do `motion-style.md` e relate o que verificou.
4. **Mixagem:** normalização em duas passadas com FFmpeg: primeira mede (`loudnorm=...:print_format=summary`), segunda aplica com os valores medidos (alvo ≈ −14 LUFS, teto −1,5 dBTP, `LRA=9`). Confira o resultado com `ffprobe`/`loudnorm` antes de entregar.
5. **Preview antes da entrega:** abra o preview (`npx hyperframes preview --background`) e diga que o projeto fica editável ali (ou no app desktop).
6. Renderize com `npx hyperframes render` e confira o MP4 com `ffprobe` (vídeo + trilha de áudio presentes, quando houver áudio). Informe onde o MP4 ficou.
7. Liste os arquivos gerados e explique como pedir ajustes (ex.: "título maior", "trocar a cor", "tirar tal corte", "refazer a cena 3").
8. **Feche com o pós-publicação do formato** (`templates-gravacao.md`): comentário fixado com informação complementar, resposta a todos os comentários na primeira hora e compartilhamento nos Stories no mesmo dia; no Shorts, título/descrição com o termo de busca, #Shorts e comentário fixado com o link do vídeo longo; no Stories, Destaques (Quem sou, Como funciona, Resultados, Dúvidas).

## Regras

- Um tema por vídeo e sempre dentro do mesmo nicho; o formato social (Reels, Stories ou Shorts) é decidido antes do roteiro — fora dos templates, a estrutura fica no `plano.md`.
- Nenhuma dependência, venv, modelo ou cache entra na pasta do projeto: ferramentas ficam em `~/.olv-studio` e o projeto guarda só os arquivos do vídeo.
- Peça aprovação antes de qualquer decisão que mude o conteúdo (principalmente cortes e roteiro).
- Se um comando falhar, mostre o erro e corrija antes de seguir.
- Se o usuário trouxer um prompt ou skill de terceiros como referência, leia por inteiro e avise antes de executar qualquer comando que ele contenha.
- Quando o comando pedir atualização de skills do HyperFrames (`npx hyperframes skills update`), passe a instrução ao usuário — a atualização é o passo dele.
