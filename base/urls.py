from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home-url'),
    path('signin/', views.signin, name='signin-url'),
    path('signup/', views.signup, name='signup-url'),
    path('dashboard/', views.dashboard, name='dashboard-url'),
    path('logout/', views.log_out, name='logout-url'),

    path('member/status/<int:id>', views.member_status, name='member-status-url'),
    path('members/', views.members, name='members-url'),
    path('member/<int:id>/', views.member, name='member-url'),
    path('member/delete/<int:id>/', views.member_delete, name='member-delete-url'),
    path('member/edit/<int:id>/', views.member_edit, name='member-edit-url'),
    path('member/add/', views.member_add, name='member-add-url'),

    path('events/', views.events, name='events-url'),
    path('event/edit/<int:id>/', views.event_edit, name='event-edit-url'),
    path('event/del/<int:id>/', views.event_delete, name='event-delete-url'),

    path('event/add/', views.event_add, name='event-add-url'),
    path('event/cancel/<int:id>', views.event_cancel, name='event-cancel-url'),

    path('memberpayment/', views.member_payment, name='member-payment-url'),

    path('complaints/', views.complaints, name='complaints-url'),
    path('complaint/<int:id>/', views.complaint, name='complaint-url'),
    path('complaint/reply/<int:id>/', views.complaint_reply, name='complaint-reply-url'),
    path('complaint/reply/edit/<int:id>/', views.complaint_reply_edit, name='complaint-reply-edit-url'),
    path('complaint/delete/<int:id>/', views.complaint_delete, name='complaint-delete-url'),
    path('complaint/edit/<int:id>/', views.complaint_edit, name='complaint-edit-url'),
    path('complaint/add/', views.complaint_add, name='complaint-add-url'),

]