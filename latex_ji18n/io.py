import ruamel.yaml as yaml


def read_yaml_file(filepath, default_content={}):
    with open(filepath, "r", encoding="utf-8") as f:
        content = yaml.safe_load(f) or default_content
    return content
