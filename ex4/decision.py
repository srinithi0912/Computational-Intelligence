import csv
import math
from collections import Counter, defaultdict

with open("LaptopPrice dataset.csv","r") as file:
    reader = csv.reader(file)
    data = list(reader)

features = data[0]
records = data[1:]
target_index = len(features) - 1

def calculate_entropy_with_steps(target_values):
    count = Counter(target_values)
    total = sum(count.values())
    entropy = 0
    
    print("   Log Calculations:")
    for cls, value in count.items():
        p = value / total
        log_val = math.log2(p)
        entropy_part = -p * log_val
        entropy += entropy_part
        
        print(f"      -({value}/{total}) * log2({value}/{total}) "
              f"= -({round(p,4)}) * ({round(log_val,4)}) "
              f"= {round(entropy_part,4)}")
    
    print(f"   Final Entropy = {round(entropy,4)}\n")
    return entropy

# Total dataset entropy
target_values = [row[target_index] for row in records]
print("\n========== TOTAL DATASET ENTROPY ==========")
total_entropy = calculate_entropy_with_steps(target_values)

all_info_gain = {}

# For each feature
for i in range(len(features) - 1):
    feature_name = features[i]
    print(f"\n\n========== FEATURE: {feature_name} ==========")

    # Frequency table storage
    freq_table = defaultdict(lambda: Counter())

    # Build frequency table
    for row in records:
        feature_val = row[i]
        target_val = row[target_index]
        freq_table[feature_val][target_val] += 1

    # Get all target classes
    target_classes = set(target_values)

    # Print header
    print("\nFrequency Table:")
    header = "Value\t" + "\t".join(target_classes)
    print(header)

    total_counts = Counter()

    # Print rows
    for value in freq_table:
        row_output = value
        for cls in target_classes:
            count = freq_table[value][cls]
            total_counts[cls] += count
            row_output += f"\t{count}"
        print(row_output)

    # Print totals
    total_row = "Total"
    for cls in target_classes:
        total_row += f"\t{total_counts[cls]}"
    print(total_row)

    # Calculate weighted entropy
    weighted_entropy = 0
    print("\nEntropy Calculations Per Value:")

    for value in freq_table:
        subset = []
        for cls in freq_table[value]:
            subset += [cls] * freq_table[value][cls]

        print(f"\nValue = {value}")
        subset_entropy = calculate_entropy_with_steps(subset)
        weight = len(subset) / len(records)
        weighted_entropy += weight * subset_entropy

    info_gain = total_entropy - weighted_entropy
    all_info_gain[feature_name] = info_gain

    print(f"Information Gain ({feature_name}) = {round(info_gain,4)}")

# Root node
root = max(all_info_gain, key=all_info_gain.get)

print("\n\n========== FINAL RESULT ==========")
for key, value in all_info_gain.items():
    print(f"{key} : {round(value,4)}")

print(f"\nRoot Node of the decision tree is {root}")
