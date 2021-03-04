from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UsaState(models.Model):
    __tablename__ = 'usa_states'

    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    code = models.CharField(max_length=2, null=False, blank=False)


class UsaCity(models.Model):
    __tablename__ = 'usa_cities'

    name = models.CharField(max_length=100, null=False, blank=False)
    state = models.ForeignKey(UsaState, on_delete=models.CASCADE)

    @property
    def locality(self):
        return f"{self.name}, {self.state.code}"


class UsaRealEstate(models.Model):
    __tablename__ = 'usa_real_estates'

    name = models.CharField(max_length=256, null=False, blank=False)
    phone = models.CharField(max_length=16, null=False, blank=False)
    city = models.ForeignKey(UsaCity, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=256, null=True, blank=True)
    locality = models.CharField(max_length=64, null=True, blank=True)
    pincode = models.CharField(max_length=64, null=True, blank=True)
    website = models.CharField(max_length=512, null=True, blank=True)
