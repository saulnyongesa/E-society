from .models import Complaint, Event
from datetime import timedelta
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from .models import OTP


def notification_count(request):
    event_count = 0
    if request.user.is_authenticated:
        complaints = Complaint.objects.filter(
            user__society=request.user.society, is_solved=False
        )
        events = Event.objects.filter(society__user=request.user, is_done=False)
        count = complaints.count() + events.count()
        event_count = events.count()
    else:
        count = 0  # If user is not logged in, return 0

    return {"notification_count": count, "events_count": event_count}


class CheckOTPTimeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        otps = OTP.objects.filter(is_used=False)
        for otp in otps:
            expire_time = otp.expire_time
            if expire_time <= timezone.now():
                otp.is_used = True
                otp.save()
                otp.delete()
        return None
