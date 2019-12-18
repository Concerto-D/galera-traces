#!/usr/bin/python3

import time, datetime
from typing import Dict, Tuple, List, Set

from concerto.all import *

from server import Server
from dep import Dep


class ServerDeps(Assembly):
    # deps_times: for each dependency, [config time on server, allocation time on dep, update time on dep]
    def __init__(self, d_sa : float, d_sc : List[float], d_sr : float, d_ss : List[float], d_sp : List[float], d_di : List[float], d_dr : List[float], d_du : List[float]):
        Assembly.__init__(self)
        self.server = Server(d_sa, d_sc, d_sr, d_ss, d_sp)
        self.nb_deps = len(d_sc)
        self.deps = [Dep(i, d_di[i], d_dr[i], d_du[i]) for i in range(self.nb_deps)]
            
    @staticmethod
    def dep_name(i : int):
        return "dep%d"%i
    
    def deploy_deps(self):
        for i in range(len(self.deps)):
            self.add_component(self.dep_name(i), self.deps[i])
            self.push_b(self.dep_name(i), 'deploy')
        self.wait_all()
        self.synchronize()
            
    
    def deploy_server(self):
        self.add_component('server', self.server)
        for i in range(len(self.deps)):
            self.connect(self.dep_name(i), 'service',
                         'server', Server.name_for_dep_service(i))
            self.connect(self.dep_name(i), 'ip',
                         'server', Server.name_for_dep_ip(i))
        self.push_b('server', 'deploy')
        self.wait('server')
        self.synchronize()
        
    def update_no_server(self):
        for i in range(len(self.deps)):
            self.push_b(self.dep_name(i), 'update')
            self.push_b(self.dep_name(i), 'deploy')
        self.wait_all()
        self.synchronize()
        
    def update_with_server(self):
        self.push_b('server', 'suspend')
        for i in range(len(self.deps)):
            self.push_b(self.dep_name(i), 'update')
        
        self.push_b('server', 'deploy')
        for i in range(len(self.deps)):
            self.push_b(self.dep_name(i), 'deploy')
        self.wait('server')
        self.synchronize()


def measure_time(fn):
    start_time : float = time.perf_counter()
    fn()
    end_time : float = time.perf_counter()
    return end_time-start_time


