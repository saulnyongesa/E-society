from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import *

# for admissions signup
class PWDChangeView(PasswordChangeView):
    form = PasswordChangeForm
    success_url = reverse_lazy('home-url')

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'second_name', 'last_name', 'email', 'phone', 'age', 'gender','marital_status']
        
class eventAddForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location']

class eventEditForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description','location', 'date']


class memberPaymentForm(forms.ModelForm):
    class Meta:
        model = MemberPayment
        fields = ['user', 'amount', 'date']

class complaintAddForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description']

class complaintReplyEditForm(forms.ModelForm):
    class Meta:
        model = ComplaintReply
        fields = ['description']


        