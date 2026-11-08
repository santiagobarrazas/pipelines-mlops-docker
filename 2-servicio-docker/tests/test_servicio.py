import pytest

from app.main import app
from app.modelo import AGUDA, CRONICA, LEVE, NO_ENFERMO, predecir, validar

CASOS = [
    ({"temperatura": 36.6, "frecuencia_cardiaca": 75, "dolor": 0, "dias_sintomas": 0}, NO_ENFERMO),
    ({"temperatura": 37.8, "frecuencia_cardiaca": 85, "dolor": 3, "dias_sintomas": 2}, LEVE),
    ({"temperatura": 39.5, "frecuencia_cardiaca": 125, "dolor": 8, "dias_sintomas": 3}, AGUDA),
    ({"temperatura": 37.0, "frecuencia_cardiaca": 80, "dolor": 5, "dias_sintomas": 180}, CRONICA),
]


@pytest.mark.parametrize("entradas, esperado", CASOS)
def test_cada_estado_es_alcanzable(entradas, esperado):
    assert predecir(**entradas).estado == esperado


@pytest.mark.parametrize("datos", [
    {"frecuencia_cardiaca": 80, "dolor": 1, "dias_sintomas": 1},
    {"temperatura": "abc", "frecuencia_cardiaca": 80, "dolor": 1, "dias_sintomas": 1},
    {"temperatura": 50, "frecuencia_cardiaca": 80, "dolor": 1, "dias_sintomas": 1},
])
def test_validar_rechaza_entradas_invalidas(datos):
    with pytest.raises(ValueError):
        validar(datos)


def test_api_y_formulario():
    cliente = app.test_client()
    entradas, esperado = CASOS[2]
    resp = cliente.post("/predecir", json=entradas)
    assert resp.status_code == 200 and resp.get_json()["estado"] == esperado
    assert cliente.post("/predecir", json={"dolor": 2}).status_code == 400
    assert esperado in cliente.post("/", data=entradas).get_data(as_text=True)
    assert cliente.get("/salud").get_json() == {"estado": "ok"}
