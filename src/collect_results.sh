#!/bin/bash

# Run the evaluaiton with each problem ID
for i in {0..7}; do
    python3 run_eval.py ${i}
done

mv out_r*.txt ../results/RandomResults/Output/
mv out_q*.txt ../restuls/QResults/Output/
mv out_s*.txt ../results/SimpleResults/Output/

exit 0
