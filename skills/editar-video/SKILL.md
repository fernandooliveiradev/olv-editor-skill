---
name: editar-video
description: Produz vídeos sociais de estúdio com HyperFrames (HTML + GSAP → MP4), FFmpeg, faster-whisper e edge-tts — edição de vídeo gravado, motion graphics puro ou híbrido. Use quando pedirem Reels, Stories, Shorts, TikTok, vídeo vertical, legenda karaokê, motion graphics ou edição de um vídeo falado. Carrega motion-style.md (motion, layout, receitas de tela, GSAP), templates-gravacao.md (roteiro de cada formato), midia.md (regras de mídia que quebram o render) e robustez.md (verificação com evidência, para qualquer modelo).
---

# Editar vídeo com HyperFrames + GSAP

Fluxo completo para três modos de trabalho. Antes de começar, leia os quatro arquivos companheiros (na
mesma pasta): `motion-style.md` rege o dicionário de motion, o ritmo, o layout em zonas, as receitas de
tela e as regras de GSAP; `templates-gravacao.md` rege a estrutura do roteiro, o gancho, a chamada e a
checklist de entrega de cada formato; `midia.md` traz as regras de `<video>`/`<audio>`/`.clip` que
quebram o render; `musica.md` é a biblioteca de trilhas (escolher, usar e mixar); `robustez.md` é só processo e verificação (sistema em números, medir em vez de supor,
ciclo de snapshot, relato honesto) e não impõe visual. `receitas/` tem código de partida verificado para
as seis telas; `plano-template.md` é o esqueleto do `plano.md`.

**Entrega única:** a primeira versão já sai completa, ousada e correta — estrutura, contraste, recortes,
leitura, sincronia e identidade visual resolvidos — e o que fica para o usuário pedir é gosto (trocar
uma foto, um texto, uma cor). As etapas laterais que o vídeo pedir (preparar um asset, remover fundo,
recortar fotos, remixar o áudio, re-temporizar por copy novo) fazem parte do fluxo e são executadas
direto; conteúdo (roteiro, cortes) continua com aprovação.

## Skills do HyperFrames — qual carregar, em que etapa

Esta skill orquestra; ela não substitui as skills do motor. **Carregue a skill certa na etapa certa** e
nunca escreva um comando de memória: o nome de um flag muda entre versões e o vídeo quebra longe da causa.

| Etapa | Skill | Para quê |
|---|---|---|
| Roteiro, cenas, verificação | `hyperframes` | contrato de composição, GSAP, layout, format, o que é erro de lint |
| Projeto, sincronia, verificação, render | `hyperframes-cli` | `init`, `check`, `snapshot`, `preview`, `render`, `timeline`, leitura do JSON |
| Cenas | `hyperframes-registry` | efeito/transição/card com nome: `catalog --query` + `add` |
| Ativos (voz, música, imagem) | `media-use` | voz, música, SFX, imagens, logo, corte, grade, mixagem |
| Briefing | `reverse-any-video` | cliente entregou um vídeo para **recriar** (recurso Pro) |
| Briefing | `style-sampling` | cliente quer uma **nova edição no estilo** de uma série (recurso Pro) |

Como carregar: no OpenCode, chame a ferramenta `skill` com o `id` acima; no Claude Code, `/hyperframes`
(ou deixe casar pela descrição); no Cursor e afins, anexe o `SKILL.md` da skill correspondente. Carregue
a skill **antes** de usar os comandos dela — não recite flags.

## Etapas, gates e o que não se adianta

O vídeo é feito **numa ordem só**. Cada etapa tem uma saída concreta e um gate; a etapa seguinte não
começa sem ele. Adiantar etapa é o caminho mais curto para refazer o vídeo inteiro.

