import logging
import os
from typing import List
from pathlib import Path


logger = logging.getLogger(__name__)


class YouTubeFileSystemService:
    
    @staticmethod
    def find_videos(source_dir: str, limit: int = None) -> List[str]:
        videos = []
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'}
        
        try:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    if Path(file).suffix.lower() in video_extensions:
                        videos.append(os.path.join(root, file))
                        if limit and len(videos) >= limit:
                            return videos
            
            logger.info(f"Encontrados {len(videos)} vídeos em {source_dir}")
            return videos
        except Exception as e:
            logger.error(f"Erro ao procurar vídeos: {str(e)}")
            return []
    
    @staticmethod
    def get_video_info(video_path: str) -> dict:
        try:
            if not os.path.exists(video_path):
                return {}
            
            file_stat = os.stat(video_path)
            
            return {
                'path': video_path,
                'filename': os.path.basename(video_path),
                'size_mb': round(file_stat.st_size / (1024 * 1024), 2),
                'created_time': file_stat.st_ctime,
                'modified_time': file_stat.st_mtime
            }
        except Exception as e:
            logger.error(f"Erro ao obter info do vídeo: {str(e)}")
            return {}
    
    @staticmethod
    def delete_folder(folder_path: str) -> bool:
        """Delete uma pasta e todo seu conteúdo de forma segura."""
        try:
            import shutil
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                logger.info(f"Pasta deletada com sucesso: {folder_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao deletar pasta {folder_path}: {str(e)}")
            return False
