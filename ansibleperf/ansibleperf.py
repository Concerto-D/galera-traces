import json
import time
from reserve_g5k import G5kReservation
from remote_host import RemoteHost
from random import randint


g5k = G5kReservation("conf.yaml")
hosts = [h["address"] for h in g5k.get_hosts_info("default")]

host_times = dict()
expected_time_1 = 0.0
expected_time_2 = 0.0

for h in hosts:
    sleep_time1 = randint(0,10)
    expected_time_1 = max(expected_time_1, sleep_time1)
    sleep_time2 = randint(0,10)
    expected_time_2 = max(expected_time_2, sleep_time2)
    host_times[h] = [sleep_time1, sleep_time2]
    remote = RemoteHost(h)
    remote.run("cd ~; echo %d > time1.txt" % sleep_time1)
    remote.run("cd ~; echo %d > time2.txt" % sleep_time2)

start_time = time.perf_counter()
g5k.run_ansible(["playbook.yaml"])
end_time = time.perf_counter()

print(json.dumps(host_times))
print("Expected total time: %d" % expected_time_1+expected_time_2)
print("Measured total time: %f" % end_time-start_time)
