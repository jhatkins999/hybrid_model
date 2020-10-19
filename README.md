To run this project, you need to be running a linux based system and have anaconda downloaded

To create the environment run the command:
    conda env create -f environment.yml
After the environment is created the spacy model needs to be installed manually:
    python -m spacy download en_core_web_sm 
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
    2. python project/get_docs.py
    3. python project/to_conll.py --data_folder_path data
    4. python project/ner_retraining/create_splits.py
    5. rm -r project/model/* 
    6. allennlp train project/ner_model -s project/model --include-package project/ner_rcc
    7. python project/to_conll_test.py # Might not be necessary
    8. python project/ner_retraining/generate_ner_output.py --conll_path data/test/ner-conll --output_path data/output/ner_output --model_path project/model
    

    
