# Templates de gravação 2026/2027

Padrão do estúdio para estrutura de roteiro em social. Linguagem profissional, só estrutura,
atualizado para as regras atuais do Instagram e do YouTube. **Todo vídeo de social nasce dentro de
um destes três formatos** — o formato é escolhido no Passo 1 da skill e define os blocos de tempo,
o gancho, a chamada e a checklist de entrega.

## Como o agente usa este arquivo

1. **Escolher o formato antes do roteiro.** Ofereça Reels, Stories ou Shorts no briefing (Passo 1)
   e não misture estruturas: Stories não tem "gancho de 3 s", Shorts não tem CTA de direct.
2. **Escrever o roteiro já no template.** No `plano.md`, o roteiro sai em tabela com os blocos e
   tempos do formato escolhido, o texto exato do gancho, o CTA único e a capa (≤ 6 palavras).
3. **Converter bloco em cena.** Cada bloco do template vira uma cena (ou um grupo de cenas) na
   composição, com o cue de áudio marcado. O corte/enquadramento muda a cada 3–4 s.
4. **Fechar com a checklist do formato** na verificação e relatar item a item.

---

## 1) REELS

**Objetivo:** alcance, compartilhamento e autoridade.
**Duração:** 25 a 45 s (até 90 s só se houver história que sustente).
**Sinais que o algoritmo mede:** tempo assistido e conclusão, envios por mensagem, curtidas.

| Tempo | Bloco | O que fazer |
|---|---|---|
| 0–3 s | Gancho | Nomear a dor ou o resultado do cliente. Falar no primeiro segundo, com texto na tela. |
| 3–10 s | Contexto | Descrever a situação que o cliente reconhece no próprio negócio. |
| 10–30 s | Ideia central | Um único argumento, com dado, caso ou raciocínio. |
| 30–38 s | Ação prática | Um passo que o cliente aplica no mesmo dia. |
| 38–45 s | Fechamento | Retomar a frase do gancho e fazer um único convite. |

### Estruturas de gancho

- **Problema:** "[Situação] costuma indicar [causa que o cliente não vê]."
- **Pergunta:** "Você consegue responder [pergunta-chave do negócio dele]?"
- **Contraste:** "Empresas que [fazem X] decidem melhor do que as que [fazem Y]."
- **Erro comum:** "O principal erro de quem [objetivo] é [erro]."

### Modelos de chamada para ação (escolher um)

- **Envio:** "Envie este vídeo para quem [função do decisor] na sua empresa."
- **Palavra-chave:** "Comente [PALAVRA] e eu envio [material]."
- **Mensagem:** "Me chame no direct com [PALAVRA] para [benefício]."

### Regras de produção

- Um tema por vídeo, sempre dentro do mesmo nicho.
- Sem marca d'água de outras plataformas, boa resolução, áudio claro, sem bordas e sem tela só de texto.
- Olhar para a lente, tom de conversa profissional.
- Mudança de enquadramento ou corte a cada 3 a 4 segundos.
- Legenda embutida.
- Capa com a promessa em até 6 palavras.
- Termos de busca do cliente na fala, no texto da tela e na legenda.
- Testar dois ganchos diferentes do mesmo roteiro com Trial Reels antes de publicar para a base.

### Pós-publicação (entregar ao usuário no fechamento)

- Comentário fixado com informação complementar.
- Responder todos os comentários na primeira hora.
- Compartilhar o Reels nos Stories no mesmo dia.

---

## 2) STORIES

**Objetivo:** relacionamento e conversão (atinge principalmente quem já segue).
**Formato:** 5 a 7 telas, de 7 a 15 s cada.

| Tela | Função | O que fazer |
|---|---|---|
| 1 | Abertura interativa | Enquete ou quiz sobre uma dor do cliente. |
| 2 | Contexto | Falar à câmera por que a pergunta importa. |
| 3 | Conteúdo | Uma dica ou raciocínio curto, ligado ao Reels mais recente. |
| 4 | Prova | Resultado, bastidor do trabalho ou antes e depois, com autorização. |
| 5 | Caixa de perguntas | Convidar o cliente a expor a dúvida dele. |
| 6 | Chamada para ação | Botão de mensagem ou link, com instrução clara. |