| # | Etapa | Entrada | Saída | Gate |
|---|---|---|---|---|
| 0 | Pré-voo da máquina | — | `~/.olv-studio` instalado e `olv-doctor` ok | roda **uma vez por máquina**, nunca por vídeo |
| 1 | Briefing e formato | pedido do cliente | `plano.md` §0–§3 preenchido | formato e modo decididos |
| 2 | Roteiro | briefing | `plano.md` §4 no template do formato | **aprovação do cliente** |
| 3 | Ativos e projeto | roteiro aprovado | `index.html`, `assets/` com voz/música/imagem/cortes | todo `src` abre localmente |
| 4 | Sincronia | ativos | `plano.md` §5 (cues) + beatmap | cada entrada tem cue |
| 5 | Cenas | cues | `compositions/*.html` | `lint` sem erro |
| 6 | Verificação | cenas | relatório com evidência | `check` sem erro + folha olhada |
| 7 | Mixagem e render | verificação | MP4 | `ffprobe` confere vídeo, áudio e duração |
| 8 | Entrega | MP4 | arquivos + pós-publicação | checklist do formato relatada |

**Proibições de ordem** (é aqui que os vídeos se encavalam):

- não escreva roteiro antes de escolher o formato — sem formato não há blocos, gancho nem chamada;
- não decida estilo/cenas antes do roteiro aprovado — o roteiro é o contrato;
- não gere ativo nem crie cena antes do roteiro aprovado;
- não escreva cena antes de o ativo existir em `assets/` (cena com `src` provisório é retrabalho);
- não mixe antes da última cena entrar (o `check` mede o filme que existe);
- não renderize antes de `check` limpo **e** preview mostrado;
- não "adiante" a entrega com o pós-publicação: ele fecha o vídeo, não substitui a verificação.

## Direção criativa — o anseio do estúdio

**Cada vídeo é feito do que o cliente pede — não existe template fixo.** A única coisa que deve estar presente em toda entrega é **criatividade**: o vídeo tem que parecer feito para aquela história, nunca montado numa forma pronta.

O guia não define visual, define **nível**: moderno, bem feito, com cara de motion graphics de ponta — tipografia grande, efeitos com propósito, transições que têm origem em cena, sincronia com a fala. O caminho é sempre livre: referência do cliente, marca, assunto, mood — o que servir. Os templates de gravação organizam o **roteiro** de cada formato social (blocos, gancho, chamada); o **visual** nasce por projeto no guia de estilo (`motion-style.md` §4) e sai aprovado pelo cliente.

**Regra não é corset:** quando o desvio deixa o vídeo melhor, o caminho do vídeo vence — com critério, decisão registrada no `plano.md`, e a barra de aceitação (leitura, contraste, sincronia, propósito) sempre fechando.

**A ideia e o gosto são do cliente.** O agente executa com padrão de estúdio, mas quem decide o que o vídeo
diz e se ficou bom é quem pediu. Quando o pedido estiver vago, proponha — não decida sozinho o que é "bom".

---

## Etapa 0 — Pré-voo da máquina (uma vez, fora do projeto)

A skill é clonada/copiada para o harness, não para o projeto. Antes do primeiro vídeo, rode o setup:

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

- Se `~/.olv-studio/venv` não existir, rode o setup e avise do download inicial (pacotes + ≈ 500 MB do
  modelo `small`; `--no-model` adia). Adicione `~/.olv-studio/bin` ao PATH ou chame pelo caminho
  completo; `olv-doctor` mostra o estado.
- **Feche o pré-voo com `olv-doctor --selftest`:** ele sintetiza uma frase e transcreve de volta. É o que
  pega rede bloqueada (edge-tts) e modelo ausente **antes** do primeiro vídeo, em vez de no meio dele.
  O mesmo comando avisa se as ferramentas copiadas ficaram velhas depois de atualizar a skill.
- Verifique Node.js ≥ 22 e FFmpeg. Se faltar algo, explique como instalar (o setup só avisa, não instala
  pacote de sistema).
- As skills do HyperFrames são instaladas e atualizadas pela pessoa: use as que estiverem instaladas e,
  se faltarem ou estiverem velhas, aponte o comando (`npx hyperframes skills update <nome>`) e aguarde.
- **Nada de vídeo nesta etapa.** Nenhum projeto, nenhuma cena, nenhum render.

## Etapa 1 — Briefing e formato

