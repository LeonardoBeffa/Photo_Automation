# Organizador de Arquivos Multimídia

Este script Python organiza arquivos de imagem e vídeo em diretórios específicos com base em suas características e metadados. Ele utiliza as bibliotecas `exif`, `watchdog` e `logging` para monitorar e mover arquivos.

## Funcionalidades

- **Organização por Ano**: Move arquivos de imagem para diretórios com base no ano extraído dos metadados EXIF da imagem.
- **Separação por Tipo de Arquivo**: Move arquivos de imagem e vídeo para diretórios distintos.
- **Arquivamento de Imagens sem EXIF**: Move imagens que não contêm metadados EXIF para um diretório separado.
- **Detecção Automática de Arquivos**: Monitora um diretório raiz em tempo real e organiza os arquivos conforme são adicionados ou modificados.

## Estrutura de Diretórios

- `DIRETORIO RAIZ`: Diretório principal onde os arquivos são monitorados e organizados.
- `DontEXIF`: Diretório para imagens que não possuem metadados EXIF.
- `videos`: Diretório para arquivos de vídeo.
- `2010`, `2011`, ..., `2024`: Diretórios para imagens, organizadas por ano.

## Tipos de Arquivos Suportados

- **Imagens**: `.jpg`, `.jpeg`, `.gif`, `.png`, `.tiff`, `.bmp`, entre outros.
- **Vídeos**: `.mp4`, `.avi`, `.mov`, `.mkv`, entre outros.

## Como Usar

1. **Configuração**: Ajuste o `source_dir` para o diretório que deseja monitorar.
2. **Execução**: Execute o script. Ele começará a monitorar o diretório raiz e moverá arquivos conforme definidos.
3. **Logs**: Logs de movimentação dos arquivos serão registrados e podem ser visualizados para verificar o status da organização.

## Requisitos

- `exif`
- `watchdog`
- `logging`

Você pode instalar as dependências com:

```bash
pip install exif watchdog
