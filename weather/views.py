import math
from django.core.management import CommandError, call_command
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import WeatherRecordFilter
from .models import WeatherRecord
from .serializers import WeatherRecordSerializer


class WeatherRecordViewSet(viewsets.ModelViewSet):
	queryset = WeatherRecord.objects.filter(status=True).order_by('-timestamp')
	serializer_class = WeatherRecordSerializer
	filterset_class = WeatherRecordFilter

	def perform_destroy(self, instance):
		instance.status = False
		instance.save()

	@action(detail=False, methods=['get'])
	def nearby(self, request):
		lat = request.query_params.get('lat')
		lon = request.query_params.get('lon')
		radius = request.query_params.get('radius', 10)  # radio en km

		if lat is None or lon is None:
			return Response({'detail': 'Faltan parámetros lat o lon'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			lat = float(lat)
			lon = float(lon)
			radius = float(radius)
		except ValueError:
			return Response({'detail': 'lat, lon y radius deben ser números'}, status=status.HTTP_400_BAD_REQUEST)

		records = self.get_queryset().exclude(latitude__isnull=True).exclude(longitude__isnull=True)
		nearby_records = []

		for record in records:
			# Fórmula de Haversine
			R = 6371.0 # radio de la tierra en km
			dlat = math.radians(record.latitude - lat)
			dlon = math.radians(record.longitude - lon)
			a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat)) * math.cos(math.radians(record.latitude)) * math.sin(dlon / 2)**2
			c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
			distance = R * c

			if distance <= radius:
				nearby_records.append(record)

		serializer = self.get_serializer(nearby_records, many=True)
		return Response(serializer.data)


class FetchWeatherAPIView(APIView):
	def post(self, request):
		city = request.data.get('city')
		if not city:
			return Response(
				{'detail': 'El campo city es obligatorio'},
				status=status.HTTP_400_BAD_REQUEST,
			)

		try:
			call_command('fetch_weather', city)
		except CommandError as exc:
			message = str(exc)
			if 'Ciudad no encontrada' in message:
				return Response({'detail': message}, status=status.HTTP_404_NOT_FOUND)
			if 'API key inválida' in message:
				return Response({'detail': message}, status=status.HTTP_401_UNAUTHORIZED)
			return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)

		record = WeatherRecord.objects.filter(city=city).order_by('-timestamp').first()
		serializer = WeatherRecordSerializer(record)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
