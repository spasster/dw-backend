from rest_framework import serializers

from subscription.models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ['sub_dur', 'start_date', 'expiration_date']

