import io
import cv2
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
import numpy as np
from sqlmodel import Session
from app.core.database import get_session
from app.models.image import Image as ImageModel
from app.models.image import ImagePrediction as ImagePredictionModel
from app.crud.image import create_image_prediction as crud_create_image_prediction
from app.crud.image import create_image as crud_create_image
from app.crud.image import get_image_prediction as crud_get_image_prediction
from app.services.prediction import generate_segmentation, get_prediction

router = APIRouter()

@router.post("/prediction/")
async def predict(file: UploadFile, db: Session = Depends(get_session)):
    content = await file.read()
    image = io.BytesIO(content)
    image_model = ImageModel(
        content=image.getvalue(),
        content_type=file.content_type or "application/octet-stream",
    )
    image_id = crud_create_image(image_model, db)
    cv2_image = cv2.imdecode(np.frombuffer(image_model.content, np.uint8), cv2.IMREAD_COLOR)
    mel, segmentation = get_prediction(cv2_image) 
    segmentation_bytes = generate_segmentation(segmentation)
    segmentation_model = ImagePredictionModel(
        image=image_id,
        mel=mel,
        segmentation=segmentation_bytes,
    )
    results = crud_create_image_prediction(segmentation_model, db)
    return {
        "segmentation_id": results.id,
        "mel": results.mel
    }
    
@router.get("/prediction/{image_id}")
async def get_prediction_image(image_prediction_id: str, db: Session = Depends(get_session)):
    image_prediction = crud_get_image_prediction(image_prediction_id, db)
    if image_prediction is None:
        raise HTTPException(status_code=404, detail="Image prediction not found")
    return StreamingResponse(
        io.BytesIO(image_prediction.segmentation),
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename=segmentation_{image_prediction_id}.png"},
    )
    
        
    
        