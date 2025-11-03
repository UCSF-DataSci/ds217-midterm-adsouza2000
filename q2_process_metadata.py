#!/usr/bin/env python3

import random

# Parse key=value config file into dictionary
def parse_config(filepath: str) -> dict:
    config = {}
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if "=" in line:
                key, value = line.split("=")
                config[key.strip()] = int(value.strip())
    return config


# Validate configuration values
def validate_config(config: dict) -> dict:
    results = {}

    results['sample_data_rows'] = isinstance(config.get('sample_data_rows'), int) and config['sample_data_rows'] > 0
    results['sample_data_min'] = isinstance(config.get('sample_data_min'), int) and config['sample_data_min'] >= 1
    results['sample_data_max'] = isinstance(config.get('sample_data_max'), int) and config['sample_data_max'] > config['sample_data_min']

    return results


# Generate random sample data
def generate_sample_data(filename: str, config: dict) -> None:
    rows = config['sample_data_rows']
    min_v = config['sample_data_min']
    max_v = config['sample_data_max']

    with open(filename, 'w') as file:
        for _ in range(rows):
            num = random.randint(min_v, max_v)
            file.write(str(num) + "\n")


# Calculate basic statistics
def calculate_statistics(data: list) -> dict:
    count = len(data)
    _sum = sum(data)
    mean = _sum / count

    sorted_data = sorted(data)
    mid = count // 2
    if count % 2 == 1:
        median = sorted_data[mid]
    else:
        median = (sorted_data[mid - 1] + sorted_data[mid]) / 2

    return {"count": count, "sum": _sum, "mean": mean, "median": median}


# MAIN EXECUTION
if __name__ == '__main__':
    config = parse_config("q2_config.txt")
    validation = validate_config(config)

    print("Validation Results:", validation)

    if not all(validation.values()):
        print("❌ Invalid configuration. Please fix q2_config.txt")
        exit(1)

    data_file = "data/sample_data.csv"
    generate_sample_data(data_file, config)

    with open(data_file, 'r') as f:
        nums = [int(x.strip()) for x in f.readlines()]

    stats = calculate_statistics(nums)

    with open("output/statistics.txt", "w") as f:
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

    print("✅ Q2 complete! Sample data + statistics created.")
