# 🎬 YouTube Uploader

Faz upload automático de vídeos para o YouTube com metadados personalizáveis.

---

## 🚀 Quick Start

```bash
# 1. Configurar Google API (ver SETUP_YOUTUBE_API.md)
# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
# Editar arquivo .env com suas credenciais e caminhos (ver Configuração abaixo)
```
> ⚠️ **Importante**: Leia [SETUP_YOUTUBE_API.md](SETUP_YOUTUBE_API.md) para configurar as credenciais do Google antes de executar!

```bash
# 4. Executar
python scripts/upload.py
```

---

## 📋 Como Funciona

1. **Procura vídeos** em `VIDEO_SOURCE_DIR` (configurado em `.env`)
2. **Faz upload** com metadados automáticos
3. **Salva informações** de cada upload
4. **Relata status** (sucesso/erro)

---

## ⚙️ Configuração (`.env`)

Editar arquivo `.env`:

```env
# Google API
YOUTUBE_CLIENT_SECRETS_FILE=client_secrets.json
YOUTUBE_TOKEN_FILE=youtube_token.json

# De onde procurar vídeos
VIDEO_SOURCE_DIR=../ig-downloader/downloads

# Quantos vídeos fazer upload por execução
VIDEOS_TO_UPLOAD_PER_RUN=5

# Delay entre uploads (para evitar quota limits)
DELAY_BETWEEN_UPLOADS=60

# Metadados padrão dos vídeos
DEFAULT_VIDEO_TITLE=Reels compilação
DEFAULT_VIDEO_DESCRIPTION=Reels e vídeos compilados
DEFAULT_VIDEO_TAGS=reels,compilação,shorts

# Privacidade (PUBLIC, UNLISTED, PRIVATE)
VIDEO_PRIVACY_STATUS=PRIVATE

# Logging
LOG_LEVEL=INFO
LOG_FILE=uploads.log
```

---

## 🔑 Pré-requisitos: Google API

### Passo 1: Criar Projeto no Google Cloud

1. Ir para [Google Cloud Console](https://console.cloud.google.com/)
2. Criar novo projeto
3. Habilitar "YouTube Data API v3"

### Passo 2: Criar Credenciais

1. Ir para "APIs & Services" → "Credentials"
2. Criar credenciais "OAuth 2.0 Client ID"
3. Tipo: "Desktop Application"
4. Download como JSON

### Passo 3: Copiar Arquivo

Salvar o JSON como `client_secrets.json` na raiz de `yt-uploader/`

```
yt-uploader/
├── client_secrets.json  ← Cole aqui!
├── .env
└── ...
```

---

## 🚀 Usar

### Opção 1: Upload Único

```bash
python scripts/upload.py
```

Procura vídeos em `VIDEO_SOURCE_DIR` e faz upload.

### Opção 2: Monitorar Uploads (Futuro)

```bash
# Em desenvolvimento
```

---

## 📊 Estrutura de Saída

Cria arquivo `youtube_uploads.json`:

```json
{
  "uploads": [
    {
      "video_path": "../ig-downloader/downloads/post_1/video.mp4",
      "video_id": "dQw4w9WgXcQ",
      "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "status": "success",
      "timestamp": "2024-01-15T10:30:00"
    }
  ]
}
```

---

## 🛠️ Troubleshooting

### "client_secrets.json not found"

**Solução:**
1. Baixar arquivo do Google Cloud Console
2. Renomear para `client_secrets.json`
3. Copiar para raiz de `yt-uploader/`

### "Nenhum vídeo encontrado"

**Solução:**
1. Verificar se `VIDEO_SOURCE_DIR` existe em `.env`
2. Verificar se há vídeos em MP4, AVI, MOV, etc.
3. Executar:
```bash
python -c "import os; print(os.listdir('VIDEO_SOURCE_DIR'))"
```

### "Authentication failed"

**Solução:**
1. Deletar `youtube_token.json`
2. Executar novamente (vai abrir navegador para login)
3. Autorizar o acesso

### "Quota exceeded"

**Solução:**
Aumentar delay em `.env`:
```env
DELAY_BETWEEN_UPLOADS=120  # De 60 para 120 segundos
VIDEOS_TO_UPLOAD_PER_RUN=2  # De 5 para 2
```

---

## 📂 Estrutura de Clean Architecture

```
src/
├── domain/                              ← Entidades
│   ├── entities/youtube.py
│   └── repositories/youtube_video_repository.py
│
├── application/                         ← Casos de uso
│   └── use_cases/youtube_use_cases.py
│
└── infrastructure/                      ← Serviços
    ├── external_services/youtube/
    │   └── upload_service.py
    └── file_system/file_service.py
```

---

## 🎯 Metadados Personalizáveis

Para cada vídeo, você pode customizar:

- **Título**: Aparece como nome do vídeo
- **Descrição**: Texto longo com detalhes
- **Tags**: Palavras-chave para busca (max 500 caracteres)
- **Privacidade**: PUBLIC (visível), UNLISTED (link), PRIVATE (só eu)
- **Categoria**: Padrão é "Entertainment"

---

## 🔒 Segurança

⚠️ **NÃO commitar**:
- `.env` (tem configurações)
- `client_secrets.json` (tem credenciais)
- `youtube_token.json` (tem token de acesso)

Todos estão em `.gitignore` para proteção!

---

## 📝 Arquivos Criados

Durante execução:

- `youtube_token.json` - Token de autorização (criado na 1ª execução)
- `uploads.log` - Log de uploads
- `youtube_uploads.json` - Histórico de uploads

---

## 🎯 Casos de Uso

### Scenario 1: Upload simples

```bash
python scripts/upload.py
```

### Scenario 2: Upload com metadados customizados

Editar `scripts/upload.py` para passar metadados diferentes.

### Scenario 3: Agendar uploads diários

Usar task scheduler do Windows:
```bash
# Criar tarefa agendada que execute:
python C:\...\yt-uploader\scripts\upload.py
```

---

## 🔄 Workflow com Instagram Downloader v1.0.0

```bash
# 1. Fazer download do Instagram
cd ../ig-downloader
python scripts/main.py
# Escolher opção 4

# 2. Fazer upload no YouTube
cd ../yt-uploader
python scripts/upload.py

# 3. Repetir conforme necessário
```

---

## 📞 Suporte

Ver `README.md` na raiz do projeto para suporte geral.

---

## 📚 Leitura Adicional

- [YouTube API Documentation](https://developers.google.com/youtube/v3)
- [OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)
