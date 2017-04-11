import os

from django.shortcuts import render

from rest_framework import mixins
from rest_framework import generics
from django.http import JsonResponse

from models import STag, TaggedTrucks, Truck
from serializers import TaggedTrucksSerializer, TruckSerializer


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

    def get(self, request, truck_id=None, *args, **kwargs):

        if kwargs['pk']:
            return mixins.RetrieveModelMixin.retrieve(self, request, *args, **kwargs)
        else:
            return mixins.ListModelMixin.list(self, request, *args, **kwargs)