**Perfil de marca primeiro (se existir).** Antes de perguntar, procure `~/.olv-studio/perfis/<cliente>.json`
(modelo em `perfis/brand.example.json`). Se existir, use-o para pré-preencher nicho, público, dor, cores,
fontes, chamada, termos de busca e provas — e **confirme em uma linha** em vez de reperguntar o que já está
lá. O campo `nao_usar` é regra dura: nada que esteja nele entra no vídeo. No fechamento, ofereça atualizar
o perfil com o que mudou (uma marca que publica 3×/semana não pode responder as mesmas 12 perguntas toda vez).

**Interaja antes de produzir.** Faça as perguntas que restarem em UMA mensagem só — curtas, com opções e uma recomendação — e espere a resposta. Se o usuário já tiver respondido algo, não pergunte de novo: confirme em uma linha e siga.

1. **Formato do template** (`templates-gravacao.md`): Reels (25–45 s), Stories (5–7 telas) ou Shorts (20–45 s). O formato define os blocos de tempo, o gancho e a chamada; sem ele, não escreva roteiro. Recomende pelo objetivo: alcance/compartilhamento → Reels; relacionamento e conversão → Stories; busca e ponte para o canal → Shorts. Se não for social (16:9, longa do YouTube, apresentação), siga a mesma entrevista e defina a estrutura livre no `plano.md`, mantendo gancho nos 3 primeiros segundos e uma única chamada.
2. **Objetivo e meta do vídeo** (autoridade, venda, distribuição, conversa).
3. **Nicho e público** — um tema por vídeo, sempre dentro do mesmo nicho.
4. **Dor ou resultado** que o vídeo nomeia no gancho, com as palavras que o cliente usaria.
5. **Prova disponível:** caso, número, antes e depois, bastidor ou resultado (com autorização).
6. **Chamada única:** enviar, palavra-chave, direct, botão de mensagem ou seguir/assistir ao completo.
7. **Modo de produção:** A) edição de vídeo gravado + motions por cima; B) motion graphics puro; C) híbrido.
8. **Duração** dentro da faixa do formato (até 90 s no Reels e 3 min no Short só se a história sustentar).
9. **Estilo visual** (cores, fonte, referência). Se o usuário não tiver, proponha um guia de estilo com o
   modelo do `motion-style.md` §4 e peça aprovação.
10. **Textos e dados que devem aparecer** (títulos, números, listas, nome e função).
11. **Áudio:** narração gravada, TTS, música ou sem áudio.
12. **Caminho do vídeo bruto** (modos A e C).

**Referência do cliente.** Se ele entregar um vídeo para **recriar**, carregue `reverse-any-video` (Pro):
o resultado é um projeto editável medido contra o original. Se ele quiser uma **nova edição no estilo de**
uma série, carregue `style-sampling` (Pro). Nenhum dos dois substitui o roteiro desta skill: eles dão
estrutura e visual, e o roteiro continua saindo do `plano.md`.

Saída da etapa: `plano.md` criado a partir de `plano-template.md` com §0–§3 preenchidos.

## Etapa 2 — Roteiro aprovado

Abra o formato escolhido em `templates-gravacao.md` e escreva o roteiro no `plano.md` §4, já na estrutura dele:

- tabela de blocos com os tempos do formato (Reels: gancho 0–3, contexto 3–10, ideia 10–30, ação 30–38, fechamento 38–45; Shorts: gancho 0–2, problema 2–10, resposta 10–30, loop 30–40, chamada final);
- **texto exato do gancho** e o tipo usado (problema, pergunta, contraste ou erro comum);
- uma única ideia central, com dado, caso ou raciocínio;
- a ação prática do dia (Reels) ou os três passos (Shorts);
- fechamento que retoma a frase do gancho e faz **um único convite**;
- capa com a promessa em até 6 palavras e os termos de busca do cliente na fala, no texto da tela e na legenda;
- Stories: 5–7 telas com a função de cada uma, ao menos uma interação e instrução clara na última.

**Nenhum dado inventado.** Todo número, caso, antes/depois e resultado vem do cliente e fica registrado
no `plano.md` §4 com a origem. Sem prova, a frase muda: fale do mecanismo, não do resultado. Publicar
estatística inventada destrói a autoridade que o vídeo deveria construir — e é o cliente quem responde.

