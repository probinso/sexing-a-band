from __future__ import print_function

import gensim
import json
import pickle
import sys
from sklearn.externals import joblib
from scipy.sparse import lil_matrix
import utility
from lyrics_to_bow import lyrics_to_bow


def make_stemmed_dict(data):
    stemmed_data = lyrics_to_bow(data)
    return stemmed_data if stemmed_data is not None else {}

def conv_stem_dict(a_dict, word_lookup_dict):
    """
    converts stemmed dict output into {word_num: count} format
    where word_num maps to a word's key in lookup dict from model training.
    returns empty dict if word wasn't seen during model training. 
    also return length of word_lookup_dict used later in data transform
    """
    num_word_feat = len(word_lookup_dict.keys())

    out_dict = {}
    for word in a_dict.keys():
        try:
            out_dict[word_lookup_dict[word]] = a_dict[word]
        except:
            # word not in lookup dict during training
            continue
    return out_dict, num_word_feat

def tfidf_transform_stemmed_dict(word_num_dict, tfidf_model):
    """
    turn dict into a dict of word_keys: tfidf_scores using trained tfidf model 
    """
    song_tfidf = tfidf_model[word_num_dict.items()]

    tfidf_dict = {}
    for key, value in song_tfidf:
        tfidf_dict[key] = value

    return tfidf_dict

def tfidf_dict_to_matrix(tfidf_dict, num_word_feat):
    """
    create a lil_matrix out of tfidf_dict so it matches format used in training 
    """
    list_of_dicts = [tfidf_dict]

    # create a list of list matrix of the appropriate size 
    sparse_matrix = lil_matrix((len(list_of_dicts), num_word_feat))

    # loop thorugh each dict and add its values to appropriate matrix 
    for idx, a_dict in enumerate(list_of_dicts):        
        for key in a_dict.keys():
            # subtracting 1 from the key because values in dict start at 1
            # assign value at the index that matches word in matrix 
            sparse_matrix[idx, key - 1] = a_dict[key]
    return sparse_matrix

def data_prep_helper(word, word_lookup_dict, tfidf_model):
    """
    handle the data prep of stemming a word, mapping word to lookup dict 
    used in training, converting that dict using pre-trained tfidf model,
    and then finally turn dict into a list of list matrix to mirror 
    data prep in the training process.  
    """
    stem_dict = make_stemmed_dict(word)

    word_num_dict, num_word_feat = conv_stem_dict(stem_dict, word_lookup_dict)

    tfidf_dict = tfidf_transform_stemmed_dict(word_num_dict, tfidf_model)

    lil_matrix_from_dict = tfidf_dict_to_matrix(tfidf_dict, num_word_feat)

    return lil_matrix_from_dict

def load_NB_model(NB_model_pkl):
    """
    load pre trained NB model
    """
    with open(utility.make_resource(NB_model_pkl), "rb") as fo:
        clf = joblib.load(fo)

    return clf 

def load_word_lookup_dict(word_lookup_pkl):
    """
    load word lookup dict used in training and return the dict, 
    list of all words in dict, and num of words in dict 
    """
    with open(utility.make_resource(word_lookup_pkl), "rb") as f:
        dict_obj = pickle.load(f)
        words_in_dict = dict_obj.keys()

    return dict_obj, words_in_dict
    
def interface(word_lookup_pkl, tfidf_model_pkl, NB_model_pkl, out_file):
    """
    load all models and pkl files, loop thorough each word in training lookup dict,
    get probability scores for each word for all decades, write word and scores out 
    to csv. 
    """
    loaded_dict, words_in_dict = load_word_lookup_dict(word_lookup_pkl)
    loaded_NB_model = load_NB_model(NB_model_pkl)
    loaded_tfidf_model = gensim.models.TfidfModel.load(utility.make_resource(tfidf_model_pkl))

    with open(utility.make_resource(out_file), 'w') as of:
        for word in words_in_dict:
            prepped_word_data = data_prep_helper(word, loaded_dict, loaded_tfidf_model) 

            decade_probs = loaded_NB_model.predict_proba(prepped_word_data[0].toarray())[0]
            probs_list = [str(score) for score in decade_probs]
            
            if probs_list: 
                probs_list.insert(0, word)
                print(','.join(probs_list), file=of)
    
def cli_interface():
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    try:
        word_lookup_dict, tfidf_model = sys.argv[1], sys.argv[2] 
        NB_model, out_file = sys.argv[3], sys.argv[4]
    except:
        print("usage: {} <dict_pickle> <tfidf_model> <NB_model> <outpath>".format(sys.argv[0]))
        sys.exit(1)
    interface(word_lookup_dict, tfidf_model, NB_model, out_file)


if __name__ == "__main__":
    cli_interface()
