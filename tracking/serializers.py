'''
Created on 09-Apr-2017

@author: smahapat
'''
from rest_framework import serializers

from models import TaggedTrucks, Truck, STag, Tracking


class TruckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('id', 'reg_no', 'tags')


class TrackingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tracking
        fields = ('id', 'stag', 'lat', 'lng')


class TaggedTrucksSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaggedTrucks
        fields = ('id', 'stag', 'truck')


class STagSerializer(serializers.ModelSerializer):

    location = TrackingSerializer(many=True, read_only=True)

    class Meta:
        model = STag
        fields = ('mac_id', 'active', 'location')
