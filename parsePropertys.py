import yaml



def getFileSource():
    with open('genom.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config["file"]["sourcefolder"]
