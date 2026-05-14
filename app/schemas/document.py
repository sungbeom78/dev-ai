from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    content: str
    source: Optional[str] = None
    license: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class ChunkBase(BaseModel):
    chunk_index: int
    content: str
    char_start: int
    char_end: int

class ChunkResponse(ChunkBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    document_id: int
    created_at: datetime
