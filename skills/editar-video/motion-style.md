# Guia de Motion Style

Consulte este arquivo antes de criar qualquer animação. O objetivo é um visual moderno, limpo e consistente, sem exagero. Este guia é o padrão do estúdio: vocabulário, ritmo, layout em zonas, receitas de tela e as regras técnicas de GSAP que mantêm cada animação fiel ao que foi escrito.

## 1. Princípios

1. **Hierarquia primeiro.** Em cada momento, um elemento é o protagonista. Os demais entram depois, em seus próprios momentos, ou ficam discretos.
2. **Movimento com propósito.** Toda animação guia o olhar, enfatiza uma ideia ou marca uma transição — o motivo de tela (uma linha de batimento, um contador, um card) dá o contexto.
3. **Entradas com presença, saídas mais curtas.** A entrada tem mais presença que a saída (saída com 40–50% da duração da entrada).
4. **Consistência.** Mesmo easing, mesmas durações e mesma "personalidade" de movimento em todo o vídeo, usando as receitas da §7.
5. **Respiro.** Deixe o conteúdo parado tempo suficiente para ser lido: pelo menos ~0,3 s por palavra de texto de tela; títulos curtos ficam no mínimo 1 s em cena e a última linha do vídeo, no mínimo 2 s.
6. **Menos é mais.** Uma ideia por cena, com 2 ou 3 elementos animando em cada momento.

## 2. Vocabulário de motion (com o equivalente em GSAP)

| Técnica | O que é | Exemplo em GSAP |
|---|---|---|
| Fade + slide | Aparece subindo ou deslizando poucos pixels | `fromTo(el, {opacity:0, y:30}, {opacity:1, y:0})` |
| Easing de saída suave | Entrada que desacelera e acomoda | `ease: "power3.out"`, `"expo.out"` |
| Overshoot / back | Passa um pouco do ponto e volta, dá "vida" | `ease: "back.out(1.4)"` a `"back.out(1.7)"` |
| Stagger | Elementos entram em sequência | `stagger: 0.06` a `0.1` (palavras 0.08, letras ~0.03) |
| Texto cinético | Palavras ou letras entrando no ritmo da fala | dividir o texto em spans + stagger |
| Blur-in por palavra | Palavra desfocada que ganha foco ao entrar | `filter: "blur(6px)" → "blur(0px)"`, 0.16 s |
| Mask reveal | Texto ou forma revelados por máscara | animar `clipPath` |
| Count-up | Número subindo até o valor final | animar um objeto numérico e escrever no `onUpdate` |
| Line draw | Linha ou ícone SVG se desenhando | animar `strokeDashoffset` com `autoRound: false` |
| Traço de ênfase | Barra coral que se desenha sob a palavra-chave | `scaleX: 0 → 1`, `transformOrigin: "left center"` |
| Split + tremor | Micro-impacto de 2–4 quadros no cue de áudio | `textShadow` coral/branco pulsado + `x` com `steps(3)` |
| Count-up + trilho | Número e barra de progresso preenchendo juntos | dois `fromTo` no mesmo passe e mesmo easing |
| Escala com ancoragem | Cresce a partir de um ponto | `transformOrigin` + `scale` |
| Parallax | Camadas em velocidades diferentes | tweens com durações e distâncias distintas |
| Morph / transformação | Uma forma vira outra | animar `border-radius`, `d` do path (com plugin) |
| Antecipação | Recuo pequeno antes do movimento principal | tween de 2 fases |
| Follow-through | Acomodação depois de parar | tween curto final com `back` ou `elastic` leve |
| Overlap | Animações que começam antes da anterior terminar | posições relativas na timeline (`"-=0.2"`) |
| Câmera falsa | Zoom/pan lento sobre um bloco | `scale` 1 → 1.05 durante a cena toda |
| Transições | Wipe, zoom-through, flash branco, whip, shader | blocos do catálogo (`npx hyperframes add ...`) |

