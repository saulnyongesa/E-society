from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from base.forms import *
from .emails import *
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'index.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('dashboard-url')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('dashboard-url')
            else:
                messages.info(request, 'Email or password is incorrect')
    return render(request, 'sign_in.html')


def signup(request):
    if request.method == 'POST':
        # Get form data
        society_name = request.POST.get('society_name')
        registration_certificate = request.FILES.get('registration_certificate')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate form data
        if password != confirm_password:
            messages.error(request, "Password and Confirm Password do not match.")
        try:
            Society.objects.get(name=society_name)
            messages.error(request, "Society already exists.")
        except Society.DoesNotExist:
            # Save Society
            society = Society.objects.create(name=society_name, certificate=registration_certificate)
            society.save()
        try:
            User.objects.get(email=email)
            messages.error(request, "Email already exists.")
        except User.DoesNotExist:
            pass
        # Save User
        user = User.objects.create(
            username=email,
            email=email,
            phone=phone,
            password=make_password(password),  # Hash the password before saving
            society=society,
            is_staff=True
        )
        user.save()
        messages.success(request, 'E-Society Account created successfully')
        # Redirect to a success page or login page
        return redirect('signin-url')  # Replace with actual success page URL or login page

    return render(request, 'sign_up.html')


@login_required(login_url='signin-url')
def dashboard(request):
    user = User.objects.filter(society=request.user.society)
    complaints = Complaint.objects.filter(
        user__society=request.user.society,
        is_solved=False
        )
    events = Event.objects.filter(
        society=request.user.society,
        is_done=True
        )
    context = {
        'user': user.count(),
        'complaints': complaints.count(),
        'events': events.count(),
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='signin-url')
def log_out(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home-url')


# Members functionality=======================================
def member_status(request, id):
    member = User.objects.get(id=id)
    messages.success(request, 'Member status fetched successfully')
    return render(request, 'member_status.html', {'member': member})

@login_required(login_url='signin-url')
def members(request):
    members = User.objects.all()
    return render(request, 'members.html', {'members': members})

@login_required(login_url='signin-url')
def member(request, id):
    member = User.objects.get(id=id)
    return render(request, 'member.html', {'member': member})

@login_required(login_url='signin-url')
def member_delete(request, id):
    member = User.objects.get(id=id)
    member.delete()
    messages.success(request, 'Member deleted successfully')
    return redirect('members-url')

@login_required(login_url='signin-url')
def member_edit(request, id):
    member = User.objects.get(id=id)
    form = UserSignupForm(instance=member)
    if request.method == 'POST':
        form = UserSignupForm(request.POST, instance=member)
        if form.is_valid():
            form.instance.username = form.instance.email
            form.save()
            messages.success(request, 'Member updated successfully')
            return redirect('members-url')
    return render(request, 'member_edit.html', {'form': form, 'member': member})

@login_required(login_url='signin-url')
def member_add(request):
    form = UserSignupForm()
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.instance.username = form.instance.email
            form.instance.password = make_password(form.instance.email)
            form.instance.society = request.user.society
            form.save()
            messages.success(request, 'Member added successfully')
            return redirect('members-url')
    return render(request, 'member_add.html', {'form': form})


    # Events functionality=======================================

@login_required(login_url='signin-url')
def events(request):
        events = Event.objects.filter(
            society=request.user.society,
        )
        return render(request, 'events.html', {'events': events})

@login_required(login_url='signin-url')
def event_add(request):
        form = eventAddForm()
        if request.method == 'POST':
            date = request.POST['date']
            form = eventAddForm(request.POST)
            if form.is_valid():
                form.instance.date = date
                form.instance.society = request.user.society
                users = User.objects.filter(society=request.user.society)
                for user in users:
                    if user.id != request.user.id:
                        send_notification_email(
                            user.email,
                            form.instance.description,
                            date,
                            form.instance.location,
                            form.instance.name,
                        )
                form.save()
                messages.success(request, 'Event added successfully')
                return redirect('events-url')
        return render(request, 'event_add.html', {'form': form})

@login_required(login_url='signin-url')
def event_edit(request, id):
        event = Event.objects.get(id=id)
        form = eventEditForm(instance=event)
        if request.method == 'POST':
            form = eventEditForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request, 'Event updated successfully')
                return redirect('events-url')
        return render(request, 'event_edit.html', {'form': form, 'event': event})

@login_required(login_url='signin-url')
def event_delete(request, id):
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event deleted successfully')
        return redirect('events-url')

