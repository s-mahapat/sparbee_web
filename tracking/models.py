from django.db import models

# Create your models here.
class Truck(models.Model):

    reg_no = models.CharField(max_length=12)


class Driver(models.Model):

    name = models.CharField(max_length=50)


class STag(models.Model):

    mac_id = models.CharField(max_length=20)
    active = models.BooleanField(default=True)


class TaggedTrucks(models.Model):

    stag = models.ForeignKey(STag, on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name="tags")


class Tracking(models.Model):

    stag = models.ForeignKey(STag, on_delete=models.CASCADE, related_name="location")
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lng = models.DecimalField(max_digits=10, decimal_places=6)
    update_time = models.DateTimeField(auto_now_add=True)


class LiveTracking(models.Model):
    mobile = models.CharField(max_length=14)
    stag = models.ForeignKey(STag, on_delete=models.CASCADE, related_name="livelocation")
    radius = models.DecimalField(max_digits=10, decimal_places=6)
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lng = models.DecimalField(max_digits=10, decimal_places=6)
    update_time = models.DateTimeField(auto_now_add=True)
