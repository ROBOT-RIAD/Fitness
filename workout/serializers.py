from rest_framework import serializers
from .models import Workout


class ExtendedFileField(serializers.FileField):
    def to_representation(self, value):
        if value:
            request = self.context.get('request')
            url = getattr(value, 'url', value)
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None

class WorkoutSerializer(serializers.ModelSerializer):
    image = ExtendedFileField(required=False)
    class Meta:
        model = Workout
        fields = ['id','workout_name','time_needed','for_body_part','workout_type','calories_burn','equipment_needed','tag','image','benefits','created_at','updated_at',]
        read_only_fields = ['id', 'created_at', 'updated_at']
