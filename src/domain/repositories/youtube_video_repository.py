from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.youtube import YouTubeVideo


class YouTubeVideoRepository(ABC):
    
    @abstractmethod
    def save(self, video: YouTubeVideo) -> None:
        pass
    
    @abstractmethod
    def get_by_id(self, video_id: str) -> Optional[YouTubeVideo]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[YouTubeVideo]:
        pass
    
    @abstractmethod
    def update(self, video: YouTubeVideo) -> None:
        pass
    
    @abstractmethod
    def delete(self, video_id: str) -> None:
        pass
    
    @abstractmethod
    def get_by_status(self, status: str) -> List[YouTubeVideo]:
        pass