## 3. Tempos de referência

| Tipo | Duração |
|---|---|
| Micro-interação (ícone, destaque de palavra) | 0,15 a 0,3 s |
| Entrada de texto ou card | 0,4 a 0,7 s |
| Transição entre cenas | 0,4 a 0,8 s |
| Entrada de título de abertura | 0,6 a 1,0 s |
| Intervalo de stagger | 0,05 a 0,1 s por item (letras ~0,03 s) |
| Cena de motion em tela cheia (modo C) | 3 a 8 s |
| Saída de texto | 0,13 a 0,25 s |

Use durações e easings **iguais** para elementos do mesmo tipo.

## 4. Guia de estilo (preencher por projeto)

Se o usuário não tiver um estilo, proponha um deste modelo e peça aprovação. Depois use sempre como variáveis CSS (`:root`).

```
Cores:     fundo [#...]   texto [#...]   destaque [#...]   secundária [#...]
Fonte:     títulos [...]   corpo [...]   (máx. 2 famílias)
Tamanhos:  título [..px]   subtítulo [..px]   legenda [..px]   (legível em celular)
Cantos:    [0 / 8 / 16px / pílula]
Sombras e brilho: [nenhum / sutil / neon]
Personalidade: [calma e elegante / dinâmica e enérgica / técnica e limpa]
Easing padrão: [power3.out]     Easing de destaque: [back.out(1.4)]
Duração padrão de entrada: [0.5s]
```

Sugestões de personalidade:

- **Limpo e moderno:** fundo escuro ou off-white, 1 cor de destaque, tipografia grande, `power3.out`, pouco overshoot.
- **Dinâmico (Reels/Shorts):** cortes rápidos, texto grande no centro, `back.out`, stagger curto, legendas com destaque na palavra falada.
- **Técnico/produto:** grid sutil, cards, linhas se desenhando, números com count-up, easing seco (`expo.out`).

## 5. Legendas animadas

- Máximo de 2 linhas, 3 a 6 palavras por vez (modo curto) ou frase completa com palavra ativa destacada.
- Palavra ativa muda de cor ou escala levemente (+5 a 10%), sem pular o layout.
- Contraste alto com o fundo (fundo semitransparente ou contorno, quando necessário).
- Margens seguras respeitadas: em 9:16, conteúdo na faixa central, longe do topo e do rodapé onde as plataformas colocam interface.
- Sincronia com os timestamps por palavra da transcrição, já ajustados aos cortes.

## 6. Layout em zonas (9:16 e 16:9)

O layout nasce sem sobreposição quando cada conteúdo tem sua zona:

1. **Divida a tela em zonas verticais** — herói (título ou número), apoio (linha de suporte), dados (gráfico, card, lista) e selo (badge, CTA) — com um protagonista por zona.
2. **Empilhe as zonas com flexbox em coluna** e folgas de 40–70 px entre elas. Elementos absolutos ficam só nos decorativos.
3. **Medidas de tipografia:** herói entre 4 e 9% da altura do frame, apoio entre 2,5 e 4%, no máximo duas linhas por bloco; texto-chave dentro da caixa de 80% (864 px em 1080 de largura).
4. **Ancore os decorativos na própria zona** — partículas centradas no selo, linha de motivo abaixo da frase, grid no fundo — e marque-os com `data-layout-ignore`.
5. **Feche com snapshot no meio da cena:** cada zona mostra seu protagonista com respiro ao redor. O `npm run check` valida overflow, sobreposição, contraste e erros de runtime; respiro e composição você confere nos próprios snapshots.

## 7. Receitas de tela (use uma por cena, repetindo no vídeo inteiro)

