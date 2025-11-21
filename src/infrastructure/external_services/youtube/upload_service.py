import logging
import os
import sys
from typing import Optional, Tuple
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config.settings import config


logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


class YouTubeUploadService:
    
    def __init__(self):
        self.youtube = None
        self.authenticate()
    
    def authenticate(self):
        logger.info("Autenticando com Google API...")
        
        creds = None
        
        
        if os.path.exists(config.youtube_token_file):
            creds = Credentials.from_authorized_user_file(
                config.youtube_token_file,
                SCOPES
            )
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(config.youtube_client_secrets_file):
                    logger.error(f"Arquivo '{config.youtube_client_secrets_file}' não encontrado!")
                    logger.error("Veja instruções no README.md")
                    sys.exit(1)
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.youtube_client_secrets_file,
                    SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            with open(config.youtube_token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.youtube = build('youtube', 'v3', credentials=creds)
        logger.info("Autenticação bem-sucedida!")
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list = None,
        privacy_status: str = 'PRIVATE'
    ) -> Tuple[bool, Optional[str]]:
        if not os.path.exists(video_path):
            logger.error(f"Arquivo não encontrado: {video_path}")
            return False, None
        
        try:
            file_size = os.path.getsize(video_path)
            logger.info(f"Uploading: {title} ({file_size / (1024*1024):.1f} MB)")
            
            
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags or [],
                    'categoryId': '22'
                },
                'status': {
                    'privacyStatus': privacy_status
                }
            }
            
            media = MediaFileUpload(
                video_path,
                chunksize=-1,
                resumable=True,
                mimetype='video/mp4'
            )
            
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info(f"Progresso: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            logger.info(f"Upload bem-sucedido! URL: {video_url}")
            return True, video_id
            
        except Exception as e:
            logger.error(f"Erro ao fazer upload: {str(e)[:200]}")
            return False, None
