#!/bin/bash
#SBATCH --job-name=multi_3p_debate
#SBATCH --output=logs/multi_3p_%j.out
#SBATCH --error=logs/multi_3p_%j.err
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu

# 设置环境变量
export CUDA_VISIBLE_DEVICES=0

# 激活conda环境（如果你使用conda的话）
# source ~/miniconda3/etc/profile.d/conda.sh
# conda activate your_env_name

# 或者如果你使用venv
# source /path/to/your/venv/bin/activate

# 设置Python路径
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 创建日志目录
mkdir -p logs

# 打印作业信息
echo "=== Job Information ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Working Directory: $(pwd)"
echo "Start Time: $(date)"
echo "CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"

# 检查GPU状态
echo "=== GPU Information ==="
nvidia-smi

# 运行Python脚本
echo "=== Starting Python Script ==="
python main.py --mode multi_3p

# 打印完成信息
echo "=== Job Completed ==="
echo "End Time: $(date)"
echo "Exit Code: $?" 