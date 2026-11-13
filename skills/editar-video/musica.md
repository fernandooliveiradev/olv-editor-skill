# Trilhas — a biblioteca de música do estúdio

O estúdio tem uma biblioteca de trilhas própria: **72 faixas instrumentais** de ~3 minutos,
masterizadas alto (≈ −12 LUFS, pico acima de 0 dB), organizadas para vídeo social. Ela não fica no
projeto nem no repositório: fica na máquina, em `~/.olv-studio/musicas`, e o projeto só recebe a faixa
escolhida.

**Biblioteca (pasta do Drive):**
https://drive.google.com/drive/folders/1Y_zyGo1-yHMhbF3DJr3VDmzmXEfw_i-4

> O link é público. Se a biblioteca não deve ser redistribuída, troque o endereço só no seu
> `~/.olv-studio/config` (ou use uma pasta local) — este arquivo é publicado junto com a skill.

## Por que uma biblioteca indexada

Música é o item que mais atrasa um vídeo: procurar "algo calmo" em 72 arquivos, abrir cada um e ouvir
não escala. O estúdio mede cada faixa **uma vez** e guarda a ficha em `musica.json`:

| Medida | Para que serve na escolha |
|---|---|
| **BPM** | dita a energia: 70–100 calmo, 100–125 médio, 125–160 hype |
| **Duração** | precisa cobrir o vídeo com folga |
| **LUFS** | quão alto o master está (estas trilhas são quentes; entram baixas) |
| **LRA** (faixa dinâmica) | LRA baixo = som comprimido e constante; alto = respira, serve narração |
| **Título** | o nome já descreve o clima ("Sunday in Salvador", "Apex…", "Midnight…") |

O agente **não escuta** como uma pessoa: ele escolhe por essas medidas, pelo nome e pelas tags que você
anotar em `musica.tags.json`. Se o modelo tiver áudio, use `olv-musica amostra` para ouvir 15 s.

## Sincronizar (uma vez)

```bash
# da pasta do Drive (≈ 650 MB, 72 faixas)
uvx gdown --folder "https://drive.google.com/drive/folders/1Y_zyGo1-yHMhbF3DJr3VDmzmXEfw_i-4" \
  -O ~/.olv-studio/musicas

# ou de uma pasta local (Drive desktop, pendrive, compra avulsa)
olv-musica sync --de ~/Music/trilhas

# medir tudo (≈ 4 min para 72 faixas; roda em paralelo)
olv-musica index
```

`olv-musica index` extrai o áudio dos `.mp4` para `.m4a` (sem re-encodar), mede e grava
`~/.olv-studio/musicas/musica.json`. Rodar de novo só mede o que mudou.

## Escolher

```bash
olv-musica listar                       # todas, ordenadas por bpm
olv-musica listar --bpm 100-125         # energia média
olv-musica listar --lra 4-12            # que respira (bom sob narração)
olv-musica listar --busca sunset        # pelo título/tags
olv-musica listar --json                # para o agente decidir com números
```

Mapa rápido de decisão:

| O vídeo é… | Procure |
|---|---|
| explicação calma, autoridade | `--bpm 70-105 --lra 4-12` |
| Reels de opinião, ritmo médio | `--bpm 100-125` |
| lançamento, produto, hype | `--bpm 125-160 --dur 20-60` |
| depoimento, prova, bastidor | `--bpm 80-110 --lra 6-14` |

**Tags manuais** (opcional, ajuda muito): crie `~/.olv-studio/musicas/musica.tags.json`:

```json
{
  "Sunday_in_Salvador.mp4": { "tags": ["calmo", "acústico", "verão"] },
  "Piston_and_Bone.mp4": { "tags": ["industrial", "tenso", "ação"] }
}
```

## Usar no projeto

```bash
olv-musica usar "Sunday in Salvador" --projeto . --volume 0.12
```

Ele copia o áudio para `assets/audio/`, lê a duração do filme no `index.html`, imprime o `<audio>` pronto
e registra o crédito em `CREDITOS.md`. Cole o trecho **dentro do root** da composição
(`root_missing_composition_id` se ficar fora).

## Regras de mixagem (o que evita o vídeo soar amador)

- **Uma trilha por vídeo.** Trocar de música no meio quebra a continuidade; se precisar de virada,
  corte a trilha na emenda do vídeo, não no meio da frase.
- **Baixo sob a voz:** `data-volume` 0,10–0,18 nestas trilhas (elas já vêm em −12 LUFS). Se a música
  competir com a fala, o problema é volume, não escolha.
- **Fades sempre:** `data-fade-in="0.6"` e `data-fade-out="1.2"` como ponto de partida.
- **Ducking:** quando a voz é densa, abaixe a música nos trechos falados (`sidechaincompress` na
  mixagem, ou automação de volume por trecho).
- **A trilha não manda no corte.** A fala define os tempos; a música só acompanha. Se a batida não cai
  nos cortes, troque a faixa — não corte a fala para caber na música.
- **Mixagem final em −14 LUFS** (duas passadas, `loudnorm`): a trilha quente não deve empurrar o filme
  para cima do alvo.
- **Crédito e licença:** registre a faixa em `CREDITOS.md` e confirme que ela pode ser usada
  comercialmente no canal do cliente. Biblioteca do estúdio ≠ licença universal.

## Comandos

| Comando | O que faz |
|---|---|
| `olv-musica sync --de <pasta>` | copia faixas de uma pasta para a biblioteca |
| `olv-musica index` | mede e grava `musica.json` (cache por data de modificação) |
| `olv-musica listar [filtros]` | filtra por bpm, duração, LUFS, LRA e texto |
| `olv-musica usar <faixa> --projeto .` | copia para o projeto, imprime o HTML e credita |
| `olv-musica amostra <faixa> --seg 15` | extrai um trecho para escutar |
