import yaml

def load_agent(path):

    with open(path, "r") as file:
        return yaml.safe_load(file)
