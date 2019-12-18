import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import json
from sys import argv


if len(argv) > 3:
    #matplotlib.use('Agg')
    pass

with open("%s/figure%sbis_data.json" % (argv[1], argv[2])) as f:
    figure_data = json.load(f)

if argv[2] == "1":
    x_labels = [3, 5, 10, 20]
else:
    x_labels = [1, 5, 10, 20]

data_sets = [
    {
        "key": "ansible",
        "name": "Ansible",
        "color": "#0080FF",
        "hatch": None,
        "values": {}
    },
    {
        "key": "aeolus",
        "name": "Aeolus",
        "color": "#BF3030",
        "hatch": None,
        "values": {}
    },
    {
        "key": "predicted-aeolus",
        "name": "Aeolus (est.)",
        "color": "#FF4040",
        "hatch": "/////",
        "values": {}
    },
    {
        "key": "concerto",
        "name": "Concerto",
        "color": "#008000",
        "hatch": None,
        "values": {}
    },
    {
        "key": "predicted-concerto",
        "name": "Concerto (est.)",
        "color": "#00CC00",
        "hatch": "/////",
        "values": {}
    },
]

# Light blue: #75BAFF

for set_info in data_sets:
    set_info["values"] = figure_data[set_info["key"]]

nb_groups = len(x_labels)
ind = np.arange(nb_groups)  # the x locations for the groups
nb_elems = len(data_sets)
width = 0.14  # the width of the bars

fig, ax = plt.subplots(figsize=(4, 5))
rects = [ax.bar(
    ind + (-((nb_elems-1)/2)+i)*width,
    [data_sets[i]["values"][str(x)]["mean"] for x in x_labels],
    width,
    yerr=[data_sets[i]["values"][str(x)]["sd"] for x in x_labels],
    label=data_sets[i]["name"],
    color=data_sets[i]["color"],
    alpha=0.9999999,
    hatch=data_sets[i]["hatch"])
    for i in range(nb_elems)]

# Add some text for labels, title and custom x-axis tick labels, etc.
if argv[2] == "1":
    ax.set_xlabel('Size of the cluster')
else:
    ax.set_xlabel('Number of nodes added')
ax.set_ylabel('Time (s)')
ax.set_ylim(ymin=20)
# ax.set_title('Scores by group and gender')
ax.set_xticks(ind)
ax.set_xticklabels(x_labels)
ax.legend()


fig.tight_layout()

if len(argv) > 3:
    # pp = PdfPages(argv[3])
    # plt.savefig(pp, format='pdf', bbox_inches='tight')
    # pp.close()
    plt.savefig(argv[3], bbox_inches='tight', pad_inches=0)
else:
    plt.show()


AEOLUS_SET = 1
AEOLUS_EST_SET = 2
CONCERTO_SET = 3
CONCERTO_EST_SET = 4
print("== Concerto ==")
for x in x_labels:
    real = data_sets[CONCERTO_SET]["values"][str(x)]["mean"]
    pred = data_sets[CONCERTO_EST_SET]["values"][str(x)]["mean"]
    diff = abs(real-pred)
    diffp = (diff/real)*100
    print("- difference %d: %fs (%f%%)" % (x, diff, diffp))
print()
print("== Aeolus ==")
for x in x_labels:
    real = data_sets[AEOLUS_SET]["values"][str(x)]["mean"]
    pred = data_sets[AEOLUS_EST_SET]["values"][str(x)]["mean"]
    diff = abs(real-pred)
    diffp = (diff/real)*100
    print("- difference %d: %fs (%f%%)" % (x, diff, diffp))
