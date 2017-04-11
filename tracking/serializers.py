'''
Created on 09-Apr-2017

@author: smahapat
'''
from rest_framework import serializers

from models import TaggedTrucks, Truck

class TaggedTrucksSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaggedTrucks
        fields = ('id', 'stag', 'truck')


class TruckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('id', 'reg_no')
