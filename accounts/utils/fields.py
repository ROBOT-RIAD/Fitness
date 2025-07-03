from rest_framework import serializers

class MultiSelectListField(serializers.ListField):
    def to_representation(self, value):
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return value.split(',')
        return super().to_representation(value)