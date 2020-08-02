To run this project, you need to be running a linux based system and have anaconda downloaded

To create the environment run the command:
    conda env create -f environment.yml
    
Then export the pythonpath to make sure you can run your modules:
    PYTHONPATH=PathToFolder
    export PYTHONPATH
To run the preprocessing code
    1. cd preprocessing
    2. python preprocessing.py --process_citations 1 
           --process_publications 1 --pdf2txt 1 --split_paragraphs 1 --create_test 1
    Note: It takes around 2 hours to process all the PDF's. Edit the subproc param to use more threads
    to find the number of threads to run on run $ sysctl hw.logicalcpu
    
To run the NerModel Code:
    1. cp data/json/publications_train.json ../NerModel/data/train
       cp data/json/publications_test.json ../NerModel/data/test
       cp data/json/publications_dev.json ../NerModel/data/dev
       cp data/json/data_sets.json ../NerModel/data
    2. cd ../NerModel
    3. python project/get_docs.py
    4. python project/to_conll.py --data_folder_path data
    5. 
    
