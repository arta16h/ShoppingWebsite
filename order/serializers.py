from rest_framework import serializers


class AddtoCartSerializer(serializers.Serializer) :
    product = serializers.CharField()
    quantity = serializers.IntegerField()