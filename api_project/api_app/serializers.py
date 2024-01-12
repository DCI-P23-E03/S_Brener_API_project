from rest_framework import serializers
from .models import Car,CarOwner
from datetime import date 
from rest_framework.exceptions import ValidationError
from django.utils.html import escape,strip_tags
from django.utils.text import slugify

class OwnerAgeValidator:
    def __call__(self, value):
        if value>date.today().replace(year=date.today().year-18):
            raise ValidationError("Too young to own a car.")
        
class YearValidator:
    def __call__(self,value):
        if value>date.today().year:
            raise ValidationError("We are not there yet.")
        
class LicenseValidator:
    def __call__(self,value):
        value=strip_tags(value.upper()).strip()
        #if len(value)>10:
        #    raise ValidationError("Too long.")
        if Car.objects.filter(license=value).exists():
            raise ValidationError("License plate already in use.")
        value_parts=value.split()
        if not all([x.isalnum() for x in value_parts]):
            raise ValidationError("Only letters and numbers are allowed.")
        if len(value_parts)>3 or len(value_parts)<2:
            raise ValidationError("Wrong format.")
        if len(value_parts[0])>3 or not value_parts[0].isalpha():
            raise ValidationError("First group must be a group of 1,2 or 3 letters.")

class CarSerializer(serializers.ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(queryset=CarOwner.objects.all())

    year = serializers.IntegerField(validators=[YearValidator()])
    license = serializers.CharField(max_length=10, validators=[LicenseValidator()])

    def validate_make(self,value):
        return strip_tags(value).title()
    
    def validate_license(self,value):
        return strip_tags(value.upper()).strip()
    
    def validate(self,data):
        year = data.get("year")
        registered_year = data.get("registered").year
        birthyear = data.get("owner").birthdate.year
        if year>registered_year:
            raise ValidationError('Car can not be registered before it is produced')
        if birthyear>1999 and year<=1990:
            raise ValidationError('No way!')
        return super().validate(data)

    
    # def to_representation(self, instance):
    #     print(instance.owner)
    #     return super().to_representation(instance)
    
    class Meta:
        model = Car
        fields = ["id","make","model","year","license","registered","owner"]
        
class CarOwnerSerializer(serializers.ModelSerializer):

    birthdate = serializers.DateField(required=True, validators=[OwnerAgeValidator()])
    #cars = CarSerializer(default=[])
    

    def validate_firstname(self,value):
        return strip_tags(value).title()
    def validate_lastname(self,value):
        return strip_tags(value).title()
    def validate_city(self,value):
        return strip_tags(value).title()
    def validate_address(self,value):
        return strip_tags(value).title()
    
    class Meta:
        model = CarOwner
        fields = ["id","firstname","lastname","birthdate","city","address","cars"]
        extra_kwargs = {"cars": {"required":False, "allow_null":True}}

