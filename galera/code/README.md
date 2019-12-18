# Galera experiments

The scripts of the experiment itself are located in the following Git repository:
https://gitlab.inria.fr/mchardet/galera-experiment (in the paper, commit c1f1dd86
was used).
The `get_figures.sh` Bash script generates the figures after the experiments were
performed (see Instructions).
`get_figure1bis_data.py` and `get_figure2bis_data.py` add to the results the
estimated running times using the formulas obtained using the performance model of
Concerto.
`get_bar_chart.py` is used by `get_figures.sh` to generate the actual figures
using the retrieved data.


## Instructions

The experiment scripts were designed to use the Grrid'5000 experimental platform.
Please contact the authors for help to run the experiments on another infrastructure.

1. Make sure you have a valid Grid'5000 account.

2. Log in to the front-end machine of the site you are going to use for your
experiments. Clone in your home directory the Git repositories of both Concerto
and the experiments:
  - https://gitlab.inria.fr/VeRDi-project/concerto (commit b312641e)
  - https://gitlab.inria.fr/mchardet/galera-experiment (commit c1f1dd86)
From now on, everything will be done on the Grid'5000 front-end node.

3. Make sure that all the requirements of Concerto are installed (using
`pip install -i <path to req>`, where `<path to req>` is a path to the
`requirements.txt` file in the concerto directory).

4. Repeat the previous step with the `requirements.txt` file inside the
`galera-experiment` folder.
  
5. Inside the `galera-experiment` directory, create a `.python-grid5000.yaml`
file containing the following content:
```
username: USERNAME
password: PASSWORD
```
where `USERNAME` and `PASSWORD` are your Grid'5000 username and password. This is
required by the Enoslib library to make a reservation of Grid'5000 from a node other
than the front-end node of a site, which is done for the experiments with Ansible.

6. Make sure the concerto directory is in `$PYTHONPATH`, either by going to the
concerto directory and executing `source source_dir.sh`, by installing Concerto
using the `setup.py` file in its directory or by adding it yourself.

7. Make an OAR reservation on the cluster you want to use with at least 24 nodes.
The expected total running time with default parameters is approximatly 3 days.
Because the experiment uses a sweeper saved on disk, you can stop them and
resume later without losing the previous results.

8. Copy one of the `conf_<site>.yaml` files as `conf.yaml` and edit it so that
the site and cluster correspond to the ones you are using. Also, edit the
number given as part of the `oargrid_jobids` parameter so that it matches your
OAR reservation ID.

9. Run `python3 reserve.py`. We recommend to use a tool like `screen` so that you
are able to cut your SSH connection to the front-end server during the experiment.

10. The results of all the runs are available in the `galera-experiment/exp` folder.
They will be automatically retrieved by the analysis scripts.

11. On your local machine, run the `./get_figures.sh <site>` command where `<site>`
is the Grid'5000 site on which you did the experiments. The figures from the article
will be generated using the results you obtained, as well as additional files
containing information about the results in a folder with the name of the Grid'5000
site.
