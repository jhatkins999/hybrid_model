import json
from collections import defaultdict
from pyld import jsonld
import os

with open("cmr_datasets.json") as jsonfile:
    cmr = json.load(jsonfile)["feed"]
corpus = {
            "@context" : {
                "xml" : "https://cmr.earthdata.nasa.gov/search/collections.json?platform\[\]=Aura&Instrument\[\]=MLS&processing_level_id\[\]=2&version=004&page_size=100"
                         }, # Change this to be a value in config.py
            "@graph" : [],
            "@id" : cmr["id"]
         }
datasets = cmr["entry"] # this is a list
for dataset in datasets:
    corpus["@graph"].append(
        {
            "@id" : dataset["short_name"],
            "@type" : "Dataset",
            "comment" : dataset["summary"],
            "label" : dataset["dataset_id"],
            "title" : [dataset["title"]] + dataset["dif_ids"] + [dataset["short_name"]]
        })
with open("input/publications.json") as json1:
    pubs = json.load(json1)
with open("input/data_set_citation.json") as json2:
    citations = json.load(json2)
lookup = defaultdict(list)
for citation in citations:
    lookup[citation["publication_id"]].append(citation['data_set_id'])

for pub in pubs:
    corpus["@graph"].append({
        "@id" : pub["publication_id"],
        "@type" : "ResearchPublication",
        "cito:citesAsDataSource" : lookup[pub["publication_id"]],
        "title" : pub["title"],
        "pub_date" : pub["pub_date"]
    })

with open("corpus.jsonld", "w") as outfile:
   json.dump(corpus, outfile, indent=4)