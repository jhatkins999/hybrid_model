# config.py

params = {
    'DEFAULT_VERBOSE' : 1, # Sets the default verbosity for all functions
    # Zotero Parameters
    'ZOTERO_PATH' : '/Users/jhatkins/Zotero/storage/',
    'SUBPROC' : 4,  # Number of subprocesses to run while converting pdfs
    'USER_LIBRARY_KEY' : '6657757',
    'GROUP_LIBRARY_KEY' : '2395775',
    'USER_COLLECTION_ID' : 'H244E5IH',
    'GROUP_COLLECTION_ID' : 'F3P68PWK',
    'ZOTERO_API_KEY' : 'tB3q3dduZDZR1xXOXGw9ngvV',
    'LOAD_ZOT_JSON' : True, # Choose to load the last saved Zotero library if True, get the current library if False
    'LIBRARY_TYPE' : 'group', # Used to choose which library to use, 'group' for group and 'user' for user
    # Train parameters
    'TEST_SIZE' : .2, # Amount of labeled data used for testing
    'VALIDATION_SIZE' : .2, # Amount labeled data used for validation
    'RANDOM_SEED' : 714, # Random seed for replication, Original results are with seed 714
    'REMOVE_STOPWORDS' : 1, # Determines if stop words should be removed in preprocessing, options 0 or 1
    # Preprocessing Parameters
    'PARAGRAPH_LABELS' : # If the label is in a section title, the split_paragraphs function will choose that section of the doc
        ["Abstract", "Data", "MLS", "Aura", "Data", "Methods", "Instruments", "Measurements", "Acknowledgements"],
    ####################################################################
    # Need to edit the paths below
    # Absolute Data Paths
    'PUBLICATION_JSONPATH' : "/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/data/input/publications.json",
    'PUBLICATION_DOCPATH' : '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/data/input/files/text/',
    'TOKENIZED_DOCPATH' : '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/project/tokenized/',
    'PROCESSED_DOCPATH' : '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/project/processed/',
    'RESEARCH_FIELDS_OUTPUT_PATH': '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/data/output/research_fields.json',
    'RESEARCH_DATA_NO_ID_OUTPUT_PATH': '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/project/intermediate_results/data_set_mentions.json',
    'RESEARCH_METHOD_OUTPUT_PATH': '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/data/output/methods.json',
    'DATASET_QUESTION_VOCAB_PATH' : '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/project/queryselection/querylist.pickle',
    'DOCQA_CANDIDATE_ANSWER_CLASSIFIER_PATH' : '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/project/ner/release/answer_classifier_50_hidden_layer_1_epoch.pth',
    'INPUT_ULTRAFINE_PATH': '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/project/ner/release/crowd/inputUltraFine.json',
    'OUTPUT_DOCQA_PATH': '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/data/output/data_set_mentions.json',
    'FILE_ROOT': '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/project/ner/release/',
    'GLOVE_VEC': '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/project/wordvector/glove/',
    'EXP_ROOT': '/Users/jhatkins/citation_processing/kaist/rclc_2019_baseline/project/ner/models',
}