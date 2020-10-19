import shutil
import os
import json

DATA_PATH = "../preprocessing/data/processed_text/"
with open("data/train/publications.json") as json1:
    train_files = json.load(json1)
with open("data/dev/publications.json") as json2:
    dev_files = json.load(json2)
with open("data/test/publications.json") as json3:
    test_files = json.load(json3)

train_keys = [i["publication_id"] for i in train_files]
dev_keys = [j["publication_id"] for j in dev_files]
test_files = [k["publication_id"] for k in test_files]

for file in os.listdir(DATA_PATH):
    name = file.split(".")[0]
    if name in train_keys:
        shutil.copyfile(DATA_PATH+file, "data/train/input/files/text/"+file)
        print("Moving %s to training data" %file)
    elif name in test_files:
        shutil.copyfile(DATA_PATH+file, "data/test/input/files/text/"+file)
        print("Moving %s to test data" %file)
    else:
        shutil.copyfile(DATA_PATH+file, "data/dev/input/files/text/"+file)
        print("Moving %s to validation data" %file)