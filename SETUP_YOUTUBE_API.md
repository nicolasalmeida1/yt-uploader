# 🔑 Configuração do YouTube API

Guia passo a passo para configurar a autenticação com Google API.

---

## 📋 Pré-requisitos

- Conta Google
- Acesso ao Google Cloud Console

---

## 🚀 Passo 1: Criar Projeto no Google Cloud

1. **Acessar Google Cloud Console**
   - Ir para: https://console.cloud.google.com/
   - Fazer login com sua conta Google

2. **Criar novo projeto**
   - Clicar no dropdown de projetos (topo)
   - Clicar "NEW PROJECT"
   - Nome: `instagram-youtube-uploader`
   - Criar

3. **Selecionar projeto**
   - No dropdown de projetos, selecionar o novo projeto

---

## 🛠️ Passo 2: Habilitar YouTube Data API v3

1. **Abrir API Library**
   - Menu → "APIs & Services" → "Library"

2. **Procurar YouTube Data API v3**
   - Search: "youtube data"
   - Selecionar "YouTube Data API v3"

3. **Habilitar**
   - Clicar "ENABLE"

---

## 🔐 Passo 3: Criar Credenciais OAuth

1. **Abrir Credentials**
   - Menu → "APIs & Services" → "Credentials"

2. **Criar Credenciais**
   - Clicar "+ CREATE CREDENTIALS"
   - Tipo: "OAuth 2.0 Client ID"

3. **Configurar Consentimento (1ª vez)**
   - Clicar "Configure OAuth consent screen"
   - Tipo de usuário: "External"
   - Preencher informações básicas:
     - App name: `Instagram Downloader`
     - User support email: seu email
     - Developer contact: seu email
   - Salvar e continuar

4. **Configurar Escopo**
   - "Add or Remove Scopes"
   - Procurar: `youtube.upload`
   - Selecionar: `https://www.googleapis.com/auth/youtube.upload`
   - Atualizar

5. **Adicionar Usuários de Teste**
   - Sua conta Google
   - Salvar e continuar

---

## 💾 Passo 4: Download do client_secrets.json

1. **Voltar para Credentials**
   - "APIs & Services" → "Credentials"

2. **Criar novo OAuth Client ID**
   - Clicar "+ CREATE CREDENTIALS"
   - Type: "OAuth 2.0 Client ID"
   - Application type: "Desktop application"
   - Name: `Instagram Uploader`
   - Criar

3. **Download**
   - Ao lado do client ID criado, clicar ⬇️
   - Salvar arquivo JSON

4. **Renomear e copiar**
   - Renomear arquivo para: `client_secrets.json`
   - Copiar para pasta `yt-uploader/`

```
yt-uploader/
├── client_secrets.json  ← Cole aqui
├── .env
└── scripts/
```

---

## ✅ Passo 5: Testar Autenticação

```bash
cd yt-uploader
python -c "
from src.infrastructure.external_services.youtube.upload_service import YouTubeUploadService
print('Autenticando...')
service = YouTubeUploadService()
print('✓ Sucesso!')
"
```

**Primeira vez:**
1. Abrirá navegador
2. Fazer login com sua conta Google
3. Autorizar acesso
4. Fechar navegador

Arquivo `youtube_token.json` será criado automaticamente.

---

## 📝 Estrutura Final

```
yt-uploader/
├── client_secrets.json     ← Credenciais (NÃO commitar!)
├── youtube_token.json      ← Token (NÃO commitar!)
├── .env                    ← Config (NÃO commitar!)
├── .env.example            ← Template (commitar)
├── config/settings.py
├── src/
└── scripts/upload.py
```

---

## 🔄 Re-autenticar (se Token Expirou)

```bash
# Deletar token antigo
rm youtube_token.json

# Executar novamente (vai pedir autorização)
python scripts/upload.py
```

---

## 🚨 Problemas Comuns

### "client_secrets.json not found"

**Causa:** Arquivo não foi copiado para a pasta  
**Solução:** Repetir Passo 4

### "API not enabled"

**Causa:** YouTube Data API v3 não habilitada  
**Solução:** Repetir Passo 2

### "OAuth scope not granted"

**Causa:** Escopo não configurado corretamente  
**Solução:** Deletar token e refazer autenticação

### "Quota exceeded"

**Causa:** Limite de uploads atingido  
**Solução:** Aumentar delay em `.env`:
```env
DELAY_BETWEEN_UPLOADS=300  # 5 minutos
```

---

## 📊 Quotas do YouTube API

Limite padrão:
- **10.000 créditos/dia**
- Cada upload: ~1.500 créditos
- Limite: ~6 uploads/dia

Para aumentar:
1. Ir para [Google Cloud Console Quotas](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas)
2. Clicar no projeto
3. Clicar "EDIT QUOTAS" (canto superior)
4. Solicitar aumento

---

## ✨ Próximos Passos

1. ✅ Arquivo `client_secrets.json` copiado
2. ✅ `youtube_token.json` criado na 1ª execução
3. ✅ Configurar `.env` com metadados
4. ✅ Executar `python scripts/upload.py`

---

## 📞 Suporte

- [YouTube API Docs](https://developers.google.com/youtube/v3)
- [OAuth 2.0 Docs](https://developers.google.com/identity/protocols/oauth2)
- [Common Errors](https://developers.google.com/youtube/v3/guides/using_the_api)
