from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MaritalStatus)
admin.site.register(Gender)
admin.site.register(Society)
admin.site.register(User)
admin.site.register(Complaint)
admin.site.register(ComplaintReply)
admin.site.register(Event)
admin.site.register(OTP)