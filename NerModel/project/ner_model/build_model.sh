#/bin/bash

rm -r model/*
allennlp train ner_model/config.json -s model --include-package ner_rcc
