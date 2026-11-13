# Receitas de tela — código de partida verificado

Seis cenas prontas, uma por tipo de tela do `motion-style.md` §7. Elas existem para acabar com a
variação de qualidade entre um vídeo e outro: em vez de o modelo redescobrir GSAP a cada cena, ele
copia a receita mais próxima, troca os tokens e o texto, e o `check` volta a medir só o que é do vídeo.

| Arquivo | Tela | O que já vem resolvido |
|---|---|---|
| `pergunta.html` | Pergunta / problema | palavras em blur-in, traço de ênfase desenhado, apoio, motivo gráfico |
| `numero.html` | Número / estatística | count-up determinístico, trilho no mesmo easing, micro-overshoot |
| `lista.html` | Lista / checklist | card, checks desenhados em `steps`, contador em degraus |
| `produto.html` | Produto / fotos | leque de fotos, herói com spring, `data-motion-blur`, câmera falsa |
| `editorial.html` | Editorial / tipografia | duas famílias, revelação por máscara, régua desenhada |
| `cta.html` | Encerramento / CTA | símbolo em line draw, CTA com overshoot e glow, fade longo |

## Como usar

1. Copie o arquivo para `compositions/` do projeto e renomeie o prefixo (`rp-`, `rn-`, `rl-`, `rp2-`,
   `re-`, `rc-`) para o prefixo da cena (`s3-`, por exemplo) — ids são únicos no filme inteiro.
2. Monte no `index.html` (host, root da cena e chave da timeline com o **mesmo** id):

```html
<div id="s3-pergunta" data-composition-id="s3-pergunta"
     data-composition-src="compositions/s3-pergunta.html"
     data-start="6.4" data-duration="4.5" data-track-index="1"
     data-width="1080" data-height="1920"></div>
```

3. Troque os tokens no `<style>` (`--ground`, `--ink`, `--accent`, `--muted`, `--font-display`) pelos do
   `plano.md` §2 e o texto pelo do roteiro aprovado. Nada além disso precisa mudar.
4. Rode `npx hyperframes lint` e depois `check --snapshots`.

## Contrato que as receitas seguem (e você deve manter)

- **`.clip` guarda o tempo; o filho anima.** Nenhuma receita anima `visibility`, `display` ou
  `autoAlpha` no elemento `.clip` — isso é erro de lint (`gsap_animates_clip_element`).
- **`fromTo`, nunca `from`**, dentro de cena.
- **Frame 0 nunca é tela vazia:** o gancho já está visível no instante 0; a entrada é um
  assentamento (deslocamento/blur/spring), não um `opacity: 0`.
- **Uma ideia por cena**, 2–3 elementos animando por momento, saída 40–50% da entrada.
- Fontes: as empacotadas e as do Google Fonts por nome; qualquer outra exige `@font-face`.

## O que foi verificado

Testadas no HyperFrames CLI 0.9.40 (portrait 1080×1920), montadas em sequência num filme de 28,5 s:

- `lint`: **0 erros, 0 avisos** nas seis.
- `check`: **0 erros** (lint, runtime, layout, motion, contraste).
- Achados esperados, ambos sem gravidade: um `info` de `container_overflow` em `editorial.html` no
  instante em que a linha sobe dentro da máscara (é o mecanismo da revelação) e o aviso
  `film_silent` no filme de teste, que não tem áudio.
- Folha de contato olhada: as seis telas leem em tamanho de celular.

> As receitas chamam `document.querySelector` uma vez por contador; se você montar a mesma receita duas
> vezes no filme, troque o seletor por `document.querySelector` escopado na cena para o contador não
> escrever no lugar errado.
