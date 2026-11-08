from dataclasses import dataclass

NO_ENFERMO = "NO ENFERMO"
LEVE = "ENFERMEDAD LEVE"
AGUDA = "ENFERMEDAD AGUDA"
CRONICA = "ENFERMEDAD CRÓNICA"

DIAS_CRONICO = 90
PUNTAJE_AGUDO = 5

RANGOS = {
    "temperatura": (34.0, 43.0),
    "frecuencia_cardiaca": (30, 220),
    "dolor": (0, 10),
    "dias_sintomas": (0, 3650),
}


@dataclass(frozen=True)
class Prediccion:
    estado: str
    puntaje: int


def _puntos_temperatura(t: float) -> int:
    if t >= 39.0:
        return 3
    if t >= 38.0:
        return 2
    if t >= 37.5:
        return 1
    return 0


def _puntos_frecuencia(fc: float) -> int:
    if fc > 120:
        return 2
    if fc > 100:
        return 1
    return 0


def _puntos_dolor(d: float) -> int:
    if d >= 7:
        return 3
    if d >= 4:
        return 2
    if d >= 1:
        return 1
    return 0


def validar(datos: dict) -> dict:
    limpios = {}
    for campo, (minimo, maximo) in RANGOS.items():
        if campo not in datos or datos[campo] in (None, ""):
            raise ValueError(f"Falta el campo '{campo}'.")
        try:
            valor = float(datos[campo])
        except (TypeError, ValueError):
            raise ValueError(f"'{campo}' debe ser numérico.") from None
        if not minimo <= valor <= maximo:
            raise ValueError(f"'{campo}' debe estar entre {minimo} y {maximo}.")
        limpios[campo] = valor
    return limpios


def predecir(temperatura: float, frecuencia_cardiaca: float, dolor: float, dias_sintomas: float) -> Prediccion:
    puntaje = (
        _puntos_temperatura(temperatura)
        + _puntos_frecuencia(frecuencia_cardiaca)
        + _puntos_dolor(dolor)
    )
    if puntaje == 0:
        estado = NO_ENFERMO
    elif dias_sintomas >= DIAS_CRONICO:
        estado = CRONICA
    elif puntaje >= PUNTAJE_AGUDO:
        estado = AGUDA
    else:
        estado = LEVE
    return Prediccion(estado=estado, puntaje=puntaje)
