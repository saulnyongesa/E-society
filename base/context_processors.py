from .models import Complaint, Event

def notification_count(request):
    event_count = 0
    if request.user.is_authenticated:
        complaints = Complaint.objects.filter(user__society=request.user.society, is_solved=False)
        events = Event.objects.filter(society__user=request.user, is_done=False)
        count = complaints.count() + events.count()
        event_count = events.count()
    else:
        count = 0  # If user is not logged in, return 0

    return {"notification_count": count, "events_count": event_count}
