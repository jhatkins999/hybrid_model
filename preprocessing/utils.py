from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from io import StringIO


def convert_pdf2txt(input_path : str, output_path : str) -> None:
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


def add_mentions2datasets(path):
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