from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from engine.src.engine import AudioEngine
import os
import uuid
import shutil
import base64
import numpy as np
from api.models import AudioOperationRequest, AudioResponse, EffectsResponse

router = APIRouter()

# Temporary storage directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=AudioResponse)
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload an audio file and initialize processing.
    """
    # Validate file type and size
    if not file.filename.endswith(('.wav', '.mp3')):
        raise HTTPException(status_code=400, detail="Only WAV or MP3 files are supported")
    if file.size > 100_000_000:  # 100MB limit
        raise HTTPException(status_code=400, detail="File size exceeds 100MB")

    # Generate unique file ID
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    # Save uploaded file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    return AudioResponse(
        file_id=file_id,
        file_url=file_path,
        message="Audio uploaded successfully"
    )

@router.post("/process/{file_id}", response_model=AudioResponse)
async def process_audio(file_id: str, request: AudioOperationRequest):
    """
    Apply audio operations (cut, copy, paste, delete, normalize, effects).
    """
    # Find the uploaded file
    try:
        file_path = os.path.join(UPLOAD_DIR, [f for f in os.listdir(UPLOAD_DIR) if f.startswith(file_id)][0])
    except IndexError:
        raise HTTPException(status_code=404, detail="File not found")

    # Initialize engine
    engine = AudioEngine()
    try:
        engine.load(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load audio: {str(e)}")

    # Apply operations
    try:
        if request.start_time is not None and request.end_time is not None:
            if request.paste_time is not None:
                # Paste operation (requires a segment)
                if not request.segment:
                    raise HTTPException(status_code=400, detail="Segment required for paste")
                # Decode base64 segment
                segment_data = base64.b64decode(request.segment)
                import io
                import soundfile as sf
                buffer = io.BytesIO(segment_data)
                segment, sr = sf.read(buffer)
                if sr != engine.sr:
                    raise HTTPException(status_code=400, detail="Segment sample rate mismatch")
                engine.paste(segment, request.paste_time)
            else:
                # Cut or delete
                if request.segment is None:
                    engine.delete(request.start_time, request.end_time)
                else:
                    segment, engine = engine.cut(request.start_time, request.end_time)
                    # Optionally return segment (not implemented here for simplicity)

        if request.effect_name:
            if request.effect_name not in engine.effects:
                raise HTTPException(status_code=400, detail=f"Effect '{request.effect_name}' not found")
            engine.apply_effect(request.effect_name, **(request.effect_params or {}))

        if request.normalize:
            engine.normalize()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    # Save processed audio
    output_path = os.path.join(UPLOAD_DIR, f"processed_{file_id}.wav")
    try:
        engine.save(output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save audio: {str(e)}")

    # Clean up original file
    try:
        os.remove(file_path)
    except:
        pass  # Log error in production

    return AudioResponse(
        file_id=file_id,
        file_url=output_path,
        message="Audio processed successfully"
    )

@router.get("/download/{file_id}", response_model=None)
async def download_audio(file_id: str):
    """
    Download the processed audio file.
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, [f for f in os.listdir(UPLOAD_DIR) if f.startswith(f"processed_{file_id}")][0])
    except IndexError:
        raise HTTPException(status_code=404, detail="Processed file not found")

    return FileResponse(file_path, filename=f"processed_{file_id}.wav")

@router.get("/effects", response_model=EffectsResponse)
async def list_effects():
    """
    List available effects.
    """
    engine = AudioEngine()
    return EffectsResponse(effects=list(engine.effects.keys()))# src/api/endpoints.py
