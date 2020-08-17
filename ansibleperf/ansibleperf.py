import json
from reserve_g5k import G5kReservation
from remote_host import RemoteHost
from random import randint


g5k = G5kReservation("conf.yaml")
hosts = [h["address"] for h in g5k.get_hosts_info()]

host_times = dict()

for h in hosts:
    sleep_time = randint(0,10)
    host_times[h] = sleep_time
    remote = RemoteHost(h)
    remote.run("cd ~; echo %d > time.txt" % sleep_time)
    
print (json.dumps(host_times))
g5k.run_ansible(["playbook.yaml"])

