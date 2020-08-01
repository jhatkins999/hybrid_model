import os
from subprocess import Popen
import argparse
import json
import time
import re
import glob
from collections import defaultdict
from shutil import copyfile
from nltk.corpus import stopwords

from config import params
from utils import *
# from get_pdfs.src.data_utils import * --remove

from pyzotero import zotero


def load_data(load_json, zot_library, collection_id, verbose = params["DEFAULT_VERBOSE"]):
    start_time = time.time()
    if 'data_sets.json' in list(os.listdir("data/json")) and load_json:
        with open("data/json/data_sets.json") as json_data:
            datasets = json.load(json_data)
    else:
        with open("data/json/cmr_datasets.json") as json_cmr_datasets_file:
            json_cmr_datasets = json.load(json_cmr_datasets_file)
        json_cmr_dataset_list = json_cmr_datasets["feed"]["entry"]
        datasets = create_data_sets(json_cmr_dataset_list)

    if 'itemDict.json' in list(os.listdir("data/json")) and load_json:
        if verbose >= 1:
            print("Loading values from itemDict.json...")
        with open("data/json/itemDict.json", "r") as json_file:
            items = json.load(json_file)
    else:
        if verbose >=1:
            print("Getting data from Zotero...")
        items = zot_library.everything(zot_library.collection_items(collection_id))
        with open('data/json/itemDict.json', "w") as outfile:
            json.dump(items, outfile, indent=4)
    if verbose >= 1:
        print("Data loaded. It took %s seconds to load the data.\n"
            "There were %s items loaded"%(time.time() - start_time, len(items)))

    return items, datasets


def sort_zotero_parts(zotero_items):
    articles = {}
    notes = {}
    attachments = {}
    other = {}
    lookup_child_notes = defaultdict(list)
    lookup_child_links = defaultdict(list)

    for item in zotero_items:
        if item['data']['itemType'] == 'note':
            notes[item['key']] = item
            lookup_child_notes[item['data']['parentItem']].append(item['key'])
        elif item['data']['itemType'] == 'journalArticle':
            articles[item['key']] = item
        elif item['data']['itemType'] == 'attachment':
            attachments[item['key']] = item
            lookup_child_links[item['data']['parentItem']].append(item['key'])
        else:
            other[item['key']] = item
    n = open("data/json/notes.json", "w")
    j = open("data/json/articles.json", "w")
    a = open("data/json/attachments.json", "w")
    json.dump(notes, n, indent=4)
    json.dump(articles, j, indent=4)
    json.dump(attachments, a, indent=4)
    n.close()
    j.close()
    a.close()

    return articles, notes, attachments, lookup_child_notes, lookup_child_links


# add verbose statements
def process_zotero_citations(notes, lookup, data_set_citations_file, verbose=params["DEFAULT_VERBOSE"]):
    citation_list = []
    citation_count = defaultdict(int)

    for article in lookup:
        publication_id = article
        for key in lookup[article]:
            # NOTE: You may need to go back and fix the labels to ensure there is a new note for every dataset
            tags = notes[key]['data']['tags']
            mention = re.sub('(</p>)|(<p>)|(<br />)|(<br/>)', '', notes[key]['data']['note'])
            if "</span>" in mention:
                mention = mention.split(">")[1]
                mention = " ".join(mention.split("</span"))
            for tag in tags:
                if 'dataset' not in tag['tag']:
                    continue
                citation = search(citation_list, publication_id, tag)
                if citation:
                    for m in mention.split("\n"):
                        citation['mention_list'].append(m)
                else:
                    mention_list = []
                    for m in mention.split("\n"):
                        mention_list.append(m)
                    citation_list.append({
                        "citation_id": len(citation_list) + 1,
                        "publication_id": publication_id,
                        "data_set_id": tag['tag'].split(":")[1],
                        "mention_list": mention_list,
                        "score": 1.0
                    })
                    citation_count[tag['tag'].split(":")[1]] += 1
    with open(data_set_citations_file, "w") as fp:
        json.dump(citation_list, fp, indent=4)

    with open("data/json/data_sets.json") as json2:
        datasets = json.load(json2)

    for dataset in datasets:
        for citation in citation_list:
            if citation["data_set_id"] == dataset["data_set_id"]:
                dataset["mention_list"] += citation["mention_list"]
    json2.close()
    with open("data/json/data_sets.json", "w") as jsonout:
        json.dump(datasets, jsonout, indent=4)

    if verbose >= 1:
        print("There were %s total citations found." %len(citation_list))
        if verbose > 1:
            pass # Add additionalverbosity
        elif verbose > 2:
            pass # Add additional verbosity
    return citation_list


