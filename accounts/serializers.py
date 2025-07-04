from rest_framework import serializers
from .models import User,Profile
from .utils.fields import MultiSelectListField
from drf_extra_fields.fields import Base64ImageField as ExtendedFileField
# jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer





class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required= True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password']
    
    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
        Profile.objects.create(user=user)
        return user
    







class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        data = super().validate({'email': user.email, 'password': password})

        # Add user info to response
        data['user'] = {
            'id' : user.id,
            'email': user.email,
            'role': user.role,
            'name': user.profile.fullname if hasattr(user, 'profile') else '',
        }

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['id'] = user.id
        token['email'] = user.email
        token['role'] = user.role
        return token
    






class ExtendedFileField(serializers.FileField):
    def to_representation(self, value):
        if value:
            request = self.context.get('request')
            url = getattr(value, 'url', value)
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None








class ExtendedFileField(serializers.FileField):
    def to_representation(self, value):
        if value:
            request = self.context.get('request')
            url = getattr(value, 'url', value)
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None




class ProfileSerializer(serializers.ModelSerializer):
    image = ExtendedFileField(required=False)

    at_home = MultiSelectListField(required=False)
    at_gym = MultiSelectListField(required=False)
    martial_arts = MultiSelectListField(required=False)
    running = MultiSelectListField(required=False)
    other_sports = MultiSelectListField(required=False)
    allergies = MultiSelectListField(required=False)
    food_preference = MultiSelectListField(required=False)
    medical_conditions = MultiSelectListField(required=False)
    fitness_goals = MultiSelectListField(required=False)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    



class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)




class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=4)
    confirm_password = serializers.CharField(write_only=True, min_length=4)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs
