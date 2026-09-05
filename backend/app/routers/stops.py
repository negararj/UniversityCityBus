from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get("/stops", response_model=list[schemas.StopOut])
def get_stops(db: Session = Depends(get_db)):
    stops = db.query(models.Stop).all()
    return stops

