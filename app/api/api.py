from fastapi import APIRouter
from api.endpoints import user, ticket, venue, contact_person as contactPerson
from api.endpoints import event, dashboard

api_router = APIRouter()
api_router.include_router(user.router, prefix="/api/user", tags=["user"])
api_router.include_router(ticket.router, prefix="/api/ticket", tags=["ticket"])
api_router.include_router(venue.router, prefix="/api/venue", tags=["venue"])
api_router.include_router(contactPerson.router, prefix="/api/contactperson", tags=["contactperson"])
api_router.include_router(event.router, prefix="/api/event", tags=["event"])
api_router.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
