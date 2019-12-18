# Synthetic experiments

The `synthetic_experiments.py` Python file runs the synthetic experiments presented in
the paper. These consist in 4 steps: deployment of dependencies, update of these
dependencies, deployment of the server and update of the dependencies while the
server is running. Each transition duration is taken at random between 0 and 10.
`dep.py` and `server.py` contain the description of the components.
`analyze_results.py` gives insights about the results obtained using
`synthetic_experiments.py`.


## Instructions

1. Make sure the concerto directory is in `$PYTHONPATH`, either by going to the
concerto directory and executing `source source_dir.sh`, by installing Concerto
using the `setup.py` file in its directory or by adding it yourself.
2. Run `python3 synthetic_experiments.py <nb_trials> > output.json` where
`<nb_trials>` is the number of trials to run per experiment and per number of
dependencies (1, 5 and 10). By redirecting the standard output to `output.json`,
the latter will contain the results.
3. Run `python3 analyze_results.py output.json` to get information about the
results obtained, in particular the distance between the measured times and the
estimations made using the performance model of Concerto.
