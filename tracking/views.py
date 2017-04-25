import os

from django.shortcuts import render

from rest_framework import mixins
from rest_framework import generics
from django.http import JsonResponse

from models import STag, TaggedTrucks, Truck, Tracking, LiveTracking
from serializers import TaggedTrucksSerializer, TruckSerializer, TrackingSerializer,  STagSerializer, LiveTrackingSerializer
from collections import OrderedDict


# Create your views here.
def index(request):
    return render(request=request, template_name="index.html")

def template(request, tmpl_name):
    tmpl_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates", tmpl_name + ".html")
    return render(request=request, template_name=tmpl_file)


class CheckOut(generics.GenericAPIView, mixins.CreateModelMixin):

    queryset = TaggedTrucks.objects.all()
    serializer_class = TaggedTrucksSerializer

    def post(self, request, *args, **kwargs):

        trucknumber = request.data.get('trucknumber', None)
        macid = request.data.get('macid', None)

        (truck, truck_created) = Truck.objects.get_or_create(reg_no=trucknumber)
        (tag, stag_created) = STag.objects.get_or_create(mac_id=macid, active=True)

        TaggedTrucks.objects.get_or_create(stag=tag, truck=truck)

        return JsonResponse({'trucknumber': trucknumber, 'macid': macid})


class TruckList(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):

    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def get(self, request, *args, **kwargs):

        if kwargs['pk']:
            return mixins.RetrieveModelMixin.retrieve(self, request, *args, **kwargs)
        else:
            return mixins.ListModelMixin.list(self, request, *args, **kwargs)


class ItemsInTruck(generics.GenericAPIView, mixins.ListModelMixin):

    queryset = TaggedTrucks.objects.all()
    serializer_class = TaggedTrucksSerializer

    def get(self, request, truck_id, *args, **kwargs):

        # get all the tags on the truck
        self.queryset = TaggedTrucks.objects.filter(truck=truck_id)

        result = OrderedDict()

        # for every tag get the location
        for tag in self.queryset:
            result[tag.id] = {'mac_id': tag.stag.mac_id, 'lat': 0, 'lng': 0, 'update_time': 0}
            tag_locations = Tracking.objects.filter(stag=tag.stag).order_by('-id')[:1]
            for location in tag_locations:
                result[tag.id].update({'mac_id': tag.stag.mac_id, 'lat': location.lat,
                                       'lng': location.lng, 'update_time': location.update_time})


        return JsonResponse(result)

class TrackingAPI(generics.GenericAPIView, mixins.CreateModelMixin):

    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer

    def post(self, request, *args, **kwargs):
        vehice_number = request.POST.get('veh_no', None)
        tag_mac_id = request.POST.get('mac_id', None)

        truck, created = Truck.objects.get_or_create(reg_no=vehice_number)
        stag, created = STag.objects.get_or_create(mac_id=tag_mac_id, active=True)

        TaggedTrucks.objects.get_or_create(stag=stag, truck=truck)
        request.POST['stag'] = stag.id

        return self.create(request, *args, **kwargs)


class TagList(generics.GenericAPIView, mixins.ListModelMixin):

    queryset = STag.objects.all()
    serializer_class = STagSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class LiveTrackingView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):

    queryset = LiveTracking.objects.all()
    serializer_class = LiveTrackingSerializer

    def post(self, request, *args, **kwargs):
        tag_mac_id = request.POST.get('mac_id', None)
        stag, created = STag.objects.get_or_create(mac_id=tag_mac_id, active=True)
        request.POST['stag'] = stag.id
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class Track(generics.GenericAPIView, mixins.ListModelMixin):

    queryset = LiveTracking.objects.all()
    serializer_class = LiveTrackingSerializer

    def get(self, request, mac_id, *args, **kwargs):
        stag = STag.objects.get(mac_id=mac_id)
        self.queryset = LiveTracking.objects.filter(stag=stag).order_by('-id')[:1]
        return self.list(request, *args, **kwargs)