# add verbose statements
def process_zotero_publications(zotero_path, publication_ids, articles, attachments, lookup, verbose=params["DEFAULT_VERBOSE"]):
    publication_list = []
    publication_count = defaultdict(int)
    for publication_id in publication_ids:
        if search_pubs(publication_list, publication_id):
            continue
        # try:
        #     pub_item = articles[publication_id]
        # except KeyError:
        #     continue
        # try:
        #     author = pub_item['data']['creators'][0]["lastName"]
        #     title = pub_item['data']['title']
        # except KeyError:
        #     pass
        # nums = re.findall(r'\d{4}', pub_item['data']['date'])
        # year = None
        # pdf_name = None
        # if nums:
        #     year = nums[0]
        #     pdf_name = year+'_'
        # if author:
        #     pdf_name = pdf_name+author+'_'
        # pdf_name = pdf_name+title[0:50]
        # if ':' in pdf_name:
        #     pdf_name = pdf_name.split(':')[0]
        # #print ('PDF name: %s' % (pdf_name))
        # pdf_name = re.sub('(<)|(>)', '', pdf_name)
        # pdf_name = re.sub('/', '-', pdf_name)
        keys = lookup[publication_id]
        for key in keys:
            pdf_name = attachments[key]['data']['filename']
        pdf_files = glob.glob(zotero_path + "**/" + pdf_name)
        if pdf_files:
            pdf_file = pdf_files[0]  # os.path.basename(pdf_files[0])
            txt_name = publication_id + '.txt'
        else:
            continue
        pub_item = articles[publication_id]
        nums = re.findall(r'\d{4}', pub_item['data']['date'])
        year = None
        if nums:
            year = nums[0]
        publication_list.append({
            "publication_id": publication_id,
            "unique_identifier": pub_item['data']['DOI'],
            "title": pub_item['data']['title'],
            "pub_date": year,
            "pdf_file_name": pdf_file,
            "text_file_name": txt_name
        })
        name = publication_id + ".pdf"
        if name in os.listdir("data/PDF"):
            continue
        else:
            copyfile(pdf_file, "data/PDF/" + name)
        publication_count[publication_id] += 1
    with open("data/json/publications.json", "w") as fp:
        json.dump(publication_list, fp, indent=4)
    if verbose >= 1:
        print("There were %s total publications found." %len(publication_list))
        if verbose > 1:
            pass # Add additional verbosity
        elif verbose > 2:
            pass # Add additional verbosity

    return publication_list


def split_doc_paragraphs(src, dest, remove_stopwords = params["REMOVE_STOPWORDS"],
                     labels = params['PARAGRAPH_LABELS'], verbose=params["DEFAULT_VERBOSE"]):
    stop_words = stopwords.words("english")
    max_len = len(max(labels, key=len))

    for doc in os.listdir(src):
        fp = open(src + doc)
        txt = fp.read()
        paragraphs = txt.split("\n\n")
        outtxt = ""
        for i in range(len(paragraphs)):
            para = paragraphs[i]
            if any(label.lower() in para.lower() for label in labels):
                if len(para) > 3 * max_len:
                    outtxt += para
                else:
                    outtxt += paragraphs[i + 1]

        if remove_stopwords:
            words = outtxt.split(" ")
            newtxt = ""
            for word in words:
                if "\n" in word:
                    split = word.split("\n")
                    if split[0] not in stop_words:
                        newtxt += split[0] + "\n"
                    else:
                        newtxt += "\n"
                    if split[1] not in stop_words:
                        newtxt += split[1] + " "
                        continue
                if word not in stop_words:
                    newtxt += word + " "
            outtxt = newtxt
        out = open(dest + doc, "w")
        out.write(outtxt)
        out.close()
        if verbose > 1:
            print("Processed %s" % doc)
    if verbose:
        print("%s documents processed" % len(os.listdir(dest)))


