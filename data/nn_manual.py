import math

# Pesos por defecto
w_ih = [[0.1, 0.2],
        [0.3, 0.4]]
w_ho = [0.5, 0.6]
learning_rate = 0.25

# Dataset de ejemplo
dataset = [
    {"x": [0.0, 0.0], "y": 0},
    {"x": [0.0, 1.0], "y": 1},
    {"x": [1.0, 0.0], "y": 1},
    {"x": [1.0, 1.0], "y": 0},
]

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

def sigmoid_derivative(out):
    return out * (1 - out)

def run_manual():
    global w_ih, w_ho
    for i, sample in enumerate(dataset, start=1):
        x1, x2 = sample["x"]
        y_true  = sample["y"]

        # Forward hidden
        net_h = [w_ih[0][0]*x1 + w_ih[0][1]*x2,
                 w_ih[1][0]*x1 + w_ih[1][1]*x2]
        out_h = [sigmoid(n) for n in net_h]

        # Forward output
        net_o = w_ho[0]*out_h[0] + w_ho[1]*out_h[1]
        out_o = sigmoid(net_o)

        # Backprop
        error_o = y_true - out_o
        delta_o = error_o * sigmoid_derivative(out_o)
        delta_h = [delta_o * w_ho[j] * sigmoid_derivative(out_h[j]) for j in range(2)]

        # Update weights
        w_ho = [w_ho[j] + learning_rate * delta_o * out_h[j] for j in range(2)]
        w_ih = [
            [w_ih[j][0] + learning_rate * delta_h[j] * x1,
             w_ih[j][1] + learning_rate * delta_h[j] * x2]
            for j in range(2)
        ]

        # Mostrar paso
        print(f"\n=== Paso {i} ===")
        print("Entrada:", sample["x"], "Salida esperada:", y_true)
        print("net_h:", net_h, "out_h:", [round(v,3) for v in out_h])
        print("net_o:", round(net_o,3), "out_o:", round(out_o,3))
        print("delta_o:", round(delta_o,3), "delta_h:", [round(d,3) for d in delta_h])
        print("w_ih:", [[round(v,3) for v in row] for row in w_ih])
        print("w_ho:", [round(v,3) for v in w_ho])

    print("\nPesos finales:")
    print("w_ih:", [[round(v,3) for v in row] for row in w_ih])
    print("w_ho:", [round(v,3) for v in w_ho])

if __name__ == "__main__":
    run_manual()
