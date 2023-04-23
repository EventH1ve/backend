from fastapi import APIRouter
from api.endpoints import user, ticket, venue, contact_person as contactPerson


api_router = APIRouter()
api_router.include_router(user.router, prefix="/api/user", tags=["user"])
api_router.include_router(ticket.router, prefix="/api/ticket", tags=["ticket"])
api_router.include_router(venue.router, prefix="/api/venue", tags=["venue"])
api_router.include_router(contactPerson.router, prefix="/api/contactperson", tags=["contactperson"])
