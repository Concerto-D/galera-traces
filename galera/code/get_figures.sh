if [ -z "$1" ]
  then
    echo "No argument supplied, please provide G5K site"
    exit 1
fi

mkdir -p $1

ssh $1.g5k << EOF
  cd galera-experiment/utils/generate_figures/remote/; 
  bash collect_data.sh
EOF
scp $1.g5k:galera-experiment/utils/generate_figures/remote/figure1_data.json $1/figure1_data.json
scp $1.g5k:galera-experiment/utils/generate_figures/remote/figure1_analysis.txt $1/figure1_analysis.txt
scp $1.g5k:galera-experiment/utils/generate_figures/remote/figure2_data.json $1/figure2_data.json
scp $1.g5k:galera-experiment/utils/generate_figures/remote/figure2_analysis.txt $1/figure2_analysis.txt
scp $1.g5k:galera-experiment/utils/generate_figures/remote/durations.json $1/durations.json

python3 get_figure1bis_data.py $1/figure1_data.json $1/durations.json > $1/figure1bis_data.json
python3 get_figure2bis_data.py $1/figure2_data.json $1/durations.json > $1/figure2bis_data.json
python3 get_bar_chart.py $1 1 $1/chart1.pdf
python3 get_bar_chart.py $1 2 $1/chart2.pdf
