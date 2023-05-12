-- FUNCTION: update event overall rating 

CREATE OR REPLACE FUNCTION public.update_event_rating()
    RETURNS trigger
    LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
  UPDATE public.events
  SET overallRating = (SELECT AVG(feedbackrating) FROM public.eventfeedback 
					   WHERE public.eventfeedback.eventid = NEW.eventid)
  WHERE public.events.id = NEW.eventid;
  RETURN NEW;
END;
$BODY$;

-- Trigger: when a user add, edit or delete a rating

CREATE TRIGGER update_event_rating_trigger
    AFTER INSERT OR DELETE OR UPDATE 
    ON public.eventfeedback
    FOR EACH ROW
    EXECUTE FUNCTION public.update_event_rating();


-- FUNCTION: calculate number of tickets reserved

CREATE OR REPLACE FUNCTION public.update_ticket_quantity()
    RETURNS trigger
    LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
  UPDATE public.eventticketcapacity
  SET reservedAmount = reservedAmount + 1
  WHERE public.eventticketcapacity.eventid = NEW.eventid;
	RETURN NEW;
END;
$BODY$;

ALTER FUNCTION public.update_ticket_quantity()
    OWNER TO postgres;

-- Trigger: when a user reserve or return a ticket

CREATE TRIGGER reservation_made_trigger
    AFTER INSERT OR DELETE OR UPDATE 
    ON public.ticket
    FOR EACH ROW
    EXECUTE FUNCTION public.update_ticket_quantity();
