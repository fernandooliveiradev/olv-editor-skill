# plano.md — esqueleto do projeto

Copie este arquivo para a raiz do projeto como `plano.md` e preencha **na ordem das etapas**. Ele é a
memória do vídeo: o que foi decidido, com que números, o que já foi aprovado e o que falta. Se o
processo for interrompido, é daqui que se retoma — não do histórico da conversa.

Não deixe seção vazia nem `<...>` para trás: campo sem resposta é decisão não tomada, e decisão não
tomada vira retrabalho na etapa 5.

---

## 0. Cabeçalho

| Campo | Valor |
|---|---|
| Projeto | `<nome-do-projeto>` |
| Formato | Reels / Stories / Shorts / livre (16:9) |
| Modo | A (vídeo gravado + motions) / B (motion puro) / C (híbrido) |
| Duração alvo | `<s>` (dentro da faixa do formato) |
| Objetivo | alcance / autoridade / venda / relacionamento |
| Público | `<nicho + quem é>` |
| Dor nomeada no gancho | "<palavra que o cliente usa>" |
| Chamada única | `<enviar / palavra-chave / direct / botão / seguir>` |
| Voz | gravação própria / TTS `<voz>` / sem voz |
| Data de entrega | `<AAAA-MM-DD>` |

## 1. Estado (atualize a cada etapa — é o retomar)

- [ ] 1. Briefing respondido e formato escolhido
- [ ] 2. Roteiro **aprovado** pelo cliente
- [ ] 3. Ativos em `assets/` (voz, música, SFX, imagens, vídeo) e abrindo localmente
- [ ] 4. Cues e beatmap travados
- [ ] 5. Cenas escritas
- [ ] 6. `check` limpo, folha de revisão olhada
- [ ] 7. Mixagem e render conferidos
- [ ] 8. Entrega e pós-publicação entregues

## 2. Estilo (tokens — viram `:root` no CSS)

```
fundo:        #......
texto:        #......
destaque:     #......
secundária:   #......
título:       <fonte empacotada ou @font-face>
corpo:        <fonte>
título:  <px>   apoio: <px>   legenda: <px>   (mín. 2,6% da altura do frame)
cantos: <0|8|16|pílula>    sombra: <nenhuma|sutil|neon>
personalidade: <calma|dinâmica|técnica>
easing padrão: <power3.out>    destaque: <back.out(1.4)>
```

## 3. Sistema de layout (números, em px de 1080×1920)

| Zona | Faixa em y | Regra |
|---|---|---|
| Interface da plataforma (topo) | `0 – <220>` | nada essencial |
| Herói (título/número) | `<220 – 760>` | 4–9% da altura |
| Apoio | `<760 – 1000>` | ≥ 2,5% da altura, ≤ 2 linhas |
| Dados (card/gráfico/lista) | `<1000 – 1290>` | um protagonista |
| Legenda | `<1300 – 1560>` | nada da cena invade |
| Interface da plataforma (rodapé) | `<1560 – 1920>` | nada essencial |

Eixo: `<centro x=540 | assimétrico x=...>`. Margem lateral: `<60>`.
Desvios deste sistema: `<cena → motivo>`.

## 4. Roteiro (aprovado em `<data>`)

| Tempo | Bloco | Texto exato | Tela (o que aparece) |
|---|---|---|---|
| 0–3 | Gancho | "<frase literal>" | `<arte/linha>` |
| … | … | … | … |

Gancho tipo: problema / pergunta / contraste / erro comum.
Capa (≤ 6 palavras): "<...>". Termos de busca do cliente: `<...>`, `<...>`.
Prova (caso/número/antes-depois): `<de onde veio; se não houver, a frase não afirma nada>`.

## 5. Cues (etapa 4 — depois dos ativos)

| Cue (s) | Evento | Elemento que nasce | SFX/beat |
|---|---|---|---|
| `<0,00>` | corte 1 | `#s1-titulo` | whoosh |
| … | … | … | … |

Beatmap: `bpm=<...>`, fase do compasso `<...>`, arquivo `beats/<...>.json`.
Compensação: a legenda começa 0,1–0,3 s depois do corte, nunca em 0 exato.

## 6. Cortes (modos A e C — aprovados em `<data>`)

| # | Início–fim (bruto) | Duração | Texto | Motivo |
|---|---|---|---|---|
| 1 | `<00:03,2 – 00:07,8>` | 4,6 s | "<...>" | silêncio de 1,1 s + hesitação |
| … | … | … | … | … |

## 7. Cenas

| # | Bloco | Início–fim | Receita | Elementos | Animação | Cue |
|---|---|---|---|---|---|---|
| 1 | Gancho | 0–3,2 | pergunta | título 2 linhas, traço, motivo | blur-in + traço | 0,0 |
| … | … | … | … | … | … | … |

Receitas disponíveis em `receitas/` (pergunta, número, lista, produto, editorial, CTA) — copie a mais
próxima e adapte os tokens; não invente do zero quando a receita serve.

## 8. Decisões fora do padrão

| Decisão | Por quê | O que foi verificado depois |
|---|---|---|
| `<...>` | `<...>` | `<...>` |

## 9. Verificação (preencher na etapa 6)

- `check`: `<0 erros / N avisos revisados>` — o que era cada aviso
- Folha de revisão olhada: `<sim/não>` — defeitos vistos e corrigidos: `<lista>`
- Folha de celular (360 px): `<legível / ajustado>`
- Faixa da legenda: `<sem colisão>`
- O que **não** foi verificado: `<...>`

## 10. Entrega

MP4: `<caminho>` · `<durações e resolução conferidas com ffprobe>`
Pós-publicação do formato: `<comentário fixado / hashtags / destaques / link>`

---

## Exemplo preenchido (recorte)

```markdown
## 0. Cabeçalho
| Arquivo | 3 erros que custam cliente |
| Formato | Reels | Modo | B | Duração alvo | 38 s |
| Objetivo | autoridade | Público | dono de clínica pequena |
| Dor | "o paciente some depois do orçamento" | Chamada | direct com a palavra ORÇAMENTO |

## 5. Cues
| 0,00 | corte 1 | #s1-titulo | whoosh |
| 3,10 | corte 2 | #s2-numero | hit |

## 7. Cenas
| 1 | Gancho | 0–3,2 | pergunta | "o paciente some" + traço | blur-in 0,16 s, traço 0,3 s | 0,0 |
| 2 | Ideia | 3,2–11,0 | número | 68% + trilho | count-up 0,9 s | 3,10 |

## 9. Verificação
- check: 0 erros; 2 avisos (line_unread no card 3 → texto reduzido; dead_stretch 3,4 s → corte encurtado)
- folha olhada: sim; defeito visto: numeral encostava na margem inferior → zona de dados subiu 40 px
- não verificado: legibilidade em Android antigo (sem aparelho)
```
