#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility methods for loading and processing review/tagging data.

The readers process the data and return a data2domain dictionary:

    domain2data = {domain: [[], [], None] for domain in domains}

which consists of:

    X, y, X_unlabeled

where

    TOKENS: raw sentences from labeled data
    LABELS: corresponding labels
    UNLABELED: raw sentences from unlabeled data (optional)

"""

TOKENS = 0
LABELS = 1
UNLABELED = 2

import os
import codecs
import numpy as np
import scipy.sparse

#from simpletagger import read_conll_file

#from bist_parser.bmstparser.src.utils import read_conll

### TODO: use names for indices: 0 => X (sentences, 1: labels, 2: unlabeled tokens

# =============== sentiment data reader functions ======

NEG_ID = 0  # the negative sentiment id
POS_ID = 1  # the positive sentiment id
NEU_ID = 2

def task2read_data_func():
    """Returns the read data method for each task."""
    return read_processed


def read_processed(domain_dir_path, unlabeled=False, max_train=None, max_unlabeled=None):
    def line2features(line):
        features = line.split(' ')[:-1]
        label = label2label_id(line.split(' ')[-1].split(':')[1].strip())
        ngram_seq = []
        for feature in features:
            ngram = feature
            ngram_seq.append(ngram)
        return ngram_seq, label

    reviews = []
    labels = []
    if unlabeled:
        file_path = os.path.join('data/semi/test/test_unlabel.txt')
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                ngram_seq, label = line2features(line)
                reviews.append(ngram_seq)
                labels.append(label)
        return reviews, labels

    pos_file_path = os.path.join(domain_dir_path, 'rengong_pos_fenci_label.txt')
    neg_file_path = os.path.join(domain_dir_path, 'rengong_neg_fenci_label.txt')
    neu_file_path = os.path.join(domain_dir_path, 'rengong_neu_fenci_label.txt')
    with open(pos_file_path, encoding='utf-8') as f_pos,\
            open(neg_file_path, encoding='utf-8') as f_neg, \
            open(neu_file_path, encoding='utf-8') as f_neu:
        for pos_line, neg_line, neu_line in zip(f_pos, f_neg, f_neu):
            ngram_seq, _ = line2features(pos_line)
            reviews.append(ngram_seq)
            labels.append(POS_ID)
            ngram_seq, _ = line2features(neg_line)
            reviews.append(ngram_seq)
            labels.append(NEG_ID)
            ngram_seq, _ = line2features(neu_line)
            reviews.append(ngram_seq)
            labels.append(NEU_ID)
    return reviews, labels


def label2label_id(label):
    if label == 'positive':
        return POS_ID
    elif label == 'negative':
        return NEG_ID
    elif label == 'neutral':
        return NEU_ID
    raise ValueError('%s is not a valid label.' % label)



if __name__ == "__main__":
    split2data = {}
    read_data = task2read_data_func()
    sentiment_path = os.path.join('data/semi/train')
    train_path = dev_path = os.path.join(sentiment_path)
    unlabeled_path = os.path.join('data/semi/test/test_unlabel.txt')
    for split, path_ in zip(['test', 'dev', 'unlabeled'],
                            [train_path, dev_path, unlabeled_path]):
        if split == 'unlabeled':
            data = read_data(path_, unlabeled=True)  # [[instances],[]]
            print(data[0])
        else:
            data = read_data(path_, unlabeled=False) # keeps [[instances],[labels]]
            print(data[0])

            if split == 'test':
                pass
            elif split == 'dev':
                continue
            elif split == 'unlabeled':
                split = 'train'
                data, data_dev = (data[0][:-200], data[1][:-200]), (data[0][-200:], data[1][-200:])
                split2data['dev'] = list(data_dev)
            elif split == 'train':
                split = 'unlabeled'
                data = data[0], []
            elif split == 'unlabeled':
                data = data[0], []


        split2data[split] = list(data)
        print('# of %s examples: %d.' % (split, len(data[0])))