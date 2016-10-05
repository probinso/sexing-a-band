# sexing-a-band
aging-a-band

1. `soung_data_prep.py` generates **data/full_output.csv** containing **track_id**, **artist_id**, **track_year**, **word_counts**
2. `topic_maker_tfidf.py` processes over **data/full_output.csv** and **mxm_dataset_train.csv** and saves the 
    * **tfidf** to **full_tfidf_model.tfidf**
    * **sli model** to **data/full_song_topics_tfidif.lsi**
3. `train_data_tfidf.py` loads the above two model files, then steps through **data/full_output.csv** to produce **full_output_tfidf.csv**
---

Team: Vikingkitty; Zak Kent; Probiso

Using the databases listed below to predict the year in which a song was written based on a LSI model.
Stretch goal is to then predict gender of artist based on the same LSI model.

http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/track_metadata.db - link to metadata DB


http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/mxm_dataset.db - link to bag of words DB


Rough guide to running scripts 

    1. make output csv using orm.py 
        orm.py: 
            - makes pony mapping for meta_db and word_db 
            - writes track_id, year, and BOW dict in key:value format to output csv
            - need to add mxm_dataset_test.txt to (line 46) to capture test data as well as train split 

            - ? 237,662 songs supposed to be in whole dataset our model was training on 152,827 
            - ? how many exceptions are happening in try/except block, are we loosing data (line 62)

    2. run topic_maker_tfidf.py to train lsi model   
        # script is basically the same as topic_maker.py except tfidf is added 

        topic_maker_tfidf.py:
            - takes top 5000 most common words and makes lookup dict for words 
            - pulls data out of output.csv and makes a list of list with each song represted by BOW counts 
            - trains tfidf model with list of lists above 
            - converts list of lists BOW to tfidf scores 
            - trains LSI using scores from above  
            - saves lsi model 

            - ? we're opening mxm_dataset_train again to make another lookup dict, I think this was done in orm.py (line 8)
            - ? still need to find a way to include both train/test .txt files 
            - ? Hobs suggested that we lower our number of topics in LSI to 50 because we only have a 5,000 dim space, we might get more meaningful topics this way. 

    3. run train_data_tfidf.py to convert data to format used in training our models 
        train_data_tfidf.py:
            - loads models trained in step #2 
            - loops through output.csv from step #1 
            - in loop converts BOW into lsi topic vectors using loaded models and calculates decade of song
            - writes each songs' id, year, decade #, topic_vector to output_tfidf.csv  

    4. run lyrics_naive_bayes.py to train GaussianNB with data prepared above
        lyrics_naive_bayes.py:
            - loads data from output_tfidf.csv
            - splits data into train/test split and trains NB 

            - ? we can look at learning class probabilites to help our models increase their accuracy, not sure if this is cheating or not:)