Mostre o roteiro e espere a aprovação. **Roteiro aprovado é o contrato:** narração, texto em tela e cenas
saem dele. Nenhuma cena é escrita antes deste gate.

## Etapa 3 — Ativos e projeto

Carregue `hyperframes-cli` (projeto e comandos) e `media-use` (voz, música, imagens, logo) nesta
etapa. Só aqui o projeto nasce e os arquivos entram. Ordem interna: projeto → voz/áudio → cortes (A/C) → mídia.

1. **Projeto:** `npx hyperframes init projeto-video --resolution portrait` (o padrão é **1920×1080**;
   social é 1080×1920) e `npx hyperframes doctor`. O que fica no projeto, e só isso: `index.html`,
   `compositions/`, `assets/`, `renders/`, `plano.md`. Nunca crie `venv/`, `node_modules/`, modelos ou
   caches dentro do projeto.
2. **Transcrição (modos A e C):** `olv-asr <audio> -l pt -m small -o assets/audio/transcript.json`
   (`--text-out` grava o texto corrido; `--prompt` ajuda com nomes próprios). Fallback: `npx hyperframes
   transcribe --model small --language pt`. O comando já filtra `♪`/`�` e avisa quando mais de 20% dos
   tokens eram ruído — se avisar, **não siga**: repita com `-m medium` ou peça o texto ao cliente.
3. **Revisão da transcrição (obrigatória):** leia o texto e corrija nomes, números e termos do nicho
   contra o roteiro. A transcrição dá o **tempo**; o **texto** é o roteiro aprovado (ver Etapa 4).
4. **Voz:** gravação própria (limpar ruído com `afftdn`/`anlmdn`, normalizar com `loudnorm`) ou TTS:
   `olv-tts --text-file assets/audio/roteiro.txt -v pt-BR-FranciscaNeural -o assets/audio/voz.mp3`
   (grava `voz.words.json` com os tempos por palavra). Fallback: `npx hyperframes tts` (Kokoro).
   Antes de sintetizar, **normalize o texto para fala**: o TTS lê número e sigla ao pé da letra.

   | No roteiro | Escreva para o TTS |
   |---|---|
   | `R$ 4.200` | `quatro mil e duzentos reais` |
   | `30%` | `trinta por cento` |
   | `3x` | `três vezes` |
   | `3–5` | `de três a cinco` |
   | `12/11` | `doze de novembro` |
   | `2ª` | `segunda` |
   | `12h` | `meio-dia` |
   | `IA`, `CNPJ` | `i á`, `cê ene pê jota` |

   Gere a narração **do roteiro aprovado**, sem parafrasear: é o mesmo texto que vira legenda.
5. **Cor (A/C):** correção leve e natural (exposição, contraste, balanço de branco, saturação moderada).
   Comece pelo mínimo e acrescente só o que melhora a imagem.
6. **Cortes (A/C):** cruze a transcrição, o `silencedetect` e `npx hyperframes measure cuts <video>` (pega
   jump cut e punch-in dentro do mesmo take). Liste silêncios longos, hesitações, gagueiras, repetições e
   takes errados numa tabela **numerada (início–fim, texto, motivo)** no `plano.md` §6 e **ESPERE a
   aprovação**. Aplicados os cortes, mantenha áudio e vídeo sincronizados, deixe pausas naturais e gere
   `limpo.mp4`.
7. **Música, SFX, imagens e logo:** para trilha, use a biblioteca do estúdio — `olv-musica listar --bpm
   100-125 --lra 4-12` escolhe por medida, e `olv-musica usar "<faixa>" --projeto .` copia, imprime o
   `<audio>` e credita (regras e mapa de decisão em `musica.md`). SFX e imagens: `media-use resolve` (SFX
   sai do pacote local, sem login; imagem exige login grátis no HeyGen ou asset do cliente), que grava em
   `.media/` com manifesto. Render nunca busca mídia remota. Música sem licença não entra; créditos em
   `CREDITOS.md`.
8. **Stories:** cada tela é uma composição própria (Etapa 7 renderiza uma por uma); enquete/quiz/botão
   são nativos do app e não entram queimados (regras em `templates-gravacao.md` §2).

