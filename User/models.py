from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='custom_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users', blank=True)

    @staticmethod
    def authenticate(email, password):
        user = CustomUser.objects.get(email=email)
        if user is not None and user.check_password(password):
            return user
        else:
            return None

    def __str__(self):
        return self.username
    
class AccountVerification(models.Model):
    idAccountVerification = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    validUntil = models.DateTimeField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Verification for {self.user.username}'