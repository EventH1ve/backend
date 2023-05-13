from typing import List
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from models.partner import Partner as ModelPartner
from schemas.partner import Partner


router = APIRouter()
@router.get('/',response_model=List[Partner])
async def listEvents(skip: int = 0, limit: int = 10):
    partners = db.session.query(ModelPartner).with_entities(
        ModelPartner.id,
        ModelPartner.name,
        ModelPartner.img
    ).all(  )
    return partners