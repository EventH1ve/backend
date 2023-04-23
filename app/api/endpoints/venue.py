from typing import List
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from models.venue import Venue as ModelVenue, VenueRestriction as ModelVenueRestriction, VenueContact as ModelVenueContact, ContactPerson as ModelContactPerson
from schemas.venue import Venue, VenueRestriction, VenueContact, ContactPerson


router = APIRouter()


@router.get('/', response_model=List[Venue])
async def listVenues(skip: int = 0, limit: int = 10):
    venues = db.session.query(ModelVenue).offset(skip).limit(limit).all()
    return venues


@router.post('/')
async def createVenue(venue: Venue):
    venueModel = ModelVenue(**venue.dict())

    db.session.add(venueModel)
    db.session.commit()

    return {
        "success": True,
        "message": "Venue created."
    }


@router.get('/{venueId}', response_model=Venue)
async def findVenue(venueId: int):
    venue = db.session.query(ModelVenue).filter(ModelVenue.id == venueId).first()
    return venue if venue else {}


@router.post('/restriction')
async def addVenueRestriction(restriction: VenueRestriction):
    restrictionModel = ModelVenueRestriction(**restriction.dict())

    db.session.add(restrictionModel)
    db.session.commit()

    return {
        "success": True,
        "message": "Venue restriction added."
    }


@router.post('/contact')
async def addVenueContact(venueContact: VenueContact):
    venueContactModel = ModelVenueContact(**venueContact.dict())

    db.session.add(venueContactModel)
    db.session.commit()

    return {
        "success": True,
        "message": "Venue contact information added."
    }


@router.get('/contact/{venueId}', response_model=List[ContactPerson])
async def addVenueContact(venueId: int):
    venueContacts = db.session.query(ModelVenueContact).filter(ModelVenueContact.venueid == venueId).all()
    contactPersons = db.session.query(ModelContactPerson).filter(ModelContactPerson.id.in_([vc.contactid for vc in venueContacts])).all()

    return contactPersons