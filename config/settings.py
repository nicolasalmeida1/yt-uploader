import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    
    def __init__(self):
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)
    
    @property
    def youtube_client_secrets_file(self) -> str:
        return os.getenv('YOUTUBE_CLIENT_SECRETS_FILE', 'client_secrets.json')
    
    @property
    def youtube_token_file(self) -> str:
        return os.getenv('YOUTUBE_TOKEN_FILE', 'youtube_token.json')
    
    @property
    def video_source_dir(self) -> str:
        return os.getenv('VIDEO_SOURCE_DIR', '../ig-downloader/downloads')
    
    @property
    def videos_to_upload_per_run(self) -> int:
        return int(os.getenv('VIDEOS_TO_UPLOAD_PER_RUN', '5'))
    
    @property
    def delay_between_uploads(self) -> int:
        return int(os.getenv('DELAY_BETWEEN_UPLOADS', '60'))
    
    @property
    def default_video_title(self) -> str:
        return os.getenv('DEFAULT_VIDEO_TITLE', 'Reels compilação')
    
    @property
    def default_video_description(self) -> str:
        return os.getenv('DEFAULT_VIDEO_DESCRIPTION', 'Reels e vídeos compilados do Instagram')
    
    @property
    def default_video_tags(self) -> list:
        tags_str = os.getenv('DEFAULT_VIDEO_TAGS', 'reels,instagram,compilação,shorts')
        return [tag.strip() for tag in tags_str.split(',')]
    
    @property
    def video_privacy_status(self) -> str:
        return os.getenv('VIDEO_PRIVACY_STATUS', 'PRIVATE')
    
    # Logging
    @property
    def log_level(self) -> str:
        return os.getenv('LOG_LEVEL', 'INFO')
    
    @property
    def log_file(self) -> str:
        return os.getenv('LOG_FILE', 'uploads.log')
    
    @property
    def upload_status_file(self) -> str:
        return os.getenv('UPLOAD_STATUS_FILE', 'youtube_uploads.json')


config = Config()
