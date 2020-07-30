# config.py

params = {
    'TEST_SIZE' : .2, # Amount of labeled data used for testing
    'VALIDATION_SIZE' : .2, # Amount labeled data used for validation
    'RANDOM_SEED' : 714, # Random seed for replication, Original results are with seed 714
    'REMOVE_STOPWORDS' : 1, # Determines if stop words should be removed in preprocessing, options 0 or 1
    'LABELS' : # If the label is in a section title, the split_paragraphs function will choose that section of the doc
        ["Abstract", "Data", "MLS", "Aura", "Data", "Methods", "Instruments", "Measurements", "Acknowledgements"],
    ####################################################################
    # Need to edit the paths below
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