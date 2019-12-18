from json import load
from statistics import mean
from sys import argv
from copy import deepcopy

with open(argv[1]) as f:
    results = load(f)

def analysis(experiment):
    def theory_time(trial):
        return trial["theory"]["concerto"][experiment]
    def real_time(trial):
        return trial["real"]["concerto"][experiment]
    def distance(trial):
        real = real_time(trial)
        theory = theory_time(trial)
        assert(real >= theory)
        return real - theory
    def distance_percentage(trial):
        dis = distance(trial)
        theory = theory_time(trial)
        return (dis/theory)*100.
    def nb_deps(trial):
        return trial["nb_deps"]
        
    
    trials = deepcopy(results)
    minimum = min([theory_time(x) for x in trials])
    average = mean([theory_time(x) for x in trials])
    maximum_distance = max([distance(x) for x in trials])
    
    print("Number of elements: %d" % len(trials))
    print("Maximum distance: %fs" % maximum_distance)
    max_percentage_trial = max(trials, key=lambda x: distance_percentage(x))
    print("Maximum distance percentage: %f%% (exec time: %fs)" % (distance_percentage(max_percentage_trial),theory_time(max_percentage_trial)))
    print("Max to Min:       %fs = %f%%"%(minimum, (maximum_distance/minimum)*100.))
    print("Max to Average:   %fs = %f%%"%(average, (maximum_distance/average)*100.))
    trials2 = sorted(trials, key=lambda x: theory_time(x))
    print("Median execution time: %fs" % theory_time(trials2[int(len(trials2)/2)]))
    
    
    

print("=== Comparing Concerto performance predictions to actual time ===")
print()
print("Min: we take the maximum time difference between theory and practice and see how much it represents compared to the instance with the minmium eecution time")
print("Average: we take the maximum time difference between theory and practice and see how much it represents compared to an instance of average eecution time")

print()
print("Deploy_deps:")
analysis("deploy_deps")

print()
print("Update_no_server:")
analysis("update_no_server")

print()
print("Deploy_server:")
analysis("deploy_server")

print()
print("Update_with_server:")
analysis("update_with_server")
