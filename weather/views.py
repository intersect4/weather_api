from django.core.management import CommandError, call_command
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import WeatherRecordFilter
from .models import WeatherRecord
from .serializers import WeatherRecordSerializer


class WeatherRecordViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = WeatherRecord.objects.all().order_by('-timestamp')
	serializer_class = WeatherRecordSerializer
	filterset_class = WeatherRecordFilter


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
