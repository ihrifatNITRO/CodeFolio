from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# class EmailVerification(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_verified = models.BooleanField(default=False)
#
#     def is_expired(self):
#         return timezone.now() > self.created_at + timezone.timedelta(minutes=10)
#
#     def __str__(self):
#         return f"Verification for {self.user.email} - {self.code}"
