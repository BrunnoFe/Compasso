<img width="866" height="314" alt="gitlogo" src="https://github.com/user-attachments/assets/e5dad8b9-4276-4b4c-ae12-355560d0f385" />

# Com Passo

**Com Passo** é uma plataforma de pesquisa em psicofisiologia que sincroniza a reprodução de músicas com a aquisição contínua do sinal do **BITalino** (via OpenSignals + Lab Streaming Layer). Amostras e marcadores de evento compartilham um único relógio (`pylsl.local_clock()`), garantindo sincronia precisa entre o estímulo auditivo e os dados fisiológicos.

---

<img width="1273" height="826" alt="ui" src="https://github.com/user-attachments/assets/604702a8-be11-435e-bf07-1884b3a3c304" />

## Sumário

- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Antes de abrir o programa](#antes-de-abrir-o-programa)
- [Menu "Experimento"](#menu-experimento)
- [Arquivos que você precisa preparar](#arquivos-que-você-precisa-preparar)
- [Como executar](#como-executar)
- [A interface, painel por painel](#a-interface-painel-por-painel)
- [Executando um experimento](#executando-um-experimento)
- [Onde os dados são salvos](#onde-os-dados-são-salvos)
- [Formato dos arquivos de saída](#formato-dos-arquivos-de-saída)
- [Logs e diagnóstico de erros](#logs-e-diagnóstico-de-erros)
- [Solução de problemas](#solução-de-problemas)

---

## Requisitos

- **Windows 10/11 ou macOS** (suporte a Linux como melhor esforço: a interface funciona, mas o controle de volume via `amixer` pode exigir configuração adicional dependendo da distribuição).
- **Python 3.12+**.
- **OpenSignals (r)evolution** instalado, com o **Lab Streaming Layer (LSL) ativado** (veja [Antes de abrir o programa](#antes-de-abrir-o-programa)).
- **BITalino emparelhado** ao computador e transmitindo pelo OpenSignals (LSL ativo).

As dependências Python estão em [`requirements.txt`](requirements.txt) (CustomTkinter, pygame-ce, pylsl, pandas, openpyxl, pillow, entre outras). O controle de volume usa `pycaw` no Windows, `osascript` no macOS e `amixer` no Linux (sem dependências extras para macOS/Linux).

---

## Instalação

```bash
# 1. Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 2. Instale as dependências
pip install -r requirements.txt
```

Para gerar um executável distribuível (`.exe` no Windows, `.app` no macOS), consulte [BUILD.md](BUILD.md).

---

## Antes de abrir o programa

A conexão com o BITalino **só funciona** se o OpenSignals estiver compartilhando os dados via Lab Streaming Layer. Faça isto **antes** de iniciar o Compasso:

1. Abra o **OpenSignals (r)evolution**.
2. Entre em **Settings** (engrenagem) → aba **Integration** (ou *Advanced*).
3. Ative a opção **Lab Streaming Layer (LSL)**.
4. Coloque o dispositivo em modo de aquisição/streaming (botão de *play* do OpenSignals), de forma que o BITalino esteja transmitindo amostras.

> Sem o LSL ativo e transmitindo, a conexão do Com Passo falha com uma mensagem de erro (timeout de ~2 s ao procurar a stream).

<img width="1115" height="761" alt="opensignals" src="https://github.com/user-attachments/assets/e68e7110-96a6-492d-9be2-84ddcad987e3" />

---

## Menu "Experimento"

<img width="720" height="530" alt="configsui" src="https://github.com/user-attachments/assets/584b386c-77f5-4327-ac46-fc0a72eba839" />

O menu **Experimento** (barra de menus da janela principal) centraliza toda a configuração do experimento em arquivos `.config` reutilizáveis. Cada `.config` é um arquivo JSON que armazena caminhos, quantidades esperadas e parâmetros do BITalino — basta abri-lo em sessões futuras para restaurar toda a configuração de uma vez.

> **Carga automática ao iniciar:** o Com Passo carrega silenciosamente o último `.config` usado (se o arquivo ainda existir e for válido) e aplica todos os campos automaticamente. Em sessões recorrentes com o mesmo protocolo, basta abrir o programa e clicar em **começar**.

### Novo

Abre a janela de configuração com campos vazios. Preencha todos os campos:

| Campo | Descrição |
| --- | --- |
| Pasta de músicas | Pasta contendo os arquivos de áudio do experimento (.mp3 / .wav / .ogg) |
| Quantidade de músicas | Número esperado de músicas (inteiro ≥ 1) |
| Quantidade de ruído | Número esperado de faixas de ruído (inteiro ≥ 0) |
| Arquivo de fatores | Planilha `.xlsx` / `.xls` com as condições de cada faixa |
| Pasta de salvamento dos dados | Onde os arquivos da sessão serão gravados |
| Canal ativo do BITalino | Canal do sensor a gravar — **A1 a A6** |
| Endereço MAC do BITalino | Endereço do dispositivo no formato `XX:XX:XX:XX:XX:XX` |

Ao clicar em **Salvar**, escolha o nome e o local do arquivo `.config` (pasta padrão sugerida: `Documentos/Compasso/Experiment files/`). A configuração é aplicada imediatamente a todos os campos da janela principal.

### Abrir

Abre um seletor de arquivos para carregar um `.config` existente da pasta `Documentos/Compasso/Experiment files/`. O arquivo é validado campo a campo antes de ser aplicado; erros específicos são exibidos ao usuário.

### Editar

Disponível somente após um **Novo** ou **Abrir** bem-sucedido. Reabre a janela de configuração pré-preenchida com os valores do `.config` atual. Ao salvar, solicita confirmação antes de sobrescrever o arquivo.

---

## Arquivos que você precisa preparar

### 1. Pasta com as músicas

Uma pasta contendo os arquivos de áudio do experimento. Formatos aceitos:

- `.mp3`, `.wav`, `.ogg`

### 2. Planilha de condições (`.xlsx` / `.xls`)

Uma planilha Excel que associa cada arquivo de música à sua **condição/fator** experimental. Ela **precisa** conter exatamente estas duas colunas:

| Coluna | Descrição |
| --- | --- |
| `musica` | Nome do arquivo de áudio **com a extensão** (ex.: `faixa_01.mp3`) |
| `fator` | Condição daquela faixa (ex.: `musica`, `ruido`, ou outros rótulos) |

Exemplo:

| musica | fator |
| --- | --- |
| faixa_01.mp3 | musica |
| branco_01.wav | ruido |

<!-- SCREENSHOT: Conditions and music sheet file example -->

> **Importante:** o valor da coluna `musica` deve bater exatamente com o nome do arquivo na pasta. Se uma música não tiver linha correspondente, o programa avisa e interrompe a verificação — corrija a planilha e recarregue. Os contadores **Música / Ruído** são calculados a partir da coluna `fator`: valores que contêm "ruido"/"ruído" contam como ruído; qualquer outro valor conta como música.

---

## Como executar

```bash
python main.py
```

A janela do Compasso abre maximizada/centralizada. Na **primeira execução**, o programa cria automaticamente as pastas de dados e de logs (veja [Onde os dados são salvos](#onde-os-dados-são-salvos)).

<!-- SCREENSHOT: Main application GUI -->

---

## A interface, painel por painel

A tela é dividida em quatro regiões:

### Painel superior — Conexão com o BITalino

1. **Endereço MAC** — campo de texto para digitar o endereço MAC do BITalino no formato `XX:XX:XX:XX:XX:XX`. É por ele que o Compasso localiza a *stream* LSL publicada pelo OpenSignals.
2. **Canal** — caixa de seleção ao lado do endereço MAC. Escolha o canal do sensor cujo sinal será gravado (**A1 a A6**). O padrão ao abrir o programa é **A1**.
3. **Botão "Desconectar"** — ao lado do Canal; encerra manualmente a conexão com o BITalino e restaura a UI de conexão. Bloqueia (com aviso) se houver um experimento em andamento — pare o experimento antes de desconectar.
4. **Botão de conexão (imagem à direita)** — conecta ao BITalino via LSL. Em caso de sucesso, a imagem muda para "conectado", o campo de MAC e o botão de conexão ficam travados, e o botão **Desconectar** é habilitado. Em caso de falha, aparece uma mensagem explicando o motivo (geralmente LSL desativado ou MAC incorreto).

> **Watchdog de conexão:** após conectar, o Compasso monitora continuamente o fluxo de amostras. Se nenhuma amostra for recebida por ~15 segundos, a conexão é encerrada automaticamente, o experimento em andamento é interrompido com marcador `stop`, e uma mensagem de aviso é exibida.

### Painel central esquerdo — Dados do participante

Preencha **Nome**, **Idade** e **Gênero** e clique em **Salvar informações**. Regras de validação:

- **Nome** e **Gênero**: apenas letras e espaços.
- **Idade**: número inteiro entre 0 e 100.
- Todos os campos são obrigatórios.

Após salvar, os campos ficam travados e o botão muda para **Editar informações**, caso precise corrigir algo.

### Painel central direito — Arquivos e diretório de saída

Três seleções, que também são preenchidas automaticamente ao carregar um `.config` pelo menu **Experimento**:

1. **Arquivos de músicas → Carregar** — escolha a **pasta** com os áudios.
2. **Condições → Buscar** — escolha a **planilha `.xlsx`** de condições. Ao concluir a seleção, o mapeamento entre arquivos e fatores é verificado automaticamente em segundo plano.
3. **Salvar dados em → Escolher** — escolha a **pasta de saída** dos dados.

A linha de status (texto no rodapé deste painel, também repetida no painel inferior) indica o que ainda falta selecionar e, quando tudo está pronto, confirma que os arquivos foram encontrados e mapeados com sucesso.

### Painel central inferior — Player

- **Nome da faixa atual**, **barra de progresso** com tempos e **Volume** (slider que controla o volume principal do sistema).
- **Parar** — interrompe **a qualquer momento** o experimento e a reprodução, gravando o marcador `stop` e finalizando o arquivo da faixa atual.

### Painel inferior — Progresso e início do experimento

- Contadores **Música: X de Y** / **Ruído: X de Y**, atualizados a cada faixa concluída.
- Linha de **status** da sessão.
- **Botão principal** (imagem à direita), que muda de estado durante o experimento:
  - **começar** — sempre visível; ao clicar, os pré-requisitos são verificados e uma mensagem de aviso indica o que falta;
  - **rodando** — desabilitado enquanto a gravação e reprodução de uma faixa estão em andamento;
  - **continuar** — habilitado ao fim de cada faixa, para avançar à próxima.

---

## Executando um experimento

### Pré-requisitos

Ao clicar em **começar**, o Compasso verifica se todos os cinco pré-requisitos estão satisfeitos — caso contrário, uma mensagem indica o que falta:

1. BITalino **conectado**;
2. Informações do participante **salvas**;
3. **Pasta de músicas** carregada (ao menos um arquivo compatível encontrado);
4. **Planilha de condições** carregada e mapeamento concluído;
5. **Diretório de saída** escolhido.

### Passo a passo

1. Configure o OpenSignals com o LSL ativo (veja [Antes de abrir o programa](#antes-de-abrir-o-programa)).
2. Abra o Com Passo — o último `.config` é carregado automaticamente se existir.
3. Se necessário, use **Experimento → Novo** para criar uma configuração ou **Experimento → Abrir** para carregar uma existente.
4. Confirme o endereço MAC e o canal (**A1–A6**) no painel superior e clique no botão de conexão.
5. Preencha Nome, Idade e Gênero e clique em **Salvar informações**.
6. Verifique que a linha de status confirma o mapeamento bem-sucedido entre músicas e condições.
7. Clique em **começar**. A ordem das faixas é **embaralhada** (aleatória, sem repetição).
8. Para cada faixa, o ciclo é:
   1. **Contagem regressiva de 10 segundos** — a gravação do sinal começa neste instante (marcador `countdown_start`). O botão vai para **rodando** (desabilitado).
   2. **Reprodução da faixa** — ao iniciar o áudio, é gravado o marcador `music_start` (com o nome do arquivo e o fator). A faixa toca até o fim.
   3. **Fim da faixa** — grava o marcador `music_end`, finaliza o par CSV + XLSX e atualiza os contadores.
   4. O botão muda para **continuar**: a sessão aguarda o pesquisador clicar para ir à próxima faixa. Use este intervalo conforme o protocolo (instruções ao participante, anotações etc.).
9. Quando todas as faixas terminam, a sessão é finalizada automaticamente.
10. O botão **Parar** (painel central inferior) encerra a sessão a qualquer momento, gravando um marcador `stop` e finalizando o arquivo da faixa em andamento.

---

## Onde os dados são salvos

| O quê | Local |
| --- | --- |
| **Dados do experimento** | `Documentos/Compasso/data/` (ou a pasta escolhida em "Salvar dados em") |
| **Arquivos de configuração** | `Documentos/Compasso/Experiment files/` |
| **Logs por categoria** | `%LOCALAPPDATA%\Compasso\logs\<categoria>\` (Windows) / `~/Library/Application Support/Compasso/logs/` (macOS) |
| **Arquivo central de erros** | `%LOCALAPPDATA%\Compasso\errors.log` (Windows) / `~/Library/Application Support/Compasso/errors.log` (macOS) |

As pastas são criadas automaticamente na primeira execução.

---

## Formato dos arquivos de saída

Cada coleta cria **uma pasta** nomeada `nome_idade_genero_dia-mes-ano_hora-min-seg` dentro do diretório de saída. Dentro dessa pasta, cada faixa gera **um par de arquivos** (CSV + XLSX) nomeados `ordem_nomedamusica`:

```text
Documentos/Compasso/data/
└── joao_25_masculino_15-06-2025_10-30-00/
    ├── 01_faixa_01.csv
    ├── 01_faixa_01.xlsx
    ├── 02_branco_01.csv
    └── 02_branco_01.xlsx
```

- A **ordem** é a posição da faixa na playlist embaralhada (começa em 1, com zero à esquerda — largura mínima de 2 dígitos).
- A **extensão do áudio** é removida do nome do arquivo.
- O **CSV é gravado em tempo real** (com fsync periódico, resistindo a quedas inesperadas); o **XLSX é gerado ao final** de cada faixa a partir do mesmo conteúdo.

<!-- SCREENSHOT: Example data file -->

### Colunas (nesta ordem exata)

| Coluna | Descrição |
| --- | --- |
| `timestamp` | Segundos desde o início da contagem regressiva daquela faixa (`local_clock()` − t0, onde t0 = instante do `countdown_start`). |
| `signal` | Valor do sensor do BITalino no canal selecionado. |
| `markers` | Vazio na maioria das linhas; preenchido nos eventos: `countdown_start`, `music_start`, `music_end`, `stop`. |
| `music_file` | Preenchido **apenas** na linha `music_start` (nome do arquivo da faixa). |
| `fator` | Preenchido **apenas** na linha `music_start` (condição/fator da faixa). |

> Os marcadores são alinhados à amostra mais próxima do instante do evento (primeira amostra com timestamp LSL ≥ ao instante do marcador).

---

## Logs e diagnóstico de erros

- Cada módulo grava em sua **própria subpasta** dentro de `logs/` (`connections/`, `gui/`, `main/`, `player/`, `recorder/`, `experiment/`, `musics/`), com um arquivo por execução identificado por data e hora.
- O **`errors.log`** (fora da pasta `logs/`) reúne **somente** avisos e erros (`WARNING`/`ERROR`/`CRITICAL`) de toda a aplicação — é o primeiro lugar para olhar quando algo der errado. O arquivo tem rotação automática de tamanho.

---

## Solução de problemas

| Sintoma | Causa provável / solução |
| --- | --- |
| **Mensagem de aviso ao clicar em "começar"** | Falta um dos cinco pré-requisitos. Verifique a mensagem exibida e o que ainda está pendente. |
| **Erro ao conectar o BITalino** | O **Lab Streaming Layer** não está ativo no OpenSignals, ou o dispositivo não está transmitindo. Reative e tente novamente. |
| **Falha ao conectar / timeout** | OpenSignals sem LSL ativo ou sem transmitir, ou MAC incorreto. Ative o LSL, coloque o BITalino em aquisição e confira o endereço MAC. |
| **"Conexão com BITalino perdida" durante o experimento** | O watchdog detectou ≥ 15 s sem amostras. Verifique o sensor e o OpenSignals, e reconecte. |
| **"Nenhuma condição encontrada para X"** | O nome na coluna `musica` da planilha não bate com o arquivo na pasta. Corrija a planilha e recarregue. |
| **Sinal sempre 0 ou constante** | Canal errado selecionado. Consulte a primeira amostra registrada no log (linha "Primeira amostra completa") e ajuste o **Canal** no painel superior ou em **Experimento → Editar**. |
| **Áudio não toca** | Verifique se os arquivos estão em `.mp3`, `.wav` ou `.ogg` e se o volume do sistema não está no mínimo. |
| **Onde estão os arquivos de erro?** | `%LOCALAPPDATA%\Compasso\errors.log` (Windows) / `~/Library/Application Support/Compasso/errors.log` (macOS). |