| Tela | Composição | Movimento |
|---|---|---|
| **Pergunta / problema** | frase em 2 linhas, palavra-chave em destaque com traço desenhado, motivo gráfico de apoio abaixo | palavras em blur-in (0,16 s, 0,08 s de intervalo), overshoot na palavra-chave, split + tremor de 3 quadros no cue do SFX, saída blur-out 0,22 s |
| **Número / estatística** | numeral grande com símbolo sobrescrito, apoio, trilho de progresso, gráfico em card, selo de recompensa | count-up e trilho no mesmo passe, barras em stagger na batida, selo com spring pop + partículas, micro-overshoot quando o número trava |
| **Lista / checklist** | card com cabeçalho e contador, itens com ícone | check desenhado item a item em cada batida, contador acompanhando um passo por item |
| **Produto / fotos** | cards grandes em leque sobreposto (rotações ±6–10°, sombra profunda), foto herói central; nas viradas, um objeto em tela vira o mundo (card ou produto cresce através da câmera) | entradas que batem nas batidas (spring `back.out(1.7)` + `data-motion-blur`), herói por último; transição com causa: o objeto cresce/sai através da câmera e a cena seguinte pousa do mesmo movimento |
| **Editorial / tipografia** | tipografia como imagem: uma linha grande por bloco, contraste serifada 900 × caixa alta com tracking, muito respiro; arte ou cor cheia em uma das metades | revelação por máscara de baixo para cima, palavra-chave com traço ou preenchimento de tinta, entrada letra a letra; um evento por vez, frame 0 já com o gancho |
| **Encerramento / CTA** | símbolo da marca, linha de ação, apoio | line draw do símbolo, CTA com overshoot + pop, glow no kick, impacto em downbeat e fade natural de ~1,5 s |

Cada cena que repete a receita reforça a identidade do vídeo. **Duas ou três transições** cobrem o filme inteiro (ex.: whoosh-wipe nas viradas de cena, flash nas viradas de energia, dissolve no encerramento).

## 8. Regras técnicas (GSAP + Hyperframes)

1. **Determinismo total:** timelines GSAP pausadas e registradas depois dos tweens; partículas e variações por PRNG com semente fixa; tudo como função do tempo da timeline.
2. **Estados pré-animados com precisão:** o primeiro tween de cada elemento é um `fromTo` padrão, cujo estado `from` define como o elemento está antes do cue (escondido, escala 0, traço por desenhar). Os tweens seguintes da mesma propriedade levam `immediateRender: false` — assim cada elemento nasce parado e aparece exatamente no seu cue.
3. **Line draw que desenha:** todo tween de `strokeDashoffset` leva `autoRound: false`; com `pathLength="1"`, o arredondamento padrão do GSAP faz o traço pular de 0 a 100%. Confira o desenho num snapshot no meio do draw.
4. **Sincronia primeiro:** antes de escrever a cena, abra o beatmap/eventos e mapeie cue → elemento (mesmo segundo). Sem beatmap, use `npx hyperframes beats` (`bpm` + `beatTimes`; downbeats você deriva pela fase do kick). Cada entrada nasce no cue do SFX correspondente.
5. Fontes e mídias locais quando possível, para o render ser reproduzível.
6. **Movers rápidos** levam `data-motion-blur="on"` na raiz da composição (ou `="off"` num nó que já traz o próprio blur) — entrada de cards, objetos que voam através da câmera, chicotes.
7. **Mudança de texto re-temporiza tudo:** cada copy novo recalcula a leitura (0,5 s + 0,3 s por palavra; última linha com no mínimo 2 s) e reposiciona entradas, saídas e pops nos cues do beatmap.
8. **Assets decorativos nascem prontos:** arte com fundo de papel ou scan vira PNG transparente (cor ou luminância removida); licença de uso comercial livre e créditos registrados num `CREDITOS.md` junto dos arquivos. Texturas e fundos intencionais ficam como estão.
9. Comandos do HyperFrames: `npm run check` depois de cada edição; snapshots nos três instantes de cada animação nova; render só depois da verificação.
10. **Mecânica bespoke com caixa herdada** (troca de caractere por gráfico): um glifo-fantasma com `visibility: hidden` fixa a caixa natural do caractere (largura, altura e baseline vêm da métrica da fonte) — as letras vizinhas nunca se movem; caixa sem glifo usa um span com largura e altura fixas como fantasma. A máscara é `overflow: hidden` nessa caixa; a letra sai e o gráfico sobe dentro dela (ou gira em Y), por 8–12 quadros a 30 fps (≈0,27–0,4 s); o gráfico segura 0,6–1,2 s com um micro-gesto e devolve a letra. Verificação: comparar a posição das letras vizinhas em três snapshots (antes, meio, depois) — diferença de 0 px.

