from rest_framework import serializers

from user_statistics.models import Statistics


class StatisticsUpdateSerializer(serializers.ModelSerializer):
    additional_playtime = serializers.DurationField(write_only=True, required=False)
    increment_launches = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = Statistics
        fields = ['playtime', 'additional_playtime', 'launch_number', 'increment_launches']

    def update(self, instance, validated_data):
        additional_playtime = validated_data.pop('additional_playtime', None)
        increment_launches = validated_data.pop('increment_launches', False)

        instance.update_statistics(
            additional_playtime=additional_playtime,
            increment_launches=increment_launches
        )
        
        return instance
