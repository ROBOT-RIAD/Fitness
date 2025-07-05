from django.db import models

# Create your models here.


class TermsAndConditions(models.Model):
    text = models.TextField()

    def __str__(self):
        return "Terms and Conditions"



class PrivacyPolicy(models.Model):
    text = models.TextField()

    def __str__(self):
        return "Privacy Policy"