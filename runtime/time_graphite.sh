batch_dir=$1

for batch in $batch_dir/*;
do
    echo "Timing: $batch" >> timer.log
    start=$(date +%s%N)
    python ../graphite.py -i $batch -o $batch.out -t 1 -v 250 > /dev/null 2>&1
    stop=$(date +%s%N)
    echo "$batch,$((($stop-$start)/1000000))" >> timer.out
done
