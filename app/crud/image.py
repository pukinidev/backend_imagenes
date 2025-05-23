from fastapi import Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.image import Image as ImageModel
from app.models.image import ImagePrediction as ImagePredictionModel

def create_image(image: ImageModel, db: Session = Depends(get_session)):
    image_to_db = ImageModel.model_validate(image)
    db.add(image_to_db)
    db.commit()
    db.refresh(image_to_db)
    return image_to_db.id

def create_image_prediction(image_prediction: ImagePredictionModel, db: Session = Depends(get_session)):
    image_segmentation_to_db = ImagePredictionModel.model_validate(image_prediction)
    db.add(image_segmentation_to_db)
    db.commit()
    db.refresh(image_segmentation_to_db)
    return image_segmentation_to_db
    
def get_image_prediction(image_prediction_id: str, db: Session = Depends(get_session)):
    statement = select(ImagePredictionModel).where(ImagePredictionModel.id == image_prediction_id)
    image_prediction = db.exec(statement).first()
    return image_prediction