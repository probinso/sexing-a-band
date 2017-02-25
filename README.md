# sexing-a-band & aging-a-band

Team: Vikingkitty; Zak Kent; Probiso

## Project description 
This is a project where Multinomial Naive Bayes is used with TF-IDF to create a model that predicts the age of a song by looking only at the lyrics it contains.

## Explanation  of data pipeline in project 
 - Convert song lyrics into bag of words format
 - Create a TF-IDF model using entire corpus
 - Transform each song into a TF-IDF weighted vector 
 - TF-IDF normalized song vectors are then used in training a Multinomial Naive Bayes model where time blocks are used as classes
 - When making a new prediction with unseen data repeat the processing steps above and feed TF-IDF song vector into pre-trained Naive Bayes model

## Song data used in project
We originally started this project by working with an open source collection of song lyrics data that was part of the Million Song Dataset. This dataset was an ideal starting point because it had song lyrics stemmed and preprocessed into a bag of words format. In the end we decided to move away from this dataset and gather our own data. We decided to do this because to Million Song Dataset only contained the 5,000 most common words across all songs. While looking at these words was interesting we felt that looking at a larger number of words could help us identify trends in language use more easily and with greater variety. Links to the original dataset we used can be found below.    

[Million_song_meta_data](http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/track_metadata.db) - link to metadata DB

[Million_song_project_BOW_data](http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/mxm_dataset.db) - link to bag of words DB

	   	    
# Makefile commands available 
Below is a brief description of each Make file command that is available and the input that it requires. The commands are written in order and recreate the process that we used to build this project. 

The ```make all``` command will run all of the commands you see below and recreate this project on your own computer. Be warned that in its current state these commands include the data scraping process which took roughly two days to complete. 

### make bow_runner.csv
This csv file is made by using ```scrape.py```, this file takes a list of song tracks from the ```tracks_per_year.txt``` file and scrapes different lyrics sharing sites to gathering lyrics for the songs. When the songs are scraped their lyrics are converted into a bag of words format.

### make bow_english.csv
This csv is created by the ```bow_to_english.py``` file and takes ```bow_runner.csv``` as input. Its purpose is to filter out and keep only those songs that are made up of mostly english words. 

### make word_lookup.pkl 
This pickle file is create using the ```savedict.py``` script and takes ```bow_english.csv``` as input. This file is created in order to save a lookup dictionary that is needed when our model is being tested against songs it hasn't seen before. Each word in a new song mush be matched to the same number value that was used to represent words when training the model.  

### make bow_english_year.csv
This csv is created by the ```year_bin_maker.py``` file and takes the ```bow_english.csv``` as input. This step is done in order to create bins or categories for different time periods in which songs were written. These bins can be adjusted inside the script and give a user the ability to control the size of the time period the model is trying to predict. 

### make full_tfidf_model.tfidf
This file is created by the ```topic_maker_tfidf.py``` script and takes ```bow_english.csv``` as input. The purpose of this step is to create a TFIDF model based on all of the songs in our collection. TF-IDF is a normalization/weighting process that helps to figure out how important each word is to the meaning of a song.

### make only_tfidf.csv
This csv is create by the ```make_tfidf_score.py``` file and takes ```bow_english_year.csv``` & ```full_tfidf_model.tfidf``` as input. This is where each songs' bag or words are converted to a TF-IDF vector using the model trained in the step above. 

### make NB_model.pkl
This file is created by running the ```NB_train_test.py``` script and takes ```only_tfidf.csv``` & ```word_lookup.pkl``` as input. In our project we used a simple Naive Bayes model which looks at the conditional probability of each word in a song given a certain time period, blends those probabilities across all the words present, and gives us the probability that a song is from one time period or another given the words it contains. We then save this model in a .pkl file so it can be reused to make predictions on unseen data.
