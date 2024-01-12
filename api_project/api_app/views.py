from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Car,CarOwner
from .serializers import CarSerializer,CarOwnerSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
import django_filters.rest_framework as filters
import django_filters
from rest_framework.response import Response

# Create your views here.

class CarFilter(django_filters.FilterSet):
    year_end=filters.NumberFilter(field_name='year',lookup_expr='lte')#published_date.year
    year_start = filters.CharFilter(field_name='year',lookup_expr='gte')
    class Meta :
        model = Car
        fields = ['make','model']

class CarList(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    #filterset_fields = ['make','model','year']
    filterset_class = CarFilter

    @swagger_auto_schema(operation_description='Retrieve the list of cars')
    def get(self,request, *args,**kwarg):
        return super().get(request, *args,**kwarg)
    
    @swagger_auto_schema(operation_description='Create a new car')
    def post(self,request, *args,**kwarg):
        return super().post(request, *args,**kwarg)
    
    def perform_create(self,serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError(detail=e.detail)
        
class CarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description='Retrieve a car by id')
    def get(self,request, *args,**kwarg):
        return super().get(request, *args,**kwarg)
    
    @swagger_auto_schema(operation_description='Update a single car')
    def put(self,request, *args,**kwarg):
        return super().put(request, *args,**kwarg)
    
    @swagger_auto_schema(operation_description='Deleta a car')
    def delete(self,request, *args,**kwarg):
        return super().delete(request, *args,**kwarg)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError(detail=e.detail)
        
class CarOwnerList(generics.ListCreateAPIView):
    queryset = CarOwner.objects.all()
    serializer_class = CarOwnerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description='Retrieve the list of car owners')
    def get(self,request, *args,**kwarg):
        return super().get(request, *args,**kwarg)
    
    @swagger_auto_schema(operation_description='Create a new car owner')
    def post(self,request, *args,**kwarg):
        return super().post(request, *args,**kwarg)
    
    def perform_create(self,serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError(detail=e.detail)
        
class CarOwnerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarOwner.objects.all()
    serializer_class = CarOwnerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description='Retrieve a car owner by id')
    def get(self,request, *args,**kwarg):
        return super().get(request, *args,**kwarg)
    
    @swagger_auto_schema(operation_description='Update a single car owner')
    def put(self,request, *args,**kwarg):
        return super().put(request, *args,**kwarg)
    
    @swagger_auto_schema(operation_description='Deleta a car owner')
    def delete(self,request, *args,**kwarg):
        return super().delete(request, *args,**kwarg)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError(detail=e.detail)