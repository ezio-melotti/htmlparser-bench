import sys
import os
import os.path
import traceback

RESULTSDIR = 'results'

def summarize(filename):
    path = os.path.abspath(os.path.join(RESULTSDIR, filename))
    failures = 0
    successes = 0
    total_size = 0
    total_time = 0
    with open(path) as file:
        for line in file:
            k = line.split("\t")
            if len(k) != 3:
                failures += 1
            else:
                successes += 1
                hostname, time, size = k
                total_size += int(size)
                total_time += float(time)
    percent = 100 - (failures / (failures+successes) * 100)
    percent = " (%.4g%% success)" % percent

    print("%-28s: %4d KB/s%s" % (filename, total_size/total_time/1024, percent))


try:
    results = sorted(os.listdir(RESULTSDIR))
except OSError as e:
    print(repr(e))
    sys.exit('Run benchmark.py to create the result files.')

for result in results:
    if not result.endswith("tsv"):
        continue
    summarize(result)
