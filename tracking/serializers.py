'''
Created on 09-Apr-2017

@author: smahapat
'''
from rest_framework import serializers

from models import TaggedTrucks, Truck, STag

class STagSerializer(serializers.ModelSerializer):

    class Meta:
        model = STag
        fields = ('mac_id', 'active', 'location')


class TruckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('id', 'reg_no', 'tags')


class TaggedTrucksSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaggedTrucks
        fields = ('id', 'stag', 'truck')



