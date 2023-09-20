#!/usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# ===================================================================
#                Welcome to ColossalAI Platform!
# ===================================================================
# Those environment variables would be injected by the runner:
#
# 1. ColossalAI Platform defined ones:
#    PROJECT_DIR, DATASET_DIR, MODEL_DIR, OUTPUT_DIR, SCRIPT_DIR
#
# 2. Required by torchrun:
#    NNODES, NPROC_PER_NODE, NODE_RANK, MASTER_ADDR, MASTER_PORT
#
# 3. Hyperparameters from configuration UI:
#    (check HyperParameters.json for more details)
#
# After that, the runner would execute `train.sh`, this script.
# ===================================================================

torchrun --nnodes ${NNODES} \
    --nproc_per_node ${NPROC_PER_NODE} \
    --node_rank ${NODE_RANK} \
    --master_addr ${MASTER_ADDR} \
    --master_port ${MASTER_PORT} \
    ${SCRIPT_DIR}/train.py \
    --project_dir ${PROJECT_DIR} \
    --dataset_dir ${DATASET_DIR} \
    --model_dir ${MODEL_DIR} \
    --output_dir ${OUTPUT_DIR}

# TODO: add more argument passing here
