from typing import Any
from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import date,timedelta
from django.utils.text import slugify
from django.utils.html import strip_tags
from .models import Car,CarOwner
from .serializers import CarSerializer,CarOwnerSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your tests here.

class CarTests(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            'admin','admin@test.py','testpassword', is_staff=True
        )
        self.token = Token.objects.create(
            user = self.admin_user)
        self.user = User.objects.create_user("user", "admin@test.com", "testpassword")
        self.user_token = Token.objects.create(user=self.user)
        self.owner=CarOwner.objects.create(
            firstname="Sergey",
            lastname="Brener",
            birthdate="1978-10-16",
            city="Hamburg",
            address="What do you care, 123a"
        )
        self.car = Car.objects.create(
            make="Mercedes",
            model="600",
            year=2020,
            license="HH A 0001",
            registered="2024-01-01",
            owner=self.owner
        )
        self.valid_payload_owner ={
            "firstname": "Fritz",
            "lastname": "Fritzstein",
            "birthdate": "2000-01-01",#date.today()-20*timedelta(days=365),
            "city": "Berlin",
            "address":"Grossestrasse, 1"
        }
        self.invalid_payload_owner ={
            "firstname": "John",
            "lastname": "Morgenstein",
            "birthdate": date.today()-16*timedelta(days=365),
            "city": "Frankfurt",
            "address":"Kleinestrasse, 11"
        }
        self.valid_payload_car= {
            "make": "BMW",
            "model": "Y11",
            "year": 2010,
            "license": "B YOU SUCK",
            "registered": date.today()-timedelta(days=1)
        }

    def test_get_all_cars(self):
        response = self.client.get(reverse("car_list"))
        cars=Car.objects.all()
        serializer=CarSerializer(cars,many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_all_owners(self):
        response = self.client.get(reverse("car_owner_list"))
        owners=CarOwner.objects.all()
        serializer=CarOwnerSerializer(owners,many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_single_car(self):

        response = self.client.get(reverse("car_detail",args=[self.car.id]))
        #print(type(response.data["license"]))
        car = Car.objects.get(id=self.car.id)
        serializer = CarSerializer(car)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_single_owner(self):
        
        response = self.client.get(reverse("car_owner_detail",args=[self.owner.id]))
        #print(response)
        owner = CarOwner.objects.get(id=self.owner.id)
        serializer = CarOwnerSerializer(owner)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_create_valid_owner_and_car(self):
        
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token.key)
        url=reverse("car_owner_list")
        response = self.client.post(url,data=self.valid_payload_owner, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        _valid_payload_car=self.valid_payload_car.copy()
        _valid_payload_car["owner"]=CarOwner.objects.all()[1].id
        response2 = self.client.post(reverse("car_list"),data=_valid_payload_car, format="json")
        
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_create_as_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.user_token.key)
        url=reverse("car_owner_list")
        response = self.client.post(url,data=self.valid_payload_owner, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authentication_required(self):
        url=reverse("car_owner_list")
        response = self.client.post(url,data=self.valid_payload_owner, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_young_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token.key)
        url=reverse("car_owner_list")
        response = self.client.post(url,data=self.invalid_payload_owner, format="json")
        #print(response.data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("Too young to own a car.", response.data["birthdate"])

    def test_update_car(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token.key)
        url=reverse("car_detail",args=[self.car.id])
        updated_car=CarSerializer(Car.objects.get(id=self.car.id)).data
        updated_car["license"]="  B bb 001  "
        response = self.client.put(url,
                        data=updated_car,
                        format="json"
                                )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(strip_tags(updated_car["license"].upper()).strip(),response.data['license'])

    def test_delete_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token.key)
        url = reverse("car_owner_detail", args=[self.owner.id])
        car_id=self.car.id
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Car.objects.filter(id=car_id).exists())
        

