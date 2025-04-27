from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict

class OperationType(str, Enum):
    CUT = "cut"
    DELETE = "delete"
    PASTE = "paste"
    APPLY_EFFECT = "apply_effect"
    NORMALIZE = "normalize"

class AudioOperationRequest(BaseModel):
    operation: OperationType
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    paste_time: Optional[float] = None
    segment_id: Optional[str] = None
    effect_name: Optional[str] = None
    effect_params: Optional[dict] = None

class AudioResponse(BaseModel):
    file_id: str
    file_url: str
    segment_id: Optional[str] = None
    message: str

class EffectsResponse(BaseModel):
    effects: list[str]
