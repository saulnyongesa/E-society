from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class MaritalStatus(models.Model):
    status_name = models.CharField(max_length=20, null=True, unique=True)

    def __str__(self):
        return self.status_name


class Gender(models.Model):
    gender_name = models.CharField(max_length=20, null=True, unique=True)

    def __str__(self):
        return self.gender_name

class Society(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    certificate = models.ImageField(upload_to="certificates/", null=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    second_name = models.CharField(max_length=20, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.ForeignKey(Gender, null=True, on_delete=models.CASCADE)
    marital_status = models.ForeignKey(MaritalStatus, null=True, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField(null=True, unique=True)
    email = models.CharField(max_length=50, null=True, unique=True)
    society = models.ForeignKey(Society, null=True, on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Event(models.Model):
        name = models.CharField(max_length=100, null=True)
        date = models.DateTimeField(null=True)
        description = models.TextField(null=True)
        location = models.CharField(max_length=100, null=True)
        is_done = models.BooleanField(default=False)
        is_cancelled = models.BooleanField(default=False)
        society = models.ForeignKey(Society, null=True, on_delete=models.CASCADE)

        def __str__(self):
            return self.name


class MemberPayment(models.Model):
        user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
        amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
        date = models.DateField(null=True)
        society = models.ForeignKey(Society, null=True, on_delete=models.CASCADE)

        def __str__(self):
            return f"{self.user.username} - {self.amount}"


class Complaint(models.Model):
        user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
        description = models.TextField(null=True)
        date = models.DateField(null=True)
        is_solved = models.BooleanField(default=False)

        def __str__(self):
            return f"Complaint by {self.user.username} on {self.date}"


class ComplaintReply(models.Model):
    complaint = models.ForeignKey(Complaint, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    date = models.DateField(null=True)

    def __str__(self):
        return f"Reply to Complaint by {self.complaint.user.username} on {self.date}"


