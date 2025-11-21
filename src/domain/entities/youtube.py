from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class YouTubeVideo:
    video_id: str
    file_path: str
    title: str
    description: str
    tags: List[str]
    privacy_status: str = 'PRIVATE'
    upload_status: str = 'pending'
    error_message: Optional[str] = None
    created_at: datetime = None
    uploaded_at: Optional[datetime] = None
    youtube_url: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class YouTubeChannel:
    channel_id: str
    title: str
    subscribers: Optional[int] = None
    total_videos: Optional[int] = None
