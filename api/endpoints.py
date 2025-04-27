from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from engine.src.engine import AudioEngine
import os
import uuid
import shutil
import base64
import numpy as np
import soundfile as sf
from api.models import OperationType, AudioOperationRequest, AudioResponse, EffectsResponse

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=AudioResponse)
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(('.wav', '.mp3')):
        raise HTTPException(status_code=400, detail="Only WAV or MP3 files are supported")
    if file.size > 100_000_000:  # 100MB limit
        raise HTTPException(status_code=400, detail="File size exceeds 100MB")

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

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
    try:
        file_path = os.path.join(UPLOAD_DIR, [f for f in os.listdir(UPLOAD_DIR) if f.startswith(file_id)][0])
    except IndexError:
        raise HTTPException(status_code=404, detail="File not found")

    engine = AudioEngine()
    try:
        engine.load(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load audio: {str(e)}")

    segment_id = None
    try:
        if request.operation == OperationType.CUT:
            if request.start_time is None or request.end_time is None:
                raise HTTPException(status_code=400, detail="start_time and end_time required for cut")
            segment, engine = engine.cut(request.start_time, request.end_time)
            segment_id = str(uuid.uuid4())
            segment_path = os.path.join(UPLOAD_DIR, f"segment_{file_id}_{segment_id}.wav")
            sf.write(segment_path, segment, engine.sr)

        elif request.operation == OperationType.DELETE:
            if request.start_time is None or request.end_time is None:
                raise HTTPException(status_code=400, detail="start_time and end_time required for delete")
            engine.delete(request.start_time, request.end_time)

        elif request.operation == OperationType.PASTE:
            if request.segment_id is None or request.paste_time is None:
                raise HTTPException(status_code=400, detail="segment_id and paste_time required for paste")
            segment_path = os.path.join(UPLOAD_DIR, f"segment_{file_id}_{request.segment_id}.wav")
            if not os.path.exists(segment_path):
                raise HTTPException(status_code=404, detail="Segment not found")
            segment, sr = sf.read(segment_path)
            if sr != engine.sr:
                raise HTTPException(status_code=400, detail="Segment sample rate mismatch")
            engine.paste(segment, request.paste_time)

        elif request.operation == OperationType.APPLY_EFFECT:
            if request.effect_name is None:
                raise HTTPException(status_code=400, detail="effect_name required for apply_effect")
            if request.effect_name not in engine.effects:
                raise HTTPException(status_code=400, detail=f"Effect '{request.effect_name}' not found")
            engine.apply_effect(request.effect_name, **(request.effect_params or {}))

        elif request.operation == OperationType.NORMALIZE:
            engine.normalize()

        else:
            raise HTTPException(status_code=400, detail="Invalid operation")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    output_path = os.path.join(UPLOAD_DIR, f"processed_{file_id}.wav")
    try:
        engine.save(output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save audio: {str(e)}")

    try:
        os.remove(file_path)
    except:
        pass

    if request.operation == OperationType.CUT:
        return AudioResponse(
            file_id=file_id,
            file_url=output_path,
            segment_id=segment_id,
            message="Cut operation successful"
        )
    
    return AudioResponse(
        file_id=file_id,
        file_url=output_path,
        message=f"{request.operation.value} operation successful"
    )

@router.get("/download/{file_id}", response_model=None)
async def download_audio(file_id: str):
    try:
        file_path = os.path.join(UPLOAD_DIR, [f for f in os.listdir(UPLOAD_DIR) if f.startswith(f"processed_{file_id}")][0])
    except IndexError:
        raise HTTPException(status_code=404, detail="Processed file not found")

    return FileResponse(file_path, filename=f"processed_{file_id}.wav")

@router.get("/effects", response_model=EffectsResponse)
async def list_effects():
    engine = AudioEngine()
    return EffectsResponse(effects=list(engine.effects.keys()))
