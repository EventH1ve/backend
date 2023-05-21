from typing import List
from schemas.ticket import TicketType

def bookSeats(bookedSeats: List[str], ticketType: TicketType):
    for seat in bookedSeats:
        row, col = seat[0], int(seat[1])
        ticketType.seats[row][col] = 1