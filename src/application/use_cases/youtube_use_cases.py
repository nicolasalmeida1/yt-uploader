import logging
from typing import List, Dict
from pathlib import Path
from src.infrastructure.external_services.youtube.upload_service import YouTubeUploadService
from src.infrastructure.file_system.file_service import YouTubeFileSystemService
from config.settings import config


logger = logging.getLogger(__name__)


class UploadVideoToYouTubeUseCase:
    
    def __init__(self):
        self.upload_service = YouTubeUploadService()
        self.file_service = YouTubeFileSystemService()
    
    def execute(
        self,
        video_path: str,
        title: str = None,
        description: str = None,
        tags: List[str] = None
    ) -> Dict:
        logger.info(f"Iniciando upload de: {video_path}")
        
        # Usar valores padrão se não fornecidos
        title = title or config.default_video_title
        description = description or config.default_video_description
        tags = tags or config.default_video_tags
        
        success, video_id = self.upload_service.upload_video(
            video_path,
            title,
            description,
            tags,
            config.video_privacy_status
        )
        
        return {
            'success': success,
            'video_id': video_id,
            'video_url': f"https://www.youtube.com/watch?v={video_id}" if video_id else None,
            'video_path': video_path
        }


class UploadMultipleVideosUseCase:
    
    def __init__(self):
        self.upload_service = YouTubeUploadService()
        self.file_service = YouTubeFileSystemService()
    
    def execute(self, source_dir: str, limit: int = None) -> Dict:
        logger.info(f"Iniciando upload em lote de: {source_dir}")
        
        # Encontrar vídeos
        videos = self.file_service.find_videos(
            source_dir,
            limit or config.videos_to_upload_per_run
        )
        
        if not videos:
            logger.warning("Nenhum vídeo encontrado!")
            return {'total': 0, 'success': 0, 'failed': 0, 'uploads': [], 'successful_folders': []}
        
        stats = {
            'total': len(videos),
            'success': 0,
            'failed': 0,
            'uploads': [],
            'successful_folders': []  # Rastrear pastas com sucesso
        }
        
        for idx, video_path in enumerate(videos, 1):
            try:
                logger.info(f"[{idx}/{len(videos)}] Uploadando: {video_path}")
                
                result = self.upload_service.upload_video(
                    video_path,
                    title=config.default_video_title,
                    description=config.default_video_description,
                    tags=config.default_video_tags,
                    privacy_status=config.video_privacy_status
                )
                
                if result[0]:
                    stats['success'] += 1
                    stats['uploads'].append({
                        'video_path': video_path,
                        'video_id': result[1],
                        'status': 'success'
                    })
                    # Rastrear pasta do vídeo bem-sucedido
                    video_folder = str(Path(video_path).parent)
                    if video_folder not in stats['successful_folders']:
                        stats['successful_folders'].append(video_folder)
                else:
                    stats['failed'] += 1
                    stats['uploads'].append({
                        'video_path': video_path,
                        'status': 'failed'
                    })
                
            except Exception as e:
                logger.error(f"Erro ao fazer upload: {str(e)}")
                stats['failed'] += 1
                stats['uploads'].append({
                    'video_path': video_path,
                    'status': 'error',
                    'error': str(e)[:100]
                })
        
        return stats
