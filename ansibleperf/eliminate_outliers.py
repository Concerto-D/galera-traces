import json
import sys
from statistics import mean, median


with open(sys.argv[1]) as f:
    data = json.load(f)["log"]
nb = int(sys.argv[2])


data2 = sorted([r["overhead"] for r in data])
data2 = data2[:-nb]

results = {
    "min_overhead": min(data2),
    "max_overhead": max(data2),
    "mean_overhead": mean(data2),
    "median_overhead": median(data2),
    "nb_attempts": len(data2)
}

print(json.dumps(results, indent='\t'))
