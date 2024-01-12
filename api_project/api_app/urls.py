from django.urls import path
from .views import CarList,CarDetail,CarOwnerList,CarOwnerDetail
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view=get_schema_view(
    openapi.Info(
    title="Car.API",
    default_version="v1",
    description="API for cars",
    terms_of_service="https://www.google.com/policies/terms",
    contact=openapi.Contact(email="contact@carapi.local"),
    license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[]
)

urlpatterns = [
    path('cars/',CarList.as_view(),name="car_list"),
    path('cars/<int:pk>/',CarDetail.as_view(),name='car_detail'),
    path('car-owners/',CarOwnerList.as_view(),name="car_owner_list"),
    path('car-owners/<int:pk>/',CarOwnerDetail.as_view(),name='car_owner_detail'),
    #path('lib/',book_list),
    #path('lib/<int:pk>/',book_detail),
    path('openapi/',schema_view.without_ui(cache_timeout=0)),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/',schema_view.with_ui('redoc',cache_timeout=0),name='schema-redoc-ui')
]