from pydantic import BaseModel
from typing import Optional, Dict

class AudioOperationRequest(BaseModel):
    start_time: Optional[float] = None  # For cut, copy, delete
    end_time: Optional[float] = None    # For cut, copy, delete
    paste_time: Optional[float] = None  # For paste
    segment: Optional[str] = None       # Base64-encoded segment for paste
    effect_name: Optional[str] = None   # Effect to apply (e.g., 'fade')
    effect_params: Optional[Dict] = None  # Parameters for effect
    normalize: Optional[bool] = False   # Whether to normalize

class AudioResponse(BaseModel):
    file_id: str
    file_url: str
    message: str

class EffectsResponse(BaseModel):
    effects: list[str]