def main(process_citations, process_publications, pdf2txt, split_paragraphs, create_test_lists, verbose=params["DEFAULT_VERBOSE"]):
    library_type = params["LIBRARY_TYPE"]
    api_key = params["ZOTERO_API_KEY"]
    if library_type == 'group':
        library_id = params["GROUP_LIBRARY_KEY"]
        collection_id = params["GROUP_COLLECTION_ID"]
    elif library_type == 'user':
        library_id = params["USER_LIBRARY_KEY"]
        collection_id = params["USER_COLLECTION_ID"]
    else:
        raise ValueError("Not an acceptable value for 'LIBRARY_TYPE', should be either 'group' or 'user'")

    items, dataset_list = load_data(params["LOAD_ZOT_JSON"], zotero.Zotero(library_id, library_type, api_key), collection_id)

    articles, notes, attachments, lookup_child_notes, lookup_child_links = sort_zotero_parts(items)

    if process_citations:
        if verbose:
            print("START PROCESSING CITATIONS")
        outfile = os.path.join('data', 'json', 'data_set_citations.json')
        process_zotero_citations(notes, lookup_child_notes, outfile)

    if process_publications:
        if verbose:
            print("START PROCESSING PUBLICATIONS")
        process_zotero_publications(params["ZOTERO_PATH"], list(articles.keys()), articles, attachments, lookup_child_links)

    if pdf2txt:
        sub_n = params["SUBPROC"]
        if verbose:
            print("CONVERTING PDF TO TXT")

        pdf_files = glob.glob("data/pdf/"+'*pdf')
        converts = []
        for i in range(len(pdf_files)):
            input_file = pdf_files[i]
            output_file = "data/text/"+input_file.split("/")[-1]+".txt"
            if i % sub_n == 0:
                commands = []
                command = ["pdf2txt.py", "-o", output_file, input_file]
                commands.append(command)
            elif i % sub_n == sub_n - 1:
                command = ["pdf2txt.py", "-o", output_file, input_file]
                commands.append(command)
                converts.append(commands)
            elif i == len(pdf_files) - 1:
                command = ["pdf2txt.py", "-o", output_file, input_file]
                commands.append(command)
                converts.append(commands)
            else:
                command = ["pdf2txt.py", "-o", output_file, input_file]
                commands.append(command)
        print("Running %s processes at once to convert pdfs" %sub_n)
        for commands in tqdm(converts, ascii=True, desc='pdf->txt'):
            try:
                procs = [Popen(i) for i in commands]
                for p in procs:
                    p.wait()
            except Exception as e:
                print(e)
        # assert len(os.listdir("data/PDF")) == len(os.listdir("data/text")) # Make sure no doc was lost

    if split_paragraphs:
        if verbose:
            print("SPLITTING PARAGRAPHS")
        split_doc_paragraphs("data/text/", "data/processed_text/")

    if create_test_lists:
        create_test()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--process_citations'
    )
    parser.add_argument(
        '--process_publications'
    )
    parser.add_argument(
        '--pdf2txt'
    )
    parser.add_argument(
        '--split_paragraphs'
    )
    parser.add_argument(
        '--create_test'
    )
    args = parser.parse_args()

    main(int(args.process_citations), int(args.process_publications), int(args.pdf2txt),
         int(args.split_paragraphs), int(args.create_test))