from json import load
from statistics import mean
from sys import argv
from copy import deepcopy

with open(argv[1]) as f:
    results = load(f)

def analysis(experiment, filter_nb_deps=None):
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
    if filter_nb_deps is not None:
        trials = list(filter(lambda t: nb_deps(t) == filter_nb_deps, trials))
    if not trials:
        print("Warning: no data points for experiment '%s' with filter_nb_deps=%d" % (experiment, filter_nb_deps))
        return
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

def full_analysis(experiment, label):
    print("%s:" % label)
    analysis(experiment)
    print()

full_analysis("deploy_deps", "Deploy_deps")
full_analysis("update_no_server", "Update_no_server")
full_analysis("deploy_server", "Deploy_server")
full_analysis("update_with_server", "Update_with_server")

print()
print("Split by number of dependencies:")
print()

def split_analysis(experiment, label):
    for nb_deps in [1, 5, 10]:
        print("%s (%d):" % (label, nb_deps))
        analysis(experiment, nb_deps)
        print()

split_analysis("deploy_deps", "Deploy_deps")
split_analysis("update_no_server", "Update_no_server")
split_analysis("deploy_server", "Deploy_server")
split_analysis("update_with_server", "Update_with_server")
