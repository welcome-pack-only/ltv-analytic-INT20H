import yaml


def get_config(path_to_config: str):
    with open(path_to_config, "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config
