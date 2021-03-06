'''
Created on 09-Apr-2017

@author: smahapat
'''
from rest_framework import serializers

from models import TaggedTrucks, Truck, STag, Tracking, LiveTracking


class TruckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('id', 'reg_no', 'tags')


class TrackingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tracking
        fields = ('id', 'stag', 'lat', 'lng', 'update_time')


class TaggedTrucksSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaggedTrucks
        fields = ('id', 'stag', 'truck')


class STagSerializer(serializers.ModelSerializer):

    location = TrackingSerializer(many=True, read_only=True)

    class Meta:
        model = STag
        fields = ('id', 'mac_id', 'active', 'location', 'livelocation')
        depth = 1


class LiveTrackingSerializer(serializers.ModelSerializer):

    class Meta:
        model = LiveTracking
        fields = ('id', 'stag', 'lat', 'lng', 'mobile', 'radius', 'update_time')