### Regras

- Ao menos um recurso de interação por sequência.
- Frequência: 3 a 5 dias por semana.
- Sequência comercial: no máximo 1 vez por semana.
- Reaproveitar o assunto do Reels da semana, para levar o cliente do alcance à conversa.
- Responder às interações por mensagem de voz curta.
- Salvar nos Destaques: Quem sou, Como funciona, Resultados, Dúvidas.

### Entregável de Stories (não é um vídeo único)

Stories é **sequência de telas independentes**, não um filme:

1. Cada tela é uma composição própria (`compositions/story-01.html` … `story-06.html`), 7–15 s cada,
   1080×1920. Monte um `index.html` master só para revisão, com as telas em sequência.
2. Renderize **um MP4 por tela** (`npx hyperframes render -c compositions/story-01.html -o renders/story-01.mp4`)
   — é assim que cada uma sobe no app — e mantenha o master para o preview.
3. Enquete, quiz, caixa de perguntas e botão de link são **nativos do app e não podem ser queimados no
   vídeo**. Deixe a área deles livre (topo e rodapé, §6 do `motion-style.md`), escreva no vídeo apenas a
   pergunta ou o convite, e entregue uma nota dizendo **qual sticker entra em qual tela**.
4. A última tela entrega a instrução da chamada em texto; o botão é colocado no app sobre a área livre.

---

## 3) SHORTS DO YOUTUBE

**Objetivo:** distribuição no feed de Shorts e ponte para o canal.
**Formato:** vertical 9:16, 1080×1920 (Short não é 16:9).
**Duração:** 20 a 45 s (até 3 min para conteúdo explicativo).
**Sinais que o algoritmo mede:** retenção, conclusão e satisfação do espectador.

| Tempo | Bloco | O que fazer |
|---|---|---|
| 0–2 s | Gancho direto | Promessa ou pergunta, sem apresentação. |
| 2–10 s | Problema | Uma frase sobre a dor e um exemplo concreto. |
| 10–30 s | Resposta em passos | Três passos, três sinais ou erro e solução. |
| 30–40 s | Fechamento em loop | Última frase completa a frase de abertura, para o vídeo reiniciar. |
| Final | Chamada leve | Seguir o canal ou assistir ao vídeo completo. |

### Regras

- O espectador deve terminar com a sensação de ter resolvido algo, não apenas de ter assistido.
- Chamada voltada a comentário, compartilhamento e inscrição, já que a curtida perdeu peso como métrica.
- Publicar em série sobre o mesmo tema, para o espectador assistir vários vídeos do canal na mesma sessão.
- Título e descrição com o termo que o cliente digitaria na busca.
- Uma ou duas hashtags relevantes, mais #Shorts.
- Fixar comentário com o link do vídeo longo.
- Ao reaproveitar o Reels, trocar gancho e título e remover marcas d'água.

---

## Quadro-resumo

| | Reels | Stories | Shorts |
|---|---|---|---|
| Duração | 25–45 s | 5–7 telas | 20–45 s |
| Meta | Alcance e compartilhamento | Relacionamento e conversão | Distribuição e ponte para o canal |
| Sinal principal | Conclusão e envios | Respostas e mensagens | Retenção e satisfação |
| Chamada | Enviar, palavra-chave ou direct | Botão de mensagem | Seguir ou assistir ao completo |

## Rotina semanal sugerida

| Dia | Formato | Função |
|---|---|---|
| Segunda | Reels | Dor do cliente |
| Terça | Stories | Enquete e caixa de perguntas |
| Quarta | Reels + Short | Ideia prática (mesmo roteiro, ganchos diferentes) |
| Quinta | Stories | Prova ou bastidor |
| Sexta | Reels | Autoridade ou caso |
| Sábado ou domingo | Stories | Sequência comercial (no máximo 1 por semana) |