## 9. Padrões de decisão

| Situação | Padrão |
|---|---|
| Cena com vários elementos | Um protagonista + 2 ou 3 elementos em movimento; os demais entram em momentos próprios |
| Entradas | Easing com desaceleração (`power3.out`, `expo.out`, `power4.out`); linear reservado a rotação e velocidade constante |
| Tamanho de texto | Legível em celular: títulos 4–9% da altura, apoio ≥ 2,5% |
| Paleta | Duas famílias de fonte, uma cor de destaque e neutros da paleta |
| Glitch, tremor e zoom | Amarrados a um evento — um cue de áudio, uma quebra de ritmo, uma virada — com o motivo de tela dando contexto |
| Transições | Duas ou três escolhidas, repetidas nas mesmas viradas; sempre que possível com causa em cena (um objeto que cresce ou voa através da câmera) |
| Saída de texto | Respiro de ~0,3 s por palavra lida antes da saída, que leva 0,13–0,25 s |
| Decoração e ilustração | O vocabulário decorativo nasce do próprio logo: mesmo traço, espessura, grau de abstração e paleta — confira lado a lado num frame. Vetores próprios (SVG no traço da marca) superam arte importada; asset externo entra quando, comparado ao logo, parecer da mesma mão |
| Recorte de foto | `object-position` escolhido para o assunto do texto ao lado — o close mostra aquilo que a fala nomeia |
| Logo sobre fundo colorido | A logo assenta num disco ou moldura neutra (cor de papel) que preserva suas cores exatas e garante leitura |
| Social / feed | Movimento ousado por padrão: tipografia grande, objetos que batem e voam, transições com causa e springs com overshoot visível |

## 10. Checklist de qualidade (rodar no preview e nos snapshots)

- [ ] Frame 0 mostra o gancho (arte, produto ou linha), nunca uma tela vazia
- [ ] Cada animação conferida em três instantes — 0,2 s antes do cue, meio da tween e logo após o fim — nos snapshots
- [ ] Cada elemento nasce e termina dentro das margens seguras, um protagonista por zona, sem textos sobrepostos
- [ ] Mecânicas bespoke conferidas: caixa do swap colada ao glifo e vizinhas na mesma posição (±0 px) antes/durante/depois
- [ ] Texto legível em tela de celular, com tempo de leitura respeitado (inclusive textos revisados: recalcular sempre; última linha ≥ 2 s)
- [ ] Contraste AA: ≥ 3:1 em texto grande e ≥ 4,5:1 em texto pequeno (o `npm run check` mede)
- [ ] Entradas importantes nascem exatamente nos cues do beatmap/SFX (≤ 1 frame de folga)
- [ ] Traços e máscaras desenham progressivamente nos snapshots
- [ ] Decoração no vocabulário do logo e sem retângulo de fundo atrás de arte
- [ ] Cada foto recortada para o assunto do texto e a logo lida com folga no seu fundo
- [ ] Cores, fontes, easings e durações iguais para elementos do mesmo tipo
- [ ] Duas ou três transições, suaves e repetidas nas mesmas viradas
- [ ] Áudio com fade nas emendas e mix normalizado (≈ −14 LUFS, teto −1,5 dBTP) — conferido no MP4 final
- [ ] `npm run check` sem erros, avisos revisados um a um, e render concluído
