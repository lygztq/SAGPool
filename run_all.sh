#!/bin/bash

for arch in hierarchical, global
do
    for hidden in 16 32 64 128
    do
        for pool_ratio in 0.25 0.5
        do
            for lr in 1e-2 5e-2 1e-3 5e-3 1e-4 5e-4
            do
                for weight_decay in 1e-2, 1e-3, 1e-4, 1e-5
                do
                    for dataset in DD PROTEINS NCI1 NCI109 Mutagenicity
                    do
                        python main.py --epochs 1 --print_every -1 --num_trials 20 --device 0 --architecture ${arch} --hid_dim ${hidden} --pool_ratio ${pool_ratio} --lr ${lr} --weight_decay ${weight_decay} --dataset ${dataset}
                    done
                done
            done
        done
    done
done
