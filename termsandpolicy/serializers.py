from rest_framework import serializers
from .models import TermsAndConditions, PrivacyPolicy,Email




class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditions
        fields = ['id', 'text']



class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ['id', 'text']

    


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['user', 'body']
        read_only_fields = ['user'] 