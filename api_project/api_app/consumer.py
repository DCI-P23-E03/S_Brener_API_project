from .models import CarOwner,Car
import requests
import random
import datetime
import django, os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_project.settings")
django.setup()

number_of_people=10
number_of_cars=20

def generate_db():
    latest_date=datetime.date.today()
    latest_date=latest_date.replace(year=latest_date.year-18)
    latest_date_str=latest_date.strftime('%Y-%m-%d')
    #print(latest_date_str)
    url_people=f"https://fakerapi.it/api/v1/persons?_quantity={number_of_people}&_birthday_end={latest_date_str}&_locale=de_DE"

    response_people=requests.get(url_people)

    people_data=response_people.json()["data"]

    #print(people_data)
    carowners=[]
    for person in people_data:
        carowner=CarOwner(
            firstname=person["firstname"],
            lastname=person["lastname"],
            birthdate=person["birthday"],
            city=person["address"]["city"],
            address=person["address"]["street"]
            )
        carowner.save()
        carowners.append(carowner)

    url_cars=f"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/records?select=make%2C%20model&limit={number_of_cars}"

    response_car=requests.get(url_cars)

    cars_data=response_car.json()["results"]

    for car in cars_data:
        year=random.randint(datetime.date.today().year-30,datetime.date.today().year)
        #year_reg=random.randint(year,datetime.date.today().year)
        reg_date=datetime.date(year,1,1)+random.random()*(datetime.date.today()-datetime.date(year,1,1))
        _car=Car(
            make=car["make"],
            model=car["model"],
            year=year,
            license=chr(random.randint(65,90))+chr(random.randint(65,90))+" "+chr(random.randint(65,90))+" "+str(random.randint(1,9999)),
            registered=reg_date,
            owner=random.choice(carowners)
        )
        _car.save()
    print("yeah")

#if __name__=="__main__":
generate_db()


    

