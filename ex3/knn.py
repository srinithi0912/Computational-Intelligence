import csv
import math

def distance_metric(a, b, r):
    total = sum(abs(x - y) ** r for x, y in zip(a, b))
    return total ** (1 / r)

def load_data(filename):
    data = []
    try:
        # Using the [Python csv module documentation](https://docs.python.org) logic
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or len(row) < 2:
                    continue
                try:
                    features = list(map(float, row[:-1]))
                    label = row[-1]
                    data.append((features, label))
                except ValueError:
                    continue
        return data
    except FileNotFoundError:
        print("Error: d.csv not found.")
        return []

def normalize(data):
    feature_count = len(data[0][0])
    mins = [min(row[0][i] for row in data) for i in range(feature_count)]
    maxs = [max(row[0][i] for row in data) for i in range(feature_count)]

    normalized_list = []
    for features, label in data:
        norm_features = []
        for i in range(feature_count):
            if maxs[i] != mins[i]:
                norm_features.append(round((features[i] - mins[i]) / (maxs[i] - mins[i]), 4))
            else:
                norm_features.append(0.0)
        normalized_list.append((features, norm_features, label))

    return normalized_list, mins, maxs

def vote(neighbors, voting_type):
    if voting_type == "1":
        counts = {}
        for _, _, _, label in neighbors:
            counts[label] = counts.get(label, 0) + 1
        return max(counts, key=counts.get)
    else:
        weighted_scores = {}
        for _, _, dist, label in neighbors:
            weight = 1 / (dist + 1e-9)
            weighted_scores[label] = weighted_scores.get(label, 0) + weight
        return max(weighted_scores, key=weighted_scores.get)

def knn(data, query, k, r_value, voting_type, is_normalized):
    distances = []
    for original, normalized, label in data:
        compare_point = normalized if is_normalized else original
        d = distance_metric(compare_point, query, r_value)
        distances.append((original, normalized, d, label))

    distances.sort(key=lambda x: x[2])
    neighbors = distances[:k]

    print(f"\nTop K ({k}) Neighbors Selected:")
    for i, (_, _, d, label) in enumerate(neighbors, 1):
        print(f"{i:<5} | Distance: {d:.4f} | Class: {label}")

    return vote(neighbors, voting_type)

def main():
    data = load_data("dataset1.csv")
    if not data: return

    # Check for Normalization
    needs_norm = any(any(val > 100.0 or val < 0.0 for val in f) for f, _ in data)

    if needs_norm:
        processed_data, mins, maxs = normalize(data)
        print("\n[ SCALING STATUS ]: Normalization Applied")
    else:
        processed_data = [(f, f, l) for f, l in data]
        mins, maxs = [], []

    # 3. Preview Dataset - PRINTING ALL 150 RECORDS
    print("\n[ FULL DATA PREVIEW (Original | Normalized) ]")
    header = f"{'Row':<4} | {'Temperature':<12} | {'litre':<12} | {'MilliLitre':<12} | {'QuantityLevel':<12} | {'Label'}"
    print(header)
    print("-" * len(header))

    for i, (orig, norm, lbl) in enumerate(processed_data, 1):
        # Displays format: Original (Normalized)
        row_str = f"{i:<4} | "
        for j in range(len(orig)):
            val_pair = f"{orig[j]}({norm[j]})"
            row_str += f"{val_pair:<12} | "
        print(row_str + lbl)

    # 4. Interaction Loop
    feature_names = ["Temperature", "litre", "Millilitre", "QuantityLevel"]
    while True:
        print("\n1. Predict \n2. Exit")
        ch = input("Choice: ")
        if ch == "2": break

        try:
            query = [float(input(f"Enter {name}: ")) for name in feature_names]
            final_query = query
            if needs_norm:
                final_query = [(query[i] - mins[i]) / (maxs[i] - mins[i]) if maxs[i] != mins[i] else 0 for i in range(len(query))]

            k = int(input("Enter K: "))
            r_val = 2 if input("Metric (1:Euclidean, 2:Manhattan): ") == "1" else 1
            v_choice = input("Voting (1:Unweighted, 2:Weighted): ")

            result = knn(processed_data, final_query, k, r_val, v_choice, needs_norm)
            print(f"\nFINAL RESULT: {result}")
        except ValueError:
            print("Error: Invalid input.")

if __name__ == "__main__":
    main()
