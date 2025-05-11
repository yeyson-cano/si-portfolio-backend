import math
from typing import Dict, Any, List

# Puedes definir aquí valores por defecto (del ejemplo del PDF)
DEFAULT_WEIGHTS_IH = [[0.1, 0.2], [0.3, 0.4]]   # ejemplo
DEFAULT_WEIGHTS_HO = [0.5, 0.6]                 # ejemplo
DEFAULT_DATASET = [
    {"x": [0.0, 0.0], "y": 0},
    {"x": [0.0, 1.0], "y": 1},
    {"x": [1.0, 0.0], "y": 1},
    {"x": [1.0, 1.0], "y": 0},
]
DEFAULT_LR = 0.25

def sigmoid(z: float) -> float:
    return 1 / (1 + math.exp(-z))

def sigmoid_derivative(output: float) -> float:
    # dσ/dz = σ(z)*(1-σ(z)), pero si ya tienes σ(z)=output:
    return output * (1 - output)

def _run_nn(params: Dict[str, Any]) -> Dict[str, Any]:
    # 1. Leer parámetros o usar defaults
    w_ih = params.get("w_ih", DEFAULT_WEIGHTS_IH)  # 2×2
    w_ho = params.get("w_ho", DEFAULT_WEIGHTS_HO)  # 2
    data = params.get("dataset", DEFAULT_DATASET)  # lista de {x, y}
    lr = params.get("learning_rate", DEFAULT_LR)

    steps: List[Dict[str, Any]] = []

    # 2. Iterar muestras
    for sample in data:
        x1, x2 = sample["x"]
        y_true = sample["y"]

        # 2.1 Forward pass – capa oculta
        net_h = [
            w_ih[0][0]*x1 + w_ih[1][0]*x2,
            w_ih[0][1]*x1 + w_ih[1][1]*x2
        ]
        out_h = [sigmoid(n) for n in net_h]

        # 2.2 Forward pass – capa salida
        net_o = w_ho[0]*out_h[0] + w_ho[1]*out_h[1]
        out_o = sigmoid(net_o)

        # 2.3 Backward pass – capa salida
        error_o = y_true - out_o
        delta_o = error_o * sigmoid_derivative(out_o)

        # 2.4 Backward pass – capa oculta
        delta_h = [
            delta_o * w_ho[i] * sigmoid_derivative(out_h[i])
            for i in range(2)
        ]

        # 2.5 Actualizar pesos
        # w_ho_new = w_ho + lr * delta_o * out_h
        w_ho = [
            w_ho[i] + lr * delta_o * out_h[i]
            for i in range(2)
        ]
        # w_ih_new[j][i] = w_ih[j][i] + lr * delta_h[j] * x_i
        w_ih = [
            [
                w_ih[0][j] + lr * delta_h[j] * x1,
                w_ih[1][j] + lr * delta_h[j] * x2
            ]
            for j in range(2)
        ]

        # 2.6 Registrar paso
        steps.append({
            "x": [x1, x2],
            "y_true": y_true,
            "net_h": net_h,
            "out_h": out_h,
            "net_o": net_o,
            "out_o": out_o,
            "delta_o": delta_o,
            "delta_h": delta_h,
            "w_ih_updated": w_ih,
            "w_ho_updated": w_ho,
        })

    return {"steps": steps, "final_weights": {"w_ih": w_ih, "w_ho": w_ho}}

def run_nn_manual(params: Dict[str, Any], verbosity: str) -> Dict[str, Any]:
    """
    Ejecuta la red manual capa a capa y devuelve un dict con:
      - history: siempre vacío para NN
      - first_epoch: siempre None para NN
      - final: { steps: [...], final_weights: {...} }
    :param params: { w_ih, w_ho, dataset, learning_rate }
    :param verbosity: "first"|"all"|"final"
    """
    raw = _run_nn(params)
    steps = raw["steps"]

    # Seleccionamos los pasos según verbosity
    if verbosity == "all":
        selected_steps = steps
    elif verbosity == "first":
        selected_steps = steps[:1]
    else:  # "final"
        selected_steps = []

    # Construimos el payload final
    final_payload: Dict[str, Any] = {
        "steps": selected_steps,
        "final_weights": raw["final_weights"],
    }

    return {
        "history": [],
        "first_epoch": None,
        "final": final_payload
    }
