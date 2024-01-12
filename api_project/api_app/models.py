from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators

# Create your models here.
class CarOwner(models.Model):
    firstname = models.CharField(max_length=50, null=False, blank=False)
    lastname = models.CharField(max_length=50, null=False, blank=False)
    birthdate = models.DateField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Car(models.Model):
    make = models.CharField(max_length=50, null=False, blank=False)
    model = models.CharField(max_length=50, null=False, blank=False)
    year = models.IntegerField()
    license = models.CharField(max_length=10)
    registered = models.DateField()
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name="cars",related_query_name='cars')

    # def clean(self):
    #     if self.year>self.registered.year:
    #         raise ValidationError('Car can not be registered before it is produced')
    
    # def save(self,*args,**kwargs):
    #     self.full_clean()
    #     return super().save(*args,**kwargs)

    #def create(self, **kwargs):
    #    if Car.objects.filter(license=kwargs.get("license")).exists():
    #        raise ValidationError("License plate already in use.")
    #    return super().create(**kwargs)

    # def save(self,*args,**kwargs):
    #     if not self.pk:
    #         if Car.objects.filter(license=kwargs["license"]).exists():
    #             raise ValidationError("License plate already in use.")
    #     return super().save(*args,**kwargs)

    


