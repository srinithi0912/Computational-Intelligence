import pandas as pd

# --------------------------
# Generate dataset (MANUAL)
# --------------------------
def generate_data(n, mode, operation):
    if mode == "binary":
        values = [0, 1]
    else:
        values = [-1, 1]

    data = []

    # Manual generation using binary counting
    total = 2 ** n
    for i in range(total):
        x = []
        num = i

        for _ in range(n):
            x.append(values[num % 2])
            num //= 2

        x = x[::-1]  # reverse to get correct order

        # Compute target
        if operation == "AND":
            t = min(x)
        elif operation == "OR":
            t = max(x)
        elif operation == "NAND":
            t = 1 if min(x) == 0 else 0 if mode == "binary" else -1
        elif operation == "NOR":
            t = 1 if max(x) == 0 else 0 if mode == "binary" else -1
        elif operation == "NOT":
            t = -x[0] if mode == "bipolar" else 1 - x[0]

        data.append(x + [t])

    columns = [f"x{i+1}" for i in range(n)] + ["target"]
    return pd.DataFrame(data, columns=columns)


# --------------------------
# Activation function
# --------------------------
def activation(net, mode):
    if mode == "binary":
        return 1 if net >= 0 else 0
    else:
        return 1 if net >= 0 else -1


# --------------------------
# Training function
# --------------------------
def train_perceptron(df, n, alpha, epochs, mode):
    weights = [0] * n
    bias = 0

    for epoch in range(epochs):
        print(f"\nEpoch {epoch+1}")
        print("-"*50)

        table = []
        correct_count = 0   # track correct outputs

        for _, row in df.iterrows():
            x = row[:-1].values
            t = row["target"]

            net = sum(w*x_i for w, x_i in zip(weights, x)) + bias
            y = activation(net, mode)

            #error = t - y

            # Update weights
            if y != t:
               for i in range(n):
                  weights[i] += alpha * t * x[i]
               bias += alpha * t

            # Count correct predictions
            if y == t:
                correct_count += 1

            table.append(list(x) + [t, net, y, weights.copy(), bias])

        columns = [f"x{i+1}" for i in range(n)] + \
                  ["target", "net", "y", "weights", "bias"]

        print(pd.DataFrame(table, columns=columns))

        # Proper convergence check
        if correct_count == len(df):
            print(f"\nTraining converged at Epoch {epoch+1}")
            break

    print("\nFinal Weights:", weights)
    print("Final Bias:", bias)


# --------------------------
# MAIN PROGRAM
# --------------------------
n = int(input("Enter number of inputs (n): "))
mode = input("Enter mode (binary/bipolar): ")
operation = input("Enter operation (AND/OR/NAND/NOR/NOT): ")
alpha = float(input("Enter learning rate: "))
epochs = int(input("Enter number of epochs: "))

df = generate_data(n, mode, operation)

# Save dataset
df.to_csv("dataset.csv", index=False)
print("\nGenerated Dataset:\n", df)

train_perceptron(df, n, alpha, epochs, mode)