@login_required(login_url='signin-url')
def event_cancel(request, id):
        event = Event.objects.get(id=id)
        event.is_cancelled = not event.is_cancelled
        users = User.objects.filter(society=request.user.society)
        for user in users:
            if user.id != request.user.id:
                send_mail(
                    f'Event "{event.name}" scheduled on "{event.date}" cancelled',
                    f'Event "{event.name}" scheduled on "{event.date}" cancelled by administrator, Please contact your administrator for more information.',
                    "sanymtechs@gmail.com",
                    [user.email],
                    fail_silently=False,
                )
        event.save()
        messages.success(request, 'Event updated successfully')
        return redirect('events-url')


    # Member Payments functionality=======================================

@login_required(login_url='signin-url')
def member_payments(request):
        payments = MemberPayment.objects.all()
        return render(request, 'member_payments.html', {'payments': payments})

@login_required(login_url='signin-url')
def member_payment(request, id):
        payment = MemberPayment.objects.get(id=id)
        return render(request, 'member_payment.html', {'payment': payment})

@login_required(login_url='signin-url')
def member_payment_delete(request, id):
        payment = MemberPayment.objects.get(id=id)
        payment.delete()
        messages.success(request, 'Member payment deleted successfully')
        return redirect('member_payments-url')

@login_required(login_url='signin-url')
def member_payment_edit(request, id):
        payment = MemberPayment.objects.get(id=id)
        form = memberPaymentForm(instance=payment)
        if request.method == 'POST':
            form = memberPaymentForm(request.POST, instance=payment)
            if form.is_valid():
                form.save()
                messages.success(request, 'Member payment updated successfully')
                return redirect('member_payments-url')
        return render(request, 'member_payment_edit.html', {'form': form, 'payment': payment})

@login_required(login_url='signin-url')
def member_payment_add(request):
        form = memberPaymentForm()
        if request.method == 'POST':
            form = memberPaymentForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Member payment added successfully')
                return redirect('member_payments-url')
        return render(request, 'member_payment_add.html', {'form': form})


    # Complaints functionality=======================================

@login_required(login_url='signin-url')
def complaints(request):
        complaints = Complaint.objects.filter(
            user__society=request.user.society,
        )
        replies = ComplaintReply.objects.all()
        return render(request, 'complaints.html', {'complaints': complaints, 'replies': replies})

@login_required(login_url='signin-url')
def complaint(request, id):
        complaint = Complaint.objects.get(id=id)
        return render(request, 'complaint.html', {'complaint': complaint})

@login_required(login_url='signin-url')
def complaint_delete(request, id):
        complaint = Complaint.objects.get(id=id)
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully')
        return redirect('complaints-url')

@login_required(login_url='signin-url')
def complaint_reply(request, id):
    complaint = Complaint.objects.get(id=id)
    if request.method == 'POST':
        reply = request.POST['reply']
        reply = ComplaintReply.objects.create(
            complaint=complaint,
            description=reply,
            date=datetime.now().astimezone(),
        )
        reply.save()
        complaint.is_solved = True
        complaint.save()
        messages.success(request, 'Complaint replied successfully')
        return redirect('complaints-url')
    return render(request, 'complaint.html')

@login_required(login_url='signin-url')
def complaint_reply_edit(request, id):
        reply = ComplaintReply.objects.get(id=id)
        complaint = Complaint.objects.get(id=reply.complaint.id)
        form = complaintReplyEditForm(instance=reply)
        if request.method == 'POST':
            form = complaintReplyEditForm(request.POST, instance=reply)
            if form.is_valid():
                form.save()
                messages.success(request, 'Reply updated successfully')
                return redirect('complaints-url')
        return render(request, 'complaint_reply_edit.html', {'form': form, 'reply': reply, 'complaint': complaint})

@login_required(login_url='signin-url')
def complaint_edit(request, id):
        complaint = Complaint.objects.get(id=id)
        form = complaintAddForm(instance=complaint)
        if request.method == 'POST':
            form = complaintAddForm(request.POST, instance=complaint)
            if form.is_valid():
                form.save()
                messages.success(request, 'Complaint updated successfully')
                return redirect('complaints-url')
        return render(request, 'members/complaint_edit.html', {'form': form, 'complaint': complaint})

def complaint_add(request):
    form = complaintAddForm()
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email does not exist')
            return redirect('complaint-add-url')

        form = complaintAddForm(request.POST)
        if form.is_valid():
            form.instance.user = user
            form.instance.date = datetime.now().astimezone()
            form.instance.society = user.society
            complaint_send = form.save()

            # Send email notification
            admin_email = User.objects.get(
                society=user.society,
                is_staff=True
            )
            send_complaint_email(admin_email, email, complaint_send)

            messages.success(request, 'Complaint added successfully')
            return redirect('complaints-url')

    return render(request, 'members/complaint_add.html', {'form': form})
