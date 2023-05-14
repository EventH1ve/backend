import qrcode
from schemas.ticket import Ticket


"""
    Generates QRCode for the given ticket and returns the path to 
    the generated image.
"""
def generateTicketQR(ticket: Ticket) -> str:
    qrImg = qrcode.make(encodeTicket(ticket))
    qrPath = "'tmp/' + ticket.qrcode + '.png'"
    qrImg.save(qrPath)
    return qrPath


"""
    Encodes the ticket into a string for QRCode generation.
"""
def encodeTicket(ticket: Ticket) -> str:
    return ';'.join([ticket.id, ticket.eventid, ticket.qrcode])
