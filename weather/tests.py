from unittest.mock import patch

from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .models import WeatherRecord


@override_settings(OPENWEATHER_API_KEY='test-key')
class WeatherAPITests(APITestCase):
	@patch('weather.management.commands.fetch_weather.requests.get')
	def test_post_fetch_weather_success(self, mock_get):
		mock_get.return_value.status_code = 200
		mock_get.return_value.json.return_value = {
			'main': {'temp': 25.5, 'humidity': 70}
		}

		response = self.client.post('/api/fetch-weather/', {'city': 'Lima'}, format='json')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(WeatherRecord.objects.count(), 1)
		record = WeatherRecord.objects.first()
		self.assertEqual(record.city, 'Lima')
		self.assertEqual(record.temperature, 25.5)
		self.assertEqual(record.humidity, 70)

	@patch('weather.management.commands.fetch_weather.requests.get')
	def test_post_fetch_weather_city_not_found(self, mock_get):
		mock_get.return_value.status_code = 404
		mock_get.return_value.json.return_value = {'message': 'city not found'}

		response = self.client.post('/api/fetch-weather/', {'city': 'NoExiste'}, format='json')

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_get_weather_filter_by_city(self):
		WeatherRecord.objects.create(city='Lima', temperature=20, humidity=60)
		WeatherRecord.objects.create(city='Bogota', temperature=15, humidity=80)

		response = self.client.get('/api/weather/?city=Lima')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]['city'], 'Lima')
