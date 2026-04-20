# Weather API - Prueba Tecnica

API construida con Django + DRF para consultar clima desde OpenWeatherMap y guardar historico local.

## Requisitos

- Python 3.9+
- Entorno virtual recomendado

## Instalacion rapida

```bash
pip install -r requirements.txt
python manage.py migrate
```

## Variables de entorno

Crear/editar el archivo `.env` en la raiz del proyecto:

```env
OPENWEATHER_API_KEY=tu_api_key
```

## Comando de gestion

Ejecuta:

```bash
python manage.py fetch_weather "Lima"
```

El comando consulta OpenWeatherMap y guarda `city`, `temperature`, `humidity` y `timestamp`.

## Endpoints

### POST /api/fetch-weather/

Body JSON:

```json
{
  "city": "Lima"
}
```

Respuestas:

- `201`: registro guardado correctamente
- `404`: ciudad no encontrada
- `401`: API key invalida

### GET /api/weather/

Lista registros y permite filtros:

- Por ciudad: `/api/weather/?city=Lima`
- Por fecha (solo fecha): `/api/weather/?timestamp=2026-04-20`

## Tests

```bash
python manage.py test
```
