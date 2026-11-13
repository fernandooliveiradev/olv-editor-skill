# Robustez — qualidade que não depende do modelo

Este arquivo não define estética. Cor, fonte, composição, ritmo e linguagem visual continuam livres e nascem de cada vídeo (`SKILL.md`, "Direção criativa"). Aqui ficam só **processo e verificação**: o que se confere, com evidência, para que qualquer modelo — grande ou pequeno, com ou sem visão — entregue um vídeo bem encaixado. Tudo abaixo é meio, nunca molde: se o vídeo pede outra solução, ela vale, desde que passe nas mesmas verificações.

## 1. Um sistema por vídeo, escrito em números, antes das cenas

Antes da primeira cena, registre no `plano.md` o sistema de layout do vídeo — qualquer um que sirva à história:

- eixo e margens (ex.: centro em x = 540, margens de N px, ou grade assimétrica — a escolha é do vídeo);
- zonas verticais com altura em px (cabeçalho, título, área de conteúdo, legenda, zona de interface da plataforma);
- tamanhos de tipografia por papel (título, apoio, rótulo) e o número máximo de linhas;
- onde fica a legenda e o que nunca invade essa faixa.

Toda cena **herda** esse sistema. Cena que precisa sair dele sai de propósito, com a razão registrada. A deriva — cada cena com um eixo, uma margem e um tamanho diferentes — é a causa mais comum de "tudo desencaixado".

## 2. Fonte única de verdade

- Tokens (cores, fontes, margens, tamanhos) em variáveis, não repetidos à mão em cada arquivo.
- Com seis ou mais cenas parecidas, gere-as de dados (um script ou template que recebe título, rótulo e conteúdo) em vez de editar cada arquivo. Corrigir o sistema uma vez corrige todas as cenas.
- Se o usuário reclama de algo que aparece em **várias** cenas, o defeito é do sistema: ache a causa comum e corrija ali, depois reverifique todas as cenas.

## 3. Meça, não adivinhe

Antes de entregar, confirme com número ou imagem — nunca por suposição:

- **Caixa × texto:** a largura do texto cabe na caixa com folga (estime largura ≈ caracteres × tamanho × fator da fonte, ou meça no DOM). Rótulo longo muda a caixa, não o contrário.
- **Dentro do quadro:** nenhum elemento, no estado **final** da animação, ultrapassa a borda do frame nem a caixa segura.
- **Sobreposição:** só existe quando intencional (e marcada com `data-layout-allow-overlap`). Cartões, rótulos e ícones nunca escondem texto.
- **Eixo e massa visual:** o conteúdo ocupa o quadro de forma equilibrada — não fica encostado em um lado deixando o outro vazio sem intenção.
- **Respiro vertical:** blocos que pertencem juntos ficam juntos; não há um vão grande e sem função entre título e conteúdo.
- **Legenda:** nenhum conteúdo da cena colide com a faixa da legenda nem com a zona de interface da plataforma.
- **Texto duplicado:** o que a legenda já diz não se repete como subtítulo na tela, a menos que o vídeo precise.
- **Ortografia:** acentos, cedilhas e caracteres especiais corretos em todo texto da tela (revisar na imagem, não só no código).
- **Estado final:** confira também o instante em que tudo já entrou na cena, não apenas o meio das animações. Muita coisa só se desencaixa quando o último elemento assenta.

## 4. Ciclo visual obrigatório

1. Gerar a cena ou o lote.
2. Snapshot (`npx hyperframes snapshot --at ...`), incluindo o estado final de cada cena; use a folha de contato para ver o filme inteiro de uma vez.
3. **Olhar** as imagens e escrever, em uma lista, cada defeito visto (ou "nenhum defeito encontrado em X, Y, Z").
4. Corrigir pela causa (seção 2), não cena por cena.
5. Repetir até a lista sair vazia, depois `npx hyperframes check`.

Não declare uma cena pronta sem ter olhado o frame dela. Vários defeitos só aparecem na imagem; o `check` valida regras, não composição.

## 5. Modelo sem visão (ou visão pouco confiável)

Se não é possível ler imagens com segurança, substitua o olhar por medida e peça ajuda humana onde faltar:

- Rode um script (Playwright/Chrome via CLI) que, para cada cena e cada instante-chave, imprime `getBoundingClientRect()` dos elementos com texto e verifica: dentro do frame, dentro da caixa segura, sem interseção indevida, centro horizontal do conteúdo próximo do eixo declarado no sistema.
- Leia o relatório do `check` por inteiro, inclusive os itens `info`.
- Entregue ao usuário os snapshots (ou a folha de contato) e peça a conferência visual; **diga explicitamente que a checagem visual não foi feita por você**.
- Nunca afirme "ficou alinhado" sem evidência medida ou imagem conferida.

## 6. Passos pequenos e reversíveis

- Uma cena (ou um lote com a mesma receita) por vez; verifique antes de seguir.
- Guarde cópia do estado anterior antes de uma reescrita grande. Se um ajuste pontual resolve, não reescreva tudo.
- Em refação ("refaça, está desencaixado"), comece por listar o que está errado e por que, depois corrija o sistema — não por "melhorar" de forma genérica.

## 7. Contratos técnicos antes do render

Revise de uma vez, antes de renderizar, os pontos que quebram a saída de forma silenciosa: timelines registradas e pausadas, nada dependente de relógio ou sorteio sem semente, caminhos de asset relativos, fontes resolvíveis, duração da raiz, áudio com `id`. A lista completa vive em `motion-style.md` §8 e nas skills do HyperFrames; releia-a em vez de confiar na memória.

## 8. Relato honesto na entrega

Feche com o que foi **verificado e como** (check, snapshots olhados, medidas) e o que **não** foi verificado. Se algo ficou aproximado, diga. Um relato claro vale mais que um "tudo certo" sem prova, e é o que deixa o usuário pedir o ajuste certo.

## Revisão final (responda antes de mostrar a versão)

1. O sistema de layout está escrito no `plano.md` e todas as cenas o seguem?
2. Olhei o frame final de cada cena e listei os defeitos (ou a ausência deles)?
3. Algum texto transborda, corta ou fica escondido?
4. O conteúdo está equilibrado no eixo e livre da legenda e da interface da plataforma?
5. Corrigi as causas comuns no sistema, e não só os sintomas?
6. O relato diz o que foi e o que não foi verificado?
