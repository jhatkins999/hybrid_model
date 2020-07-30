To run this project, you need to be running a linux based system and have anaconda downloaded

To create the environment run the command:
    conda env create -f environment.yml
   
To run the preprocessing code
    1. cd preprocessing
    2. python preprocessing.py --load_json 1 --process_citations 1 --process_publications 1 --pdf2txt 1 --split_paragraphs 1
