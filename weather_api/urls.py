from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from weather.views import FetchWeatherAPIView, WeatherRecordViewSet

router = DefaultRouter()
router.register('weather', WeatherRecordViewSet, basename='weather')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/fetch-weather/', FetchWeatherAPIView.as_view(), name='fetch-weather'),
    path('api/', include(router.urls)),
]
