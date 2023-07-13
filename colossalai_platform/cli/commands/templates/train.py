import os

from tensorboard.compat.tensorflow_stub.io.gfile import LocalFileSystem

# ==================================
# ColossalAI Platform Specification
# DO NOT MODIFY!
# Start
# ==================================

# hack to make tensorboard compatible with Cloud File System
delattr(LocalFileSystem, "append")

# Environment variables for your data access
PROJECT_DIR = os.environ['PROJECT_DIR']
DATASET_DIR = os.environ['DATASET_DIR']
OUTPUT_DIR = os.environ['OUTPUT_DIR']
CHECKPOINT_DIR = os.path.join(OUTPUT_DIR, 'checkpoint')
TENSORBOARD_DIR = os.path.join(OUTPUT_DIR, 'tensorboard')


# create directories
def create_if_not_exist(path):
    # create if not exists
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


create_if_not_exist(CHECKPOINT_DIR)
create_if_not_exist(TENSORBOARD_DIR)

# ==================================
# ColossalAI Platform Specification
# DO NOT MODIFY!
# End
# ==================================
