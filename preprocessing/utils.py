from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from io import StringIO

from config import params

import xml.etree.ElementTree as ET
import json
import requests
import os


def convert_pdf2txt(input_path : str, output_path : str, verbose=params["DEFAULT_VERBOSE"]) -> None:
  if verbose:
    for file in tqdm(Path(input_path).glob('*.pdf'), ascii=True,desc='pdf->txt'):
      fp = open(file, 'rb')
      rsrcmgr = PDFResourceManager()
      retstr = StringIO()
      codec = 'utf-8'
      laparams = LAParams()
      device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
      # Create a PDF interpreter object.
      interpreter = PDFPageInterpreter(rsrcmgr, device)
      # Process each page contained in the document.
      for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()
    txt_file = output_path+file.name+'.txt'
    if txt_file not in os.listdir(output_path):
      txt_out = open(txt_file, "w")
      txt_out.write(data)
  else:
    for file in Path(input_path).glob('*.pdf'):
      fp = open(file, 'rb')
      rsrcmgr = PDFResourceManager()
      retstr = StringIO()
      codec = 'utf-8'
      laparams = LAParams()
      device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
      # Create a PDF interpreter object.
      interpreter = PDFPageInterpreter(rsrcmgr, device)
      # Process each page contained in the document.
      for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()
    txt_file = output_path+file.name+'.txt'
    if txt_file not in os.listdir(output_path):
      txt_out = open(txt_file, "w")
      txt_out.write(data)

def mentions2datasets(path):
  with open(path + "data_sets.json") as json1:
    datasets = json.load(json1)
  with open(path + "data_set_citations.json") as json2:
    citations = json.load(json2)

  for dataset in datasets:
    for citation in citations:
      if citation["data_set_id"] == dataset["data_set_id"]:
        dataset["mention_list"] += citation["mention_list"]

  citations.close()

  with open(path + "data_set_citations.json", "w") as jsonout:
    json.dump(datasets, jsonout, indent=4)

  jsonout.close()


def search(cit_list, publication_id, dataset_id):
  for citation in cit_list:
    if citation['publication_id'] == publication_id and citation['data_set_id'] == dataset_id:
      return citation
  return False


def search_pubs(pub_list, publication_id):
  for publication in pub_list:
    if publication['publication_id'] == publication_id:
      return publication
  return False

def create_data_sets(json_cmr_dataset_list, verbose=params["DEFAULT_VERBOSE"]):
  ns = {'namespace': 'http://gcmd.gsfc.nasa.gov/Aboutus/xml/dif/'}

  dataset_list = []
  for json_cmr_dataset in json_cmr_dataset_list:
    if "_NRT" in json_cmr_dataset["short_name"]:
      continue
    entry_id = json_cmr_dataset["short_name"] + '_' + json_cmr_dataset["version_id"]
    p = (
      ('provider_id', 'GES_DISC'),
      ('entry_id', entry_id),
      ('pretty', 'true'),
    )
    response = requests.get('https://cmr.earthdata.nasa.gov/search/collections.dif10', params=p)
    # response = requests.get('https://cmr.earthdata.nasa.gov/search/collections.dif10?provider_id=GES_DISC&entry_id=ML2CO_004&pretty=true')
    root = ET.fromstring(response.text)
    DOI = None
    for child in root:
      if child.tag == "result":
        items = child.find("{" + ns.get('namespace') + "}DIF")
        for item in items:
          true_tag = item.tag.replace(("{" + ns.get('namespace') + "}"), '')
          if (true_tag == "Dataset_Citation"):
            pids = item.find("{" + ns.get('namespace') + "}Persistent_Identifier")
            for pid in pids:
              true_tag = pid.tag.replace(("{" + ns.get('namespace') + "}"), '')
              if true_tag == "Identifier":
                DOI = pid.text
                if verbose:
                  print(DOI)

    dataset_list.append({
      "data_set_id": json_cmr_dataset["short_name"],
      "version_id": json_cmr_dataset["version_id"],
      "unique_identifier": DOI,
      "title": json_cmr_dataset["dataset_id"],
      "name": json_cmr_dataset["dataset_id"],
      "description": json_cmr_dataset["summary"],
      "date": "",
      "coverages": "",
      "subjects": "",
      "methodology": "",
      "citation": "",
      "additional_keywords": "",
      "family_identifier": "",
      "mention_list": [],
      "identifier_list": [
        {
          "name": "https://doi.org/",
          "identifier": DOI
        }]
    })

  with open(os.path.join("data","json", "data_sets.json"), "w") as fp:
    json.dump(dataset_list, fp, indent=4)

  return dataset_list
