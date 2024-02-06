from datetime import datetime

from pydantic import Base64Str, BaseModel


class FaceRecognitionBase(BaseModel):
    
    name: str
    
    
class FaceRecognitionCreate(FaceRecognitionBase):
    
    image: Base64Str
    from_id: int | None = None
    
    
class FaceRecognitionRead(FaceRecognitionBase):
    
    from_id: int | None = None
    first_seen: datetime
    last_seen: datetime
    seen_count: int
    last_percent: int
    
    def __str__(self) -> str:
        return self.name
