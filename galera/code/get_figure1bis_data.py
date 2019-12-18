import json


def compute_predicted_time_aeolus(comp_transitions, trans_val):
    master_time = (
        comp_transitions["master"]["backup"][trans_val] + 
        comp_transitions["master"]["uninstall_stop"][trans_val] + 
        comp_transitions["master"]["uninstall"][trans_val] + 
        comp_transitions["master"]["mount"][trans_val] + 
        comp_transitions["master"]["create_directories"][trans_val] + 
        comp_transitions["master"]["send_config"][trans_val] + 
        comp_transitions["master"]["pull"][trans_val] + 
        comp_transitions["master"]["start"][trans_val] + 
        comp_transitions["master"]["go_ready"][trans_val] + 
        comp_transitions["master"]["restore_run"][trans_val]
    )
    worker_time1 = (
        comp_transitions["workers"]["send_scripts"][trans_val] + 
        comp_transitions["workers"]["mount"][trans_val] + 
        comp_transitions["workers"]["create_directories"][trans_val] + 
        comp_transitions["workers"]["send_config"][trans_val] + 
        comp_transitions["workers"]["pull"][trans_val]
    )
    worker_time2 = (
        comp_transitions["workers"]["start"][trans_val] + 
        comp_transitions["workers"]["go_ready"][trans_val]
    )
    return max(
        master_time,
        max(master_time,worker_time1)+worker_time2
    )


def compute_predicted_time_concerto(comp_transitions, trans_val):
    master_time = (
        comp_transitions["master"]["backup"][trans_val] + 
        comp_transitions["master"]["uninstall_stop"][trans_val] + 
        comp_transitions["master"]["uninstall"][trans_val] + 
        max (
            comp_transitions["master"]["mount"][trans_val] + 
            comp_transitions["master"]["create_directories"][trans_val] + 
            comp_transitions["master"]["send_config"][trans_val]
            ,
            comp_transitions["master"]["pull"][trans_val]
        ) +
        comp_transitions["master"]["start"][trans_val] + 
        comp_transitions["master"]["go_ready"][trans_val] + 
        comp_transitions["master"]["restore_run"][trans_val]
    )
    worker_time1 = (
        comp_transitions["workers"]["send_scripts"][trans_val] + 
        max (
            comp_transitions["workers"]["mount"][trans_val] + 
            comp_transitions["workers"]["create_directories"][trans_val] + 
            comp_transitions["workers"]["send_config"][trans_val]
            ,
            comp_transitions["workers"]["pull"][trans_val]
        )
    )
    worker_time2 = (
        comp_transitions["workers"]["start"][trans_val] + 
        comp_transitions["workers"]["go_ready"][trans_val]
    )
    return max(
        master_time,
        max(master_time,worker_time1)+worker_time2
    )


def generate_new_figure(json_figure, durations_file, durations_reconf):
    with open(json_figure) as f:
        figure = json.load(f)
    with open(durations_file) as f:
        durations = json.load(f)
    
    predicted_times_aeolus = dict()
    predicted_times_concerto = dict()
    for nbc, comp_transitions in durations[durations_reconf].items():
        pt = compute_predicted_time_aeolus(comp_transitions, "mean")
        predicted_times_aeolus[nbc] = {
            "sd": 0.,
            "min": compute_predicted_time_aeolus(comp_transitions, "min"),
            "max": compute_predicted_time_aeolus(comp_transitions, "max"),
            "median": compute_predicted_time_aeolus(comp_transitions, "median"),
            "values": [pt],
            "mean": pt,
            "discarded_values": []
        }
        pt = compute_predicted_time_concerto(comp_transitions, "mean")
        predicted_times_concerto[nbc] = {
            "sd": 0.,
            "min": compute_predicted_time_concerto(comp_transitions, "min"),
            "max": compute_predicted_time_concerto(comp_transitions, "max"),
            "median": compute_predicted_time_concerto(comp_transitions, "median"),
            "values": [pt],
            "mean": pt,
            "discarded_values": []
        }
    figure["predicted-aeolus"] = predicted_times_aeolus
    figure["predicted-concerto"] = predicted_times_concerto
    
    return figure

from sys import argv
if len(argv) != 3:
    print("Error: two argument expected: <figure data>, <durations file>")
print(json.dumps(generate_new_figure(argv[1], argv[2], "reconf1"), indent="\t"))
