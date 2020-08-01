To run this project, you need to be running a linux based system and have anaconda downloaded

To create the environment run the command:
    conda env create -f environment.yml
    
Then export the pythonpath to make sure you can run your modules:
    PYTHONPATH=PathToFolder
    export PYTHONPATH
To run the preprocessing code
    1. cd preprocessing
    2. python preprocessing.py --load_json 1 --process_citations 1 --process_publications 1 --pdf2txt 1 --split_paragraphs 1
    Note: It takes around an hour to process all the PDF's. Edit the subproc param to use more threads
    to find the number of threads to run on run $ sysctl hw.logicalcpu
    
To run the NerModel Code:
    1. n
