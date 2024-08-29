from rest_framework import serializers

from user_statistics.models import Statistics
from user_statistics.models import RefferalSystem
from subscription.serializers import SubscriptionSerializer
from authorization.models import DwUser


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ['launch_number', 'playtime', 'last_launch', 'reg_date']     
class RefferalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefferalSystem
        fields = ['refferal_available', 'code', 'refferal_number', 'refferal_bonus']


class UserPrivateDetailSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(read_only=True)
    statistics = StatisticsSerializer(read_only=True)
    refferals = serializers.SerializerMethodField()

    class Meta:
        model = DwUser
        fields = ['id', 'username', 'email', 'hwid', 'role', 'subscription', 'statistics', 'refferals']

    def get_refferals(self, obj):
        try:
            refferal_system = RefferalSystem.objects.get(user=obj)
            if refferal_system.refferal_available:
                return RefferalsSerializer(refferal_system).data
            else:
                return None
        except RefferalSystem.DoesNotExist:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        refferals_data = self.get_refferals(instance)
        if refferals_data:
            representation['refferals'] = refferals_data
        else:
            representation.pop('refferals', None)  # Удаляем ключ, если данных нет

        return representation

class UserPublicDetailSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(read_only=True)
    statistics = StatisticsSerializer(read_only=True)
    refferals = serializers.SerializerMethodField()

    class Meta:
        model = DwUser
        fields = ['id', 'username', 'role', 'subscription', 'statistics', 'refferals']

    def get_refferals(self, obj):
        try:
            refferal_system = RefferalSystem.objects.get(user=obj)
            if refferal_system.refferal_available:
                return RefferalsSerializer(refferal_system).data
            else:
                return None
        except RefferalSystem.DoesNotExist:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        refferals_data = self.get_refferals(instance)
        if refferals_data:
            representation['refferals'] = refferals_data
        else:
            representation.pop('refferals', None)  # Удаляем ключ, если данных нет

        return representation


class StatisticsUpdateSerializer(serializers.ModelSerializer):
    additional_playtime = serializers.DurationField(write_only=True, required=False)
    increment_launches = serializers.BooleanField(write_only=True, default=False)
    new_last_launch = serializers.DateTimeField(write_only=True, default=False)

    class Meta:
        model = Statistics
        fields = ['playtime', 'additional_playtime', 'launch_number', 'increment_launches', 'last_launch', 'new_last_launch']

    def update(self, instance, validated_data):
        additional_playtime = validated_data.pop('additional_playtime', None)
        increment_launches = validated_data.pop('increment_launches', False)
        new_last_launch = validated_data.pop('new_last_launch', None)

        instance.update_statistics(
            additional_playtime=additional_playtime,
            increment_launches=increment_launches,
            new_last_launch=new_last_launch
        )
        
        return instance
    

