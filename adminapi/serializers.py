from rest_framework import serializers
from accounts.models import User
from subscription.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['package_name']




class ExtendedFileField(serializers.FileField):
    def to_representation(self, value):
        if value:
            request = self.context.get('request')
            url = getattr(value, 'url', value)
            if request is not None:
                return request.build_absolute_uri(url)  # This converts it to a full URL
            return url
        return None




class UserSerializer(serializers.ModelSerializer):
    # Use SerializerMethodField to get fullname from the related Profile model
    fullname = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    # image = ExtendedFileField()

    # Add package_name field from the related Subscription model
    package_name = SubscriptionSerializer(source='subscriptions.first', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname', 'package_name','image']

    def get_fullname(self, obj):
        # Safely get the fullname from the Profile model
        profile = getattr(obj, 'profile', None)  # Use getattr to avoid RelatedObjectDoesNotExist
        return profile.fullname if profile else None
    
    def get_image(self, obj):
        profile = getattr(obj, 'profile', None)
        if profile and profile.image:
            url = profile.image.url
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(url)
            
            return url
        
        return None
    



class SingleSubscriptionSerializer(serializers.ModelSerializer):
    next_billing_date = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['package_name', 'start_date', 'price', 'status', 'next_billing_date']

    def get_next_billing_date(self, obj):
        return obj.current_period_end if obj.current_period_end else None

   
    

class SingleUserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    subscription_details = SingleSubscriptionSerializer(source='subscriptions.first', read_only=True)

    class Meta:
        model = User
        fields = ['email', 'fullname', 'image', 'subscription_details']

    def get_fullname(self, obj):
        # Safely get the fullname from the Profile model
        profile = getattr(obj, 'profile', None)
        return profile.fullname if profile else None

    def get_image(self, obj):
        profile = getattr(obj, 'profile', None)
        if profile and profile.image:
            url = profile.image.url
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(url)
            
            return url
        
        return None


