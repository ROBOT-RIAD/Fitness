from django.db import models
from accounts.models import User
# Create your models here.


class TermsAndConditions(models.Model):
    text = models.TextField()

    def __str__(self):
        return "Terms and Conditions"



class PrivacyPolicy(models.Model):
    text = models.TextField()

    def __str__(self):
        return "Privacy Policy"
    



class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    subject = models.CharField(max_length=255, default="Support")  # Fixed subject
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    sent_status = models.BooleanField(default=False)  # Whether the email was successfully sent

    def save(self, *args, **kwargs):
        # Set subject to 'Support' automatically when saving
        if not self.subject:
            self.subject = "Support"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Email from {self.user.email} - Sent: {self.sent_status}"
    
    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"


