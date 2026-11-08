# Servicio de predicción de enfermedades

Servicio web donde un médico ingresa los datos de un paciente y obtiene uno de cuatro estados: `NO ENFERMO`, `ENFERMEDAD LEVE`, `ENFERMEDAD AGUDA` o `ENFERMEDAD CRÓNICA`.

El modelo está simulado con reglas en `app/modelo.py`. Se puede usar desde un formulario web o con la API en `POST /predecir`.

## Entradas

| Campo | Descripción | Rango |
|---|---|---|
| `temperatura` | Temperatura en °C | 34 a 43 |
| `frecuencia_cardiaca` | Latidos por minuto | 30 a 220 |
| `dolor` | Intensidad del dolor | 0 a 10 |
| `dias_sintomas` | Días con síntomas | 0 a 3650 |

## Reglas

Se calcula un puntaje de severidad:

- Temperatura: 1 punto desde 37.5, 2 desde 38 y 3 desde 39.
- Frecuencia cardíaca: 1 punto sobre 100 y 2 sobre 120.
- Dolor: 1 punto desde 1, 2 desde 4 y 3 desde 7.

Con puntaje 0 el estado es `NO ENFERMO`. Si no, 90 días o más de síntomas da `ENFERMEDAD CRÓNICA`, un puntaje de 5 o más da `ENFERMEDAD AGUDA` y el resto da `ENFERMEDAD LEVE`.

## Construir la imagen

Desde esta carpeta:

```bash
docker build -t prediccion-enfermedades:1.0 .
```

## Correr el contenedor

```bash
docker run -d --name prediccion -p 5000:5000 prediccion-enfermedades:1.0
```

Si el puerto 5000 está ocupado, cambie el primer número, por ejemplo `-p 8080:5000`.

## Obtener una predicción

En el navegador, abra <http://localhost:5000/>, llene los campos y presione Predecir.

Con la API:

```bash
curl -X POST http://localhost:5000/predecir -H "Content-Type: application/json" -d '{"temperatura": 39.5, "frecuencia_cardiaca": 125, "dolor": 8, "dias_sintomas": 3}'
```

Respuesta:

```json
{"entradas": {"dias_sintomas": 3.0, "dolor": 8.0, "frecuencia_cardiaca": 125.0, "temperatura": 39.5}, "estado": "ENFERMEDAD AGUDA", "puntaje_severidad": 8}
```

Si falta un campo o un valor está fuera de rango, responde 400 con el error.

Valores de ejemplo para cada estado:

| temperatura | frecuencia_cardiaca | dolor | dias_sintomas | Estado |
|---|---|---|---|---|
| 36.6 | 75 | 0 | 0 | NO ENFERMO |
| 37.8 | 85 | 3 | 2 | ENFERMEDAD LEVE |
| 39.5 | 125 | 8 | 3 | ENFERMEDAD AGUDA |
| 37.0 | 80 | 5 | 180 | ENFERMEDAD CRÓNICA |

## Detener el contenedor

```bash
docker rm -f prediccion
```

## Pruebas

```bash
pip install -r requirements-dev.txt
python -m pytest
```
