import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from weather.models import WeatherRecord


class Command(BaseCommand):
    help = 'Obtiene clima de OpenWeatherMap y guarda temperatura/humedad'

    def add_arguments(self, parser):
        parser.add_argument('city', type=str)

    def handle(self, *args, **options):
        city = options['city']

        api_key = settings.OPENWEATHER_API_KEY
        if not api_key:
            raise CommandError('OPENWEATHER_API_KEY no esta configurada')

        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric',
        }

        try:
            response = requests.get(url, params=params, timeout=10)
        except requests.RequestException as exc:
            raise CommandError(f'Error de conexion con OpenWeatherMap: {exc}') from exc

        if response.status_code == 404:
            raise CommandError(f'Ciudad no encontrada: {city}')

        if response.status_code == 401:
            raise CommandError('API key invalida')

        if response.status_code != 200:
            raise CommandError(f'Error inesperado de OpenWeatherMap: {response.status_code}')

        data = response.json()
        main = data.get('main', {})
        temperature = main.get('temp')
        humidity = main.get('humidity')
        coord = data.get('coord', {})
        latitude = coord.get('lat')
        longitude = coord.get('lon')

        if temperature is None or humidity is None:
            raise CommandError('Respuesta invalida de OpenWeatherMap')

        record = WeatherRecord.objects.create(
            city=city,
            temperature=temperature,
            humidity=humidity,
            latitude=latitude,
            longitude=longitude,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Guardado: {record.city} T={record.temperature} H={record.humidity}'
            )
        )
