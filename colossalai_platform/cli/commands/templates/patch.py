def patch_tensorboard():
    try:
        from tensorboard.compat.tensorflow_stub.io.gfile import LocalFileSystem
        # hack to make tensorboard compatible with Cloud File System
        delattr(LocalFileSystem, "append")
    except ImportError:
        print("Tensorboard patch failed. Please check your tensorboard version.")
