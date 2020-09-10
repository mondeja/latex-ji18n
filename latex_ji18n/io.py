import hashlib

import ruamel.yaml as yaml


def read_yaml_file(filepath, default_content={}):
    with open(filepath, "r", encoding="utf-8") as f:
        content = yaml.safe_load(f) or default_content
    return content


def file_md5(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
