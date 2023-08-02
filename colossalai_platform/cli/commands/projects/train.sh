#!/usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# ===================================================================
#                Welcome to ColossalAI Platform!
#
#     This script would be executed by our distributed jobs.
# ===================================================================
# The following builtin environment variables are provided:
#
# PROJECT_DIR, DATASET_DIR, MODEL_DIR, OUTPUT_DIR
#
# Pass them to your torchrun script as you like.
#
# ===================================================================
# All hyperparameters would be injected as environment vaiables.
#
# They are defined in HyperParameters.json, check it for more details.
#
# The hyperparameters would be simply passed by name,
# in this starter script, it's ${epoch}.
#
# ===================================================================
# Also, there are some path conventions:
#
# $OUTPUT_DIR/tensorboard:
#     The platform-builtin tensorboard expects events to be here.
# $OUTPUT_DIR/checkpoint
#     The platform-builtin checkpoint recovery feature
#     expects the checkpoint to be here.
#
# ===================================================================

torchrun --nnodes ${NNODES} \
    --nproc_per_node ${NPROC_PER_NODE} \
    --node_rank ${NODE_RANK} \
    --master_addr ${MASTER_ADDR} \
    --master_port ${MASTER_PORT} \
    ${SCRIPT_DIR}/train.py \
    --epoch ${epoch} \
    --project_dir ${PROJECT_DIR} \
    --dataset_dir ${DATASET_DIR} \
    --model_dir ${MODEL_DIR} \
    --output_dir ${OUTPUT_DIR}

# TODO: add more argument passing here
