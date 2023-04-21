CREATE TABLE Users
(
    id          SERIAL,
    username    VARCHAR,
    email       VARCHAR,
    password    VARCHAR,
    phoneNumber VARCHAR,
    firstName   VARCHAR,
    lastName    VARCHAR,
    type        VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE Organization
(
    id   SERIAL,
    name VARCHAR,
    type VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE EventStatus
(
    id     SERIAL,
    status VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE EventType
(
    id   SERIAL,
    type VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE Venue
(
    id          SERIAL,
    name        VARCHAR,
    capacity    INT,
    description VARCHAR,
    createdBy   VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE PaymentMethod
(
    id     SERIAL,
    method VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE ContactPerson
(
    id          SERIAL,
    name        VARCHAR,
    phoneNumber VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE Organizer
(
    id     SERIAL,
    userID INT,
    PRIMARY KEY (id),
    FOREIGN KEY (userID) REFERENCES Users (id)
);

CREATE TABLE OrganizerOrganization
(
    id             SERIAL,
    organizerID    INT,
    organizationID INT,
    PRIMARY KEY (id),
    FOREIGN KEY (organizationID) REFERENCES Organization (id),
    FOREIGN KEY (organizerID) REFERENCES Organizer (id)
);

CREATE TABLE Attendee
(
    id     SERIAL,
    userID INT,
    PRIMARY KEY (id),
    FOREIGN KEY (userID) REFERENCES Users (id)
);

CREATE TABLE VenueAddress
(
    id             SERIAL,
    venueID        INT,
    buildingNumber INT,
    streetName     VARCHAR,
    city           VARCHAR,
    country        VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY (venueID) REFERENCES Venue (id)
);

CREATE TABLE Event
(
    id                        SERIAL,
    name                      VARCHAR,
    description               VARCHAR,
    type                      INT,
    status                    INT,
    creationDate              DATE,
    registrationStartDateTime TIMESTAMP,
    registrationEndDateTime   TIMESTAMP,
    eventStartDateTime        TIMESTAMP,
    eventEndDateTime          TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (status) REFERENCES EventStatus (id),
    FOREIGN KEY (type) REFERENCES EventType (id)
);

CREATE TABLE EventFeedback
(
    id      SERIAL,
    userID  INT,
    eventID INT,
    PRIMARY KEY (id),
    FOREIGN KEY (userID) REFERENCES Attendee (id),
    FOREIGN KEY (eventID) REFERENCES Event (id)
);

CREATE TABLE OrganizationAddress
(
    id             SERIAL,
    orgID          INT,
    buildingNumber INT,
    streetName     VARCHAR,
    city           VARCHAR,
    country        VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY (orgID) REFERENCES Organization (id)
);

CREATE TABLE Administrator
(
    id     SERIAL,
    userID INT,
    orgID  INT,
    PRIMARY KEY (id),
    FOREIGN KEY (orgID) REFERENCES Organization (id),
    FOREIGN KEY (userID) REFERENCES Users (id)
);

CREATE TABLE Post
(
    id          SERIAL,
    userID      INT,
    eventID     INT,
    title       VARCHAR,
    description VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY (eventID) REFERENCES Event (id),
    FOREIGN KEY (userID) REFERENCES Administrator (id)
);

CREATE TABLE VenueRestriction
(
    id          SERIAL,
    venueID     INT,
    restriction VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY (venueID) REFERENCES Venue (id)
);

CREATE TABLE OrganizationContact
(
    id          SERIAL,
    orgID       INT,
    phoneNumber VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY (orgID) REFERENCES Organization (id)
);

CREATE TABLE TicketType
(
    id      SERIAL,
    eventID INT,
    price   INT,
    PRIMARY KEY (id),
    FOREIGN KEY (eventID) REFERENCES Event (id)
);

CREATE TABLE Ticket
(
    id         SERIAL,
    type       INT,
    eventID    INT,
    qrCode     INT,
    seatNumber INT,
    PRIMARY KEY (id),
    FOREIGN KEY (type) REFERENCES TicketType (id),
    FOREIGN KEY (eventID) REFERENCES Event (id)
);

CREATE TABLE EventVenue
(
    id      SERIAL,
    eventID INT,
    venueID INT,
    PRIMARY KEY (id),
    FOREIGN KEY (eventID) REFERENCES Event (id),
    FOREIGN KEY (venueID) REFERENCES Venue (id)
);

CREATE TABLE TicketTypeEventSeat
(
    id           SERIAL,
    eventID      INT,
    ticketTypeID INT,
    seatNumber   INT,
    PRIMARY KEY (id),
    FOREIGN KEY (ticketTypeID) REFERENCES TicketType (id),
    FOREIGN KEY (eventID) REFERENCES Event (id)
);

CREATE TABLE Transaction
(
    id            SERIAL,
    userID        INT,
    ticketID      INT,
    paymentMethod INT,
    Field         Type,
    PRIMARY KEY (id),
    FOREIGN KEY (paymentMethod) REFERENCES PaymentMethod (id),
    FOREIGN KEY (userID) REFERENCES Attendee (id)
);

CREATE TABLE EventHost
(
    id      SERIAL,
    hostID  INT,
    eventID INT,
    PRIMARY KEY (id),
    FOREIGN KEY (hostID) REFERENCES Organization (id),
    FOREIGN KEY (eventID) REFERENCES Event (id)
);

CREATE TABLE VenueContact
(
    id        SERIAL,
    venueID   INT,
    contactID INT,
    PRIMARY KEY (id),
    FOREIGN KEY (contactID) REFERENCES ContactPerson (id),
    FOREIGN KEY (venueID) REFERENCES Venue (id)
);

CREATE TABLE EventTicketCapacity
(
    id         SERIAL,
    eventID    INT,
    ticketType INT,
    capacity   INT,
    reserved   INT,
    PRIMARY KEY (id),
    FOREIGN KEY (ticketType) REFERENCES TicketType (id),
    FOREIGN KEY (eventID) REFERENCES Event (id)
);

CREATE TABLE EventRating
(
    id         SERIAL,
    rating     INT,
    feedbackID INT,
    PRIMARY KEY (id),
    FOREIGN KEY (feedbackID) REFERENCES EventFeedback (id)
);

