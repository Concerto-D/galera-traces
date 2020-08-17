import json
import time
from reserve_g5k import G5kReservation
from remote_host import RemoteHost
from random import randint
from statistics import mean, median


NB_ATTEMPTS = 100
MIN_TIME = 0
MAX_TIME = 10


g5k = G5kReservation("conf.yaml")
hosts = [h["address"] for h in g5k.get_hosts_info("default")]
log = []

for i in range(NB_ATTEMPTS):
    host_times = dict()
    expected_time_1 = 0.0
    expected_time_2 = 0.0

    for h in hosts:
        sleep_time1 = randint(MIN_TIME,MAX_TIME)
        expected_time_1 = max(expected_time_1, sleep_time1)
        sleep_time2 = randint(MIN_TIME,MAX_TIME)
        expected_time_2 = max(expected_time_2, sleep_time2)
        host_times[h] = [sleep_time1, sleep_time2]
        remote = RemoteHost(h)
        remote.run("cd ~; echo %d > time1.txt" % sleep_time1)
        remote.run("cd ~; echo %d > time2.txt" % sleep_time2)

    start_time = time.perf_counter()
    g5k.run_ansible(["playbook.yaml"])
    end_time = time.perf_counter()
    
    expected_time = expected_time_1+expected_time_2
    measured_time = end_time-start_time
    overhead = measured_time-expected_time
    
    log.append({
        "expected": expected_time,
        "measured": measured_time,
        "overhead": overhead
    })

results = {
    "min_overhead": min([run["overhead"] for run in log]),
    "max_overhead": max([run["overhead"] for run in log]),
    "mean_overhead": mean([run["overhead"] for run in log]),
    "median_overhead": median([run["overhead"] for run in log]),
    "log": log
}

print(json.dumps(results, indent='\t'))
