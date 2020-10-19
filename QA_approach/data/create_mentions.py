import json

injson = "data/input/data_set_citation.json"
outjson = "data/output/data_set_mentions.json"

with open(injson, "r") as jsonfile:
    citations = json.load(jsonfile)
mentions = []
print(citations[0])
for citation in citations:
    for mention in citation["mention_list"]:
        mentions.append({
            "publication_id" : citation["citation_id"],
            "mention" : mention,
            "score" : 0
        })
with open(outjson, "w") as outfile:
    json.dump(mentions, outfile, indent=4)