def deploy_deps_ansible_time(d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    nb_deps = len(d_sc)
    return max([d_di[i] for i in range(nb_deps)])+max([d_dr[i] for i in range(nb_deps)])

def deploy_deps_aeolus_time(d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    nb_deps = len(d_sc)
    return max([d_di[i]+d_dr[i] for i in range(nb_deps)])

def deploy_deps_concerto_time(d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    return deploy_deps_aeolus_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du)


def update_no_server_ansible_time(d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    nb_deps = len(d_sc)
    return sum([d_du[i] for i in range(nb_deps)])+max([d_dr[i] for i in range(nb_deps)])

def update_no_server_aeolus_time(d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    nb_deps = len(d_sc)
    return max([d_du[i]+d_dr[i] for i in range(nb_deps)])

def update_no_server_concerto_time(d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    return update_no_server_aeolus_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du)


def deploy_server_ansible_time(d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    nb_deps = len(d_sc)
    return d_sa+sum([d_sc[i] for i in range(nb_deps)])+d_sr

def deploy_server_aeolus_time(d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    return deploy_server_ansible_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du)

def deploy_server_concerto_time(d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    nb_deps = len(d_sc)
    return d_sa+max([d_sc[i] for i in range(nb_deps)])+d_sr


def update_with_server_ansible_time(d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    nb_deps = len(d_sc)
    return sum([d_du[i]+d_ss[i]+d_sp[i] for i in range(nb_deps)])+max([d_dr[i] for i in range(nb_deps)])+d_sr

def update_with_server_aeolus_time(d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    nb_deps = len(d_sc)
    return max(
        max([d_du[i]+sum([d_ss[j] for j in range(i+1)])+d_dr[i] for i in range(nb_deps)]),
        d_sr+sum([d_ss[i]+d_sp[i] for i in range(nb_deps)])
    )

def update_with_server_concerto_time(d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    nb_deps = len(d_sc)
    return max(
        max([d_du[i]+d_ss[i]+d_dr[i] for i in range(nb_deps)]),
        d_sr+max([d_ss[i]+d_sp[i] for i in range(nb_deps)])
    )
    
    

def time_test(verbosity : int = -1, printing : bool = True, print_time : bool = False,
              d_sa=1., d_sc=[1.], d_sr=1., d_ss=[1.], d_sp=[1.], d_di=[1.], d_dr=[1.], d_du=[1.]):
    
    nb_deps = len(d_sc)
    sda = ServerDeps(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du)
    sda.set_verbosity(verbosity)
    sda.set_print_time(print_time)
    
    deploy_deps_time = measure_time(sda.deploy_deps)
    update_no_server_time = measure_time(sda.update_no_server)
    deploy_server_time = measure_time(sda.deploy_server)
    update_with_server_time = measure_time(sda.update_with_server)
    
    sda.terminate()
    
    return {
        "nb_deps": len(d_sc),
        "durations": {
            "d_sa": d_sa,
            "d_sc": d_sc,
            "d_sr": d_sr,
            "d_ss": d_ss,
            "d_sp": d_sp,
            "d_di": d_di,
            "d_dr": d_dr,
            "d_du": d_du
        },
        "real": {
            "concerto": {
                "deploy_deps": deploy_deps_time,
                "update_no_server": update_no_server_time,
                "deploy_server": deploy_server_time,
                "update_with_server": update_with_server_time,
            }
        },
        "theory": {
            "ansible": {
                "deploy_deps": deploy_deps_ansible_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du),
                "update_no_server": update_no_server_ansible_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du),
                "deploy_server": deploy_server_ansible_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du),
                "update_with_server": update_with_server_ansible_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du),
            },
            "aeolus": {
                "deploy_deps": deploy_deps_aeolus_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du),
                "update_no_server": update_no_server_aeolus_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du),
                "deploy_server": deploy_server_aeolus_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du),
                "update_with_server": update_with_server_aeolus_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du),
            },
            "concerto": {
                "deploy_deps": deploy_deps_concerto_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du),
                "update_no_server": update_no_server_concerto_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du),
                "deploy_server": deploy_server_concerto_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du),
                "update_with_server": update_with_server_concerto_time(d_sa, d_sc, d_sr, d_ss, d_sp, d_di, d_dr, d_du),
            }
        }
    }


def random_tests(nb_trials, min_value=0., max_value=10.):
    from random import uniform
    from json import dumps
    from sys import stderr
    results = []
    for nb_deps in [1,5,10]:
        for i in range(nb_trials):
            print("Trial %d/%d (%d deps)"%(i+1,nb_trials, nb_deps), file=stderr)
            d_sa  = uniform(min_value,max_value)
            d_sc  = [uniform(min_value,max_value) for i in range(nb_deps)]
            d_sr  = uniform(min_value,max_value)
            d_ss  = [uniform(min_value,max_value) for i in range(nb_deps)]
            d_sp  = [uniform(min_value,max_value) for i in range(nb_deps)]
            d_di  = [uniform(min_value,max_value) for i in range(nb_deps)]
            d_dr  = [uniform(min_value,max_value) for i in range(nb_deps)]
            d_du  = [uniform(min_value,max_value) for i in range(nb_deps)]
            trial = {
                "d_sa": d_sa,
                "d_sc": d_sc,
                "d_sr": d_sr,
                "d_ss": d_ss,
                "d_sp": d_sp,
                "d_di": d_di,
                "d_dr": d_dr,
                "d_du": d_du
            }
            res = time_test(verbosity=-1, printing = False, print_time = False,
                        d_sa=d_sa, d_sc=d_sc, d_sr=d_sr, d_ss=d_ss, d_sp=d_sp, d_di=d_di, d_dr=d_dr, d_du=d_du)
            results.append(res)
    print(dumps(results, indent='\t'))
    

if __name__ == '__main__':
    from sys import argv
    nb_tests = int(argv[1])
    assert(nb_tests > 0)
    random_tests(nb_tests)
