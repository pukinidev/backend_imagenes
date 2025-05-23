from datetime import datetime
from sqlmodel import Column, Field, LargeBinary, SQLModel
from uuid import uuid4  

class Image(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    content: bytes = Field(sa_column=Column(LargeBinary))
    content_type: str = Field(default="image/jpeg")
    created_at: datetime = Field(default_factory=datetime.now)
    
class ImagePrediction(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    image: str = Field(foreign_key="image.id")
    mel: float = Field(default=0.0)
    segmentation: bytes = Field(sa_column=Column(LargeBinary))
    