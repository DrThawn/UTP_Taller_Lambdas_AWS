import json

def suma(a, b): return a + b
def resta(a, b): return a - b
def multiplicacion(a, b): return a * b
def division(a, b):
    if b == 0:
        raise ZeroDivisionError("No se puede dividir entre cero")
    return a / b

OPS = {
    "suma": suma,
    "resta": resta,
    "multiplicacion": multiplicacion,
    "division": division,
}

def calculator(a: float, b: float, operation: str):
    op = operation.lower()
    if op not in OPS:
        raise ValueError(f"Operación no soportada: {operation}")
    return OPS[op](a, b)

def _get_calc_data(event):
    # Soporta payload directo o dentro de body (API Gateway proxy)
    if "calculadora" in event:
        return event["calculadora"]
    if "body" in event and event["body"]:
        body = event["body"]
        if isinstance(body, str):
            body = json.loads(body)
        return body["calculadora"]
    raise KeyError("Falta 'calculadora' en el evento")

def lambda_handler(event, context):
    try:
        data = _get_calc_data(event)
        a = float(data["numero1"])
        b = float(data["numero2"])
        ops = data["operacion"]

        # Normaliza: acepta lista, una cadena, o cadena con comas
        if isinstance(ops, str):
            ops_list = [o.strip().lower() for o in ops.split(",")]
        elif isinstance(ops, list):
            ops_list = [str(o).strip().lower() for o in ops]
        else:
            ops_list = [str(ops).strip().lower()]

        results = {}
        print(f"Calculando con a={a}, b={b}: {ops_list}")
        for op in ops_list:
            try:
                res = calculator(a, b, op)
                print(f"{op}: {res}")
                results[op] = res
            except Exception as e:
                print(f"{op}: error -> {e}")
                results[op] = f"error: {e}"

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "OK",
                "a": a,
                "b": b,
                "resultados": results
            }),
        }

    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 400, "body": json.dumps({"message": str(e)})}
