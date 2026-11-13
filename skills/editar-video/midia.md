# Mídia e áudio — as regras que quebram o render

Este arquivo existe por um motivo prático: quase todo defeito grave de vídeo aparece **na
declaração da mídia**, não na animação. Um `<video>` sem `muted`, um `<audio>` sem `id` ou um
`data-media-start` errado fazem o lint falhar ou o render sair sem som — e o sintoma (tela preta,
filme silencioso) não aponta para a causa.

Leia isto **antes** de escrever a primeira cena dos modos A e C (`SKILL.md`, "Construção da
composição"), e antes de qualquer mixagem.

## 1. O que todo clip de mídia carrega

| Atributo | Para quê | Obrigatório quando |
|---|---|---|
| `id` | a mídia é referenciável (e o `check` a nomeia nos achados) | sempre em `<audio>` (`media_missing_id`) |
| `class="clip"` | entra na timeline, ganha `data-start`/`data-duration` | toda mídia cronometrada |
| `data-start`, `data-duration` | janela do clip no filme (segundos, locais da composição) | sempre — `data-start` é o tempo real, nunca um 0 silencioso |
| `data-track-index` | faixa no Studio (é só organização; a ordem de pintura é o `z-index`) | sempre que houver mais de uma faixa |
| `data-media-start` | recorte dentro do arquivo (o "in" do corte) | todo corte que não começa no 0 do arquivo |
| `data-playback-rate` | velocidade constante (0,1–10) | só com speed ramp |
| `data-has-audio="true"` | o vídeo mantém o próprio som | vídeo com som |
| `muted` | vídeo sem som | vídeo mudo, gravação de tela, b-roll |
| `playsinline` | necessário no mobile/WebKit | todo `<video>` |
| `data-volume` | ganho (1 = 0 dB; até 3,98 = +12 dB) | áudio que não é voz em primeiro plano |
| `data-fade-in` / `data-fade-out` | fade de borda em segundos | entrada/saída de música e ambiente |

**`data-duration` de áudio nunca passa do arquivo.** Se o slot for maior que o MP3, o runtime encurta o
clip no render e avisa `clip_media_fit`; o silêncio que você queria fica fora do áudio, na cena. Use a
duração real do arquivo (`ffprobe -show_entries format=duration`) no clip de áudio e deixe a cena mais longa.

**Mídia entra dentro do root da composição.** Em `compositions/*.html`, um `<audio>`/`<video>` colocado
antes do `<div id="...">` raiz vira o "root" do template e o lint falha com `root_missing_composition_id`
(verificado). Coloque a mídia **dentro** do root, como qualquer outro filho.

**`data-start` de mídia aninhada é local à composição** — o aviso
`nested_media_start_basis_ambiguous` só lembra disso. Dentro de uma cena, o tempo conta de 0 na cena; na
raiz, conta do filme.

**O lint não perdoa:** um `<video>` cronometrado sem `data-has-audio` nem `muted` falha
(`video_missing_muted`); um `<audio>` sem `id` falha (`media_missing_id`); um `<video>`
cronometrado dentro de outro elemento cronometrado falha (`video_nested_in_timed_element`) — o
tempo vai no `<video>` **ou** no wrapper, nunca nos dois.

## 2. Modo A e C — montar os cortes do vídeo gravado

Os cortes vêm de três fontes: a transcrição, o `silencedetect` e `npx hyperframes measure cuts
<video>` (que pega jump cut e punch-in dentro do mesmo take). Aprovada a lista de cortes
(`SKILL.md`, etapa 4), cada corte vira **um `<video>`** — nunca um arquivo por corte, nunca um
`<video>` único com `data-media-start` variando por keyframe:

```html
<!-- index.html — modo A: limpo.mp4 em 2 cortes + trilha por baixo -->
<div id="root" data-composition-id="main" data-start="0" data-duration="22"
     data-width="1080" data-height="1920">

  <!-- 0 → 12,4 s do filme, do 0 s do arquivo -->
  <video id="corte1" class="clip" src="assets/video/limpo.mp4"
         data-start="0" data-duration="12.4" data-media-start="0"
         data-track-index="0" playsinline data-has-audio="true"></video>

  <!-- 12,4 → 22 s do filme, a partir de 18,2 s do arquivo -->
  <video id="corte2" class="clip" src="assets/video/limpo.mp4"
         data-start="12.4" data-duration="9.6" data-media-start="18.2"
         data-track-index="0" playsinline data-has-audio="true"></video>

  <!-- música por baixo da voz, baixa e com fades -->
  <audio id="trilha" class="clip" src="assets/audio/trilha.mp3"
         data-start="0" data-duration="22" data-volume="0.18"
         data-fade-in="0.6" data-fade-out="1.2"></audio>
</div>
```

Regras que evitam as três falhas mais comuns:

- **Vídeo sem trilha de áudio** (gravação de tela, stock mudo, cutout) leva `muted`, não
  `data-has-audio="true"` — senão o `check` reprova com `audio_source_rejected` e o render para.
- **Legenda e motion ficam depois do vídeo** na ordem de pintura (`z-index`), nunca dependendo
  da faixa.
- **Recorte de vídeo e de áudio do mesmo arquivo** (o "detach" do Studio) usa `data-link` +
  `data-sync-origin` com `data-start`, `data-duration`, `data-media-start` e
  `data-playback-rate` **idênticos** nos dois; mover um sem o outro dessincroniza.

## 3. Áudio que o `check` audita sozinho

| Achado | Significado | O que fazer |
|---|---|---|
| `audio_source_rejected` (erro) | o arquivo não tem trilha de áudio | trocar o arquivo ou marcar `muted` |
| `audio_source_unreadable` (erro) | o arquivo não abre como áudio | reexportar |
| `audio_src_not_found` (erro) | caminho errado | corrigir o `src` (sempre relativo ao projeto) |
| `audio_starts_past_source_end` (aviso) | `data-media-start` além do fim do arquivo | baixar o valor |
| `audio_clip_silent` (aviso) | aquele trecho do arquivo é mudo | mover o `data-media-start` ou trocar o trecho |
| `film_silent` (aviso) | filme > 15 s sem nenhum áudio audível | adicionar trilha/voz ou aceitar silêncio de propósito |
| `audio_none` (info) | nenhum clip toca áudio | ok se o vídeo é mudo por decisão |

Mídia remota nunca é baixada no render: **todo `src` é um arquivo local** dentro de `assets/`.

## 4. Voz, música e efeitos

- **Trilha:** a biblioteca do estúdio (`musica.md`) — `olv-musica listar` escolhe por bpm/LRA e
  `olv-musica usar` copia para o projeto com o `<audio>` pronto e o crédito.
- **B-roll de banco:** quando a fala pede uma imagem que não existe no material, busque pelo **assunto da
  frase** (não pela palavra solta), baixe com licença livre (Pexels API, Openverse) e registre o crédito.
  Ajuste a cor para a imagem conversar com o resto do filme.
- **De onde vem (SFX e imagem):** `media-use` resolve SFX do pacote local (21 sons, sem login) e música/imagem/voz pelo
  catálogo HeyGen (login grátis) ou pelo arquivo do cliente. O arquivo cai em `.media/` com um
  `manifest.jsonl`; referencie esse caminho local (`.media/audio/sfx/sfx_001.mp3`) ou mova para `assets/` —
  o contrato é só um: `src` local, nunca remoto.
- **Voz é a protagonista.** Música entra em `data-volume` baixo (≈ 0,12–0,22) e com fades; não
  compita com a fala. Para abaixar a música sob a voz, `sidechaincompress` (FFmpeg) na mixagem
  final ou automação de volume por trecho.
- **Efeitos nascem no cue.** Hit ≤ 1 quadro de folga do corte; whoosh amarrado ao movimento;
  riser terminando no evento. SFX solto no tempo vira ruído.
- **Mixagem final em duas passadas** (`loudnorm` medindo e depois aplicando): alvo ≈ −14 LUFS,
  teto −1,5 dBTP, `LRA=9` — é o padrão de plataforma social. O `npx hyperframes normalize-audio`
  (padrão −16 LUFS, `--lufs=-14` para alinhar) serve para equalizar **uma faixa**; a normalização
  do filme inteiro é a do `SKILL.md`.
- **Trilha longa não é trilha.** Música que atravessa o vídeo inteiro precisa de um corte ou de
  uma respiração a cada 8–15 s; senão o áudio "achata" mesmo com a imagem animada.

## 5. Beatmap (só quando existe música)

`npx hyperframes beats` precisa de **uma trilha local na composição marcada como música**:

```html
<audio id="trilha" src="assets/audio/trilha.mp3" data-timeline-role="music"></audio>
```

(`id` contendo `music`, `bgm` ou `soundtrack` também é reconhecido.) Sem isso o comando não
encontra a faixa e não escreve `beats/<caminho>.json`. Ele devolve `bpm` e `beatTimes`, **não**
downbeats: derive a fase do compasso pela energia da banda grave e alinhe as viradas de cena a
múltiplos inteiros de compasso. Para analisar um arquivo avulso, `npx hyperframes beats
music.mp3 --json` — nesse modo ele só imprime, não grava nada.

## 6. Vídeo gravado: rosto, recorte e print

Três recursos separam uma edição de footage amador de uma profissional — e os três dependem de medir, não
de chutar posição.

**Rosto: o texto nunca passa na frente.** Meça a caixa do rosto por quadro e use-a para decidir onde o
texto pode ficar:

```bash
npx hyperframes measure face <video> --json
```

Ele devolve `boxes` (x, y, w, h como fração do quadro) por amostra e `face_height`. Regra prática: herói e
apoio ficam **acima ou abaixo** da caixa do rosto, nunca cruzando; lower third entra na altura do ombro,
não do queixo. Se o rosto se move na cena, o texto se move com ele — ou sai do caminho.

**Recorte sem chroma key.** `npx hyperframes remove-background` (skill `media-use`) tira a pessoa do fundo.
Com o recorte por cima, o texto pode passar **atrás** dela — é o efeito que dá profundidade a um vídeo
falado. O `check` trata o recorte como opaco: marque o elemento com `data-layout-allow-occlusion` e julge
no snapshot, não no relatório.

**Print como objeto.** Print de tela, página ou slide entra na cena com perspectiva, sombra e um leve
movimento de câmera — não como imagem colada. Para destacar uma palavra dentro do print, meça a caixa do
texto no print e posicione o destaque nela; é o que faz o olho achar o ponto certo em um segundo.

**Rastrear um objeto.** Para grudar etiqueta, preço ou legenda em algo que se move, meça a posição do
ponto em quadros-chave e faça o tween entre eles (mesmo easing do movimento). Movimento estimado "a olho"
deriva em dois segundos.

## 7. Ordem: mídia antes de cena

1. Todos os arquivos chegam em `assets/` (voz, música, SFX, imagens, vídeo) e abrem localmente.
2. Só então as cenas são escritas com os `data-*` acima.
3. Só depois de `check` limpo existe mixagem e render.

Escrever cena com `src` provisório, ou mixar antes de a última cena entrar, é o caminho mais
curto para refazer tudo: o `check` mede o filme que existe, não o que você pretende montar.