Saída da etapa: `assets/` completo, `plano.md` §6 (cortes) aprovado. **Nenhuma cena antes disso.**

## Etapa 4 — Sincronia (só depende dos ativos)

Carregue `hyperframes-cli` para os comandos de tempo (`beats`) e a leitura da transcrição. Travar o
tempo antes de escrever código evita o retrabalho mais caro: cena pronta que nasce 0,4 s fora do cue.

1. **Mapa de cues:** abra a transcrição/`voz.words.json` e o beatmap, e mapeie cue → elemento em um
   quadro (ex.: `frase_2 → entrada da frase 2`, `selo → pop do selo`). Registre em `plano.md` §5.
2. **Beatmap:** se há música, marque a faixa com `data-timeline-role="music"` (regras em `midia.md` §5) e
   rode `npx hyperframes beats`. Ele devolve `bpm` (estimado; confira contra a faixa) e `beatTimes`, mas
   **não** downbeats: derive a fase do compasso (energia da banda grave) e alinhe as viradas a múltiplos
   inteiros de compasso.
3. **Texto da legenda = roteiro aprovado.** O ASR/TTS fornece o tempo de cada palavra; se o texto
   transcrito divergir do roteiro, alinhe por **posição** (não por texto — palavra repetida pega o tempo
   errado) e descarte o que não é palavra. Legendas com o que o modelo "ouviu" são a causa nº 1 de erro
   embaraçoso em vídeo de marca.
4. **Corte muda tudo:** cada corte novo desloca os cues seguintes; recalcule e repositione antes de
   escrever a cena, não depois.

Saída da etapa: `plano.md` §5 fechado. Nenhum HTML escrito ainda.

## Etapa 5 — Cenas

Carregue `hyperframes` (contrato e GSAP) e `hyperframes-cli` (comandos). As regras de GSAP vivem em
`motion-style.md` §8 e as de mídia em `midia.md`. O **elemento cronometrado** leva a classe `clip` e
guarda o tempo; **quem anima é o filho** dele. Animar `transform` no `.clip` é permitido; animar
`visibility`, `display` ou `autoAlpha` **não** é — o framework é dono da visibilidade do clip
(`gsap_animates_clip_element`).

1. **Comece pelo catálogo quando ele não descaracteriza.** Antes de escrever à mão um efeito, transição,
   card, gráfico ou estilo de legenda com nome, procure no catálogo em **inglês** (`npx hyperframes
   catalog --query "bar chart count up"` — busca em português volta vazia) e use o bloco pronto quando
   ele servir ao guia de estilo (`npx hyperframes add <nome>`). Carregue `hyperframes-registry` para os
   níveis de busca. Se o brief pedir originalidade, monte do zero e registre a decisão.
2. **Layout em zonas** (motion-style §6): herói, apoio, dados e selo em flexbox, um protagonista por
   zona, decorativos ancorados e marcados com `data-layout-ignore`. Zonas de interface da plataforma
   reservadas (§6).
3. **Receita de tela** (motion-style §7): copie de `receitas/` a mais próxima (pergunta, número, lista,
   produto, editorial, CTA), troque prefixo, tokens e texto. Mesma tipografia, mesmo easing e mesma
   personalidade em todas as cenas.
4. **Precisão GSAP** (motion-style §8.1–§8.4, §8.11–§8.13): primeiro tween em `fromTo`; tweens seguintes
   da mesma propriedade com `immediateRender: false`; `autoRound: false` em `strokeDashoffset`; timelines
   pausadas registradas depois dos tweens; partículas por PRNG com semente fixa; cena = `<template>` com
   host, root e timeline de mesmo `id`; `fromTo`, nunca `from`; fontes resolvíveis.
5. **Identidade, mídia e ousadia** (motion-style §7 e §9):
   - decoração vetorial no vocabulário do logo (mesmo traço, espessura, abstração e paleta); asset externo
     entra quando parece da própria marca, com licença comercial livre, fundo removido e crédito em
     `CREDITOS.md`;
   - fotos recortadas (`object-position`) para o assunto do texto; logo em disco neutro sobre fundos
     coloridos; `data-motion-blur` nos movers rápidos;
   - social nasce ousado: objetos que batem e voam, transições com causa, springs com overshoot visível.
6. **Modos** (mídia em `midia.md` — leia antes):
   - **Modo A:** `limpo.mp4` como base, **um `<video class="clip">` por corte** (com `data-media-start`),
     `playsinline` e `data-has-audio="true"` quando o arquivo tem som. Por cima: legenda palavra por
     palavra, título de abertura, lower third, ênfases e transições suaves.
   - **Modo B:** cada cena do storyboard vira um bloco, com timing sincronizado à narração ou à música.
   - **Modo C:** trechos de `limpo.mp4` como clips na trilha principal (regras do modo A) + cenas de motion
     em tela cheia nos pontos marcados no `plano.md`, com transição de ida e volta. Voz contínua por baixo
     quando fizer sentido; mesma identidade em tudo.
7. **Uma ideia por cena**, com 2 ou 3 elementos animando em cada momento. Corte ou mudança de
   enquadramento a cada 3–4 s.

Gate: `npx hyperframes lint` sem erro. Sem isso, não vá para a verificação.

## Etapa 6 — Verificação

Carregue `hyperframes-cli` (check, snapshot, preview) e releia `robustez.md` como checklist.

**Verificação com evidência (`robustez.md`):** registre o sistema de layout no `plano.md` §3 antes das
cenas, olhe o frame final de cada cena e liste os defeitos (ou a ausência deles); sem visão, use medidas
do DOM e peça a conferência visual ao usuário, dizendo isso na entrega. Defeito que se repete em várias
cenas é do sistema — corrija a causa comum.

**Barra de aceitação — fecha inteira antes de mostrar qualquer versão:** texto exato do cliente (e todo
texto novo com leitura recalculada e cues reposicionados), decoração no vocabulário do logo e sem
retângulo de fundo atrás de arte, fotos recortadas para o assunto, logo lida com folga no seu fundo,
movimento ousado onde a receita pede, contraste AA (≥3:1 em texto grande, ≥4,5:1 em texto pequeno) e
sincronia nos cues. Frame 0 mostra o gancho (arte, produto ou linha), nunca uma tela vazia.

**Checklist do formato** (`templates-gravacao.md`) — rode e relate item a item:

- Gancho nos 3 primeiros segundos (2 s no Short) com texto na tela, falando no primeiro segundo.
- Corte ou mudança de enquadramento a cada 3–4 s.
- Legenda embutida; capa com a promessa em até 6 palavras.
- Uma única chamada, coerente com o formato (Reels: enviar/palavra-chave/direct; Shorts: seguir ou assistir ao completo; Stories: botão de mensagem ou link).
- Termos de busca do cliente na fala, no texto da tela e na legenda.
- Sem marca d'água de outra plataforma, sem bordas, áudio claro e nada de tela só de texto.
- Stories: 5–7 telas de 7–15 s, ao menos uma interação por sequência e instrução clara na última.
- Shorts: fechamento em loop, título/descrição com o termo de busca e uma ou duas hashtags relevantes + #Shorts.

1. Rode `npx hyperframes check --snapshots` (lint + runtime + layout + motion + contraste + craft, com
   frames gerais e um crop por achado) e leve a zero os erros; revise cada aviso um a um. O `npm run
   check` do projeto criado com `init` aponta para esse comando.
2. **Olhe o filme inteiro de uma vez:** `npx hyperframes snapshot --review` gera a folha de batidas, as
   tiras de emenda (0,2 s em volta de cada corte) e a folha em tamanho de celular — leia as imagens.
   Reserve o snapshot triplo (`snapshot --at`, 0,2 s antes / meio / depois) para animações **novas ou
   suspeitas**: três instantes por animação em 20 cenas são 60 imagens e não escala.
3. Rode a checklist de qualidade do `motion-style.md` §10 e relate o que verificou, incluindo:
   legibilidade na folha de celular (`review-phone.jpg`, 360 px), colisão com a faixa da legenda
   (`check --caption-zone "x0=0;y0=.78;x1=1;y1=1;severity=error"`) e, onde houver intenção de movimento
   declarada, o sidecar `*.motion.json` (`appearsBy`, `before`, `staysInFrame`, `keepsMoving`) — é o que
   transforma "nasceu no cue" em verificação automática.
