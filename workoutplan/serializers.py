from rest_framework import serializers


class DelimitedListField(serializers.Field):
    """
    Accepts a comma‑separated string OR a JSON list and always returns list[str].
    Outgoing representation is a single comma‑separated string.
    """

    def to_internal_value(self, data):
        if data is None:
            return []

        # If the client sent a real JSON list, keep it.
        if isinstance(data, list):
            str_items = [str(item).strip() for item in data if str(item).strip()]
            return str_items

        # Otherwise treat it as a comma‑separated string.
        if isinstance(data, str):
            str_items = [part.strip() for part in data.split(",") if part.strip()]
            return str_items

        raise serializers.ValidationError("Must be a comma‑separated string or a JSON list.")

    def to_representation(self, value):
        # Store None / [] as an empty string to keep the output compact.
        if not value:
            return ""
        # Always join with a single comma + space for readability.
        return ", ".join(map(str, value))


class TrainingDataSerializer(serializers.Serializer):
    # Basic fields
    fitness_level       = serializers.CharField(max_length=50)
    train               = serializers.CharField(max_length=100)
    injuries_discomfort = serializers.CharField(allow_blank=True, required=False)

    # Daily workout duration (new field)
    daily_duration_minutes = serializers.IntegerField(
        required=True,
        help_text="User's preferred workout time per day in minutes"
    )

    # Muscle‑group fields (all accept comma‑separated input)
    chest        = DelimitedListField(required=False)
    back         = DelimitedListField(required=False)
    shoulders    = DelimitedListField(required=False)
    biceps       = DelimitedListField(required=False)
    triceps      = DelimitedListField(required=False)
    quadriceps   = DelimitedListField(required=False)
    hamstrings   = DelimitedListField(required=False)
    glutes       = DelimitedListField(required=False)
    calves       = DelimitedListField(required=False)
    adductors    = DelimitedListField(required=False)  
    lower_back   = DelimitedListField(required=False)
