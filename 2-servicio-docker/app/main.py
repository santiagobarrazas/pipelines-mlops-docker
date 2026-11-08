import logging

from flask import Flask, jsonify, render_template, request

from app.modelo import RANGOS, predecir, validar

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("servicio")

app = Flask(__name__)
app.json.ensure_ascii = False


@app.get("/salud")
def salud():
    return jsonify(estado="ok")


@app.route("/", methods=["GET", "POST"])
def formulario():
    resultado, error, valores = None, None, {}
    if request.method == "POST":
        valores = request.form.to_dict()
        try:
            resultado = predecir(**validar(valores))
        except ValueError as exc:
            error = str(exc)
    return render_template("index.html", rangos=RANGOS, valores=valores, resultado=resultado, error=error)


@app.post("/predecir")
def api_predecir():
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify(error="El cuerpo debe ser un objeto JSON."), 400
    try:
        entradas = validar(datos)
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    pred = predecir(**entradas)
    log.info("prediccion estado=%s puntaje=%s", pred.estado, pred.puntaje)
    return jsonify(estado=pred.estado, puntaje_severidad=pred.puntaje, entradas=entradas)
