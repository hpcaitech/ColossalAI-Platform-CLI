# 🔮 <Template-Name>


## 📚 Introduction

To be added by the author

## 📍 Data Preparation

To be added by the author


## 💡 Write Your Own Template

This section will guide you to write your own template.

1. Install ColossalAI Platform CLI `cap` based on the instruction in the [GitHub Page](https://github.com/hpcaitech/ColossalAI-Platform-CLI).

2. Initialize your template

```bash
cap template init <name>
```

3. Migrate your code to the template. We have provided the `train.py` as the common entrypoint. `train.py` contains some pre-defined code which is necessary for the template to work. You should not modify them. If you wnat to use other files as the entrypoint, you should change `train.py` in `train.sh` to your own file name while maintaining the pre-defined code in your own file.

4. Update the `HypeerParameters.json` for your training arguments. This json file defines the arguments which can be configured by the user on the ColossalAI Platform Web UI. An example is given below.

```json
{
    "name": "epoch",
    "types": "string",
    "defaultValue": "10"
}
```

The `name` will be passed to the `train.sh` as an environment variable, i.e. you can do `echo $epoch` in `train.sh`. The `types` can be `string`, `int`, `float`, `bool` and `enum`. The `defaultValue` is the default value of the argument and it is optional.

5. Update `train.sh` which will be invoked by the Platform to start training jobs. You can just change the argument passing part.

6. Add any dependency of your code to the `requirements.txt` for your Python environment.

7. Check and update the `Dockerfile`. This will be used to build the Docker image for your training job. You can add any dependency of your code to the `Dockerfile` for your Docker environment.
