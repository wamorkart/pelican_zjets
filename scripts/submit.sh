#!/bin/bash

#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -n 64
#SBATCH --ntasks-per-node 4
#SBATCH --gpus-per-task 1
#SBATCH -t 22:00:00
#SBATCH -A m3246
#SBATCH --gpu-bind=none
#SBATCH --module=gpu,nccl-2.18
#SBATCH --mail-user=twamorkar@lbl.gov

module load conda
conda activate zjets
#pretraining
echo srun -torchrun --nproc_per_node=4 top_tagging.py --batch_size=32 --epochs=35 --warmup_epochs=5  --n_layers=6 --n_hidden=72 --lr=0.001  --c_weight=0.005 --dropout=0.2 --weight_decay=0.01 --exp_name=zjets_fullstats_20082024 --datadir data/zjets_14082024/
srun -torchrun --nproc_per_node=4 top_tagging.py --batch_size=32 --epochs=35 --warmup_epochs=5  --n_layers=6 --n_hidden=72 --lr=0.001  --c_weight=0.005 --dropout=0.2 --weight_decay=0.01 --exp_name=zjets_fullstats_20082024 --datadir data/zjets_14082024/