4. **Frame 0:** o `check` audita o frame 0 do `index.html`. Se todo o conteúdo vem de cenas montadas, ele
   pode acusar `first_frame_empty` mesmo com a cena visível no snapshot — nesse caso ponha o gancho (ou
   um elemento visível) no próprio `index.html` no instante 0, ou registre o aviso como conhecido no
   relato. Não ignore: o frame 0 é a capa no feed.
5. **Repita até a lista sair vazia.** O preview e o render são a etapa seguinte, não esta.

Gate: `check` sem erro, folha olhada, defeitos listados (ou ausência declarada). **Sem render ainda.**

## Etapa 7 — Mixagem e render

Carregue `hyperframes-cli` (render, preview) e, se a mixagem pedir tratamento de faixa, a referência de
mixagem do `media-use`.

1. **Mixagem:** normalização em duas passadas com FFmpeg: a primeira mede (`loudnorm=...:print_format=summary`),
   a segunda aplica com os valores medidos (alvo ≈ −14 LUFS, teto −1,5 dBTP, `LRA=9`). Confira com
   `ffprobe`/`loudnorm` antes de entregar. Voz na frente, música baixa, fades nas emendas.
2. **Preview é a superfície de revisão:** abra `npx hyperframes preview --background`, confirme que a URL
   responde e mostre. O projeto fica editável ali (ou no app desktop).
3. **Render:** `npx hyperframes render --quality delivery` (use `--quality draft` enquanto itera; `looks`
   é o primeiro encode bom). Renderize depois do `check` limpo e do preview mostrado — ou quando o
   cliente pedir o arquivo direto.
4. **Conferência:** `ffprobe` no MP4 — vídeo e trilha de áudio presentes (quando houver áudio) e duração
   igual ao `data-duration` da raiz. Informe onde o MP4 ficou.
5. **Confira o áudio contra o roteiro:** `olv-confere renders/final.mp4 --roteiro roteiro.txt` transcreve o
   MP4 e compara palavra por palavra com o texto aprovado (troca, falta, sobra e percentual). É o que pega
   o TTS que comeu uma palavra e o corte que engoliu meia frase — leia a lista mesmo quando passar.
6. **Stories:** um MP4 por tela (`render -c compositions/story-01.html -o renders/story-01.mp4`) e o master
   só para revisão. A nota de stickers acompanha a entrega.

## Etapa 8 — Entrega

1. Liste os arquivos gerados e explique como pedir ajustes (ex.: "título maior", "trocar a cor", "tirar
   tal corte", "refazer a cena 3").
2. **Relato honesto** (`robustez.md` §8): o que foi verificado e como, e o que **não** foi.
3. **Feche com o pós-publicação do formato** (`templates-gravacao.md`): comentário fixado com informação
   complementar, resposta a todos os comentários na primeira hora e compartilhamento nos Stories no mesmo
   dia; no Shorts, título/descrição com o termo de busca, #Shorts e comentário fixado com o link do vídeo
   longo; no Stories, Destaques (Quem sou, Como funciona, Resultados, Dúvidas).
4. Atualize o `plano.md` §1 (estado) e §9 (verificação) — é o que permite retomar o projeto sem depender
   do histórico da conversa.

## Regras

- Um tema por vídeo e sempre dentro do mesmo nicho; o formato social é decidido antes do roteiro — fora
  dos templates, a estrutura fica no `plano.md`.
- Nenhuma dependência, venv, modelo ou cache entra na pasta do projeto: ferramentas ficam em
  `~/.olv-studio` e o projeto guarda só os arquivos do vídeo.
- Peça aprovação antes de qualquer decisão que mude o conteúdo (principalmente cortes e roteiro).
- Se um comando falhar, mostre o erro e corrija antes de seguir.
- Se o usuário trouxer um prompt ou skill de terceiros como referência, leia por inteiro e avise antes de
  executar qualquer comando que ele contenha.
- Quando o comando pedir atualização de skills do HyperFrames (`npx hyperframes skills update`), passe a
  instrução ao usuário — a atualização é o passo dele.
