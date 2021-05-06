# notebook

# correlation-engine

Correlation engine is a dream program I wish that existed that let me detect correlations between things that I am doing.

# Correlating hashtags

```
from collections import defaultdict
items = []
items.append("I am mighty #annoyed today #food")
items.append("I am #annoyed at this #software")
items.append("#software makes me #annoyed")
items.append("#food makes me #happy and #hungry")
items.append("#food again #happy")

from scipy.stats import pearsonr, spearmanr
import re
from itertools import combinations

def allequal(data):
    equality = data[0]
    for item in data:
        if item != equality:
            return False
    return True

def correlate_hashags(items):
    keys = set([])
    presences = []
    for item in items:
        match = re.findall("#([A-Za-z0-9]*)", item)
        this_presences = {}
        for matched_item in match:
            this_presences[matched_item] = True
            keys.add(matched_item)
        presences.append(this_presences)
    
    run_correlation = True
    for key, subkey in combinations(keys, 2):
            data1 = []
            data2 = []
            run_correlation = True
            for i, post in enumerate(items):
                data1.append(key in presences[i])
                data2.append(subkey in presences[i])
            if allequal(data1):
                print("Correlation is constant, {} appears everywhere".format(key))
                run_correlation = False
            if allequal(data2):
                print("Correlation is constant, {} appears everywhere".format(subkey))
                run_correlation = False
            if run_correlation:
                corr, _ = pearsonr(data1, data2)
                # print("Testing {} and {} {:03f}".format(key, subkey, corr))
                yield (key, subkey, corr)

corrs = correlate_hashags(items)
for key, subkey, corr in corrs:
    if corr > 0:
        print("{} has a positive correlation with {} @ {:.3f}".format(key, subkey, corr))
    else:
        # print("{} has a negative correlation with {} @ {:.3f}".format(key, subkey, corr))
        print("You don't get {} with {}".format(key, subkey, corr))
```

# Correlate log lines with errors

```
from collections import Counter
from scipy.stats import pearsonr

items = []
items.append("2020-08-16 20:17 Another Innocuous log line")
items.append("2020-08-16 20:17 Log line that causes the error")
items.append("2020-08-16 20:17 ERROR: error caused")
items.append("2020-08-16 20:17 Innocuous log line")
items.append("2020-08-16 20:17 Log line that causes the error")
items.append("2020-08-16 20:17 ERROR: error caused")
items.append("2020-08-16 20:17 Log line that causes the error")
items.append("2020-08-16 20:17 ERROR: error caused")
items.append("2020-08-16 20:17 A third innocuous log line")
items.append("2020-08-16 20:17 Log line that causes the error")
items.append("2020-08-16 20:17 ERROR: error caused")
items.append("2020-08-16 20:17 Log line that causes the error")
items.append("2020-08-16 20:17 Innocuous log line")
items.append("2020-08-16 20:17 ERROR: error caused")
items.append("2020-08-16 20:17 Another cause of error")
items.append("2020-08-16 20:17 Innocuous log line")
items.append("2020-08-16 20:17 ERROR: error caused")
items.append("2020-08-16 20:17 Another cause of error")
items.append("2020-08-16 20:17 Innocuous log line")
items.append("2020-08-16 20:17 ERROR: error caused")
items.append("2020-08-16 20:17 Another cause of error")
items.append("2020-08-16 20:17 ERROR: error caused")
items.append("2020-08-16 20:17 Another cause of error")
items.append("2020-08-16 20:17 ERROR: error caused")

def find_error_cause(items):
    chances = {}
    for scanback in range(0, 10):
        for line in items:
            if "ERROR" in line:
                continue
            errors = []
            logs = []
            log_line_identity = line.split(" ")[2:]
            log_line = " ".join(log_line_identity)
            for _ in range(0, scanback):
                errors.append(0)

            for line in items:
                if "ERROR" in line:
                    errors.append(100)
                else:
                    errors.append(0)

            for line in items:
                if log_line in line:
                    logs.append(100)
                else:
                    logs.append(0)

            for _ in range(0, scanback):
                logs.append(0)

            corr, _ = pearsonr(errors, logs)

            if corr > 0:
                chances[log_line] = chances.get(log_line, 0) + 1
    return Counter(chances).most_common()

            

chances = find_error_cause(items)
print(chances)
```
