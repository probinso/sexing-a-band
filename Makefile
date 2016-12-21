
RESOURCE=/media/terra/UndecidedTeam

$(RESOURCE)/bow_english.csv:bow_to_english.py $(RESOURCE)/bow_runner.csv
	bow_to_english.py $(RESOURCE)/bow_runner.csv $(RESOURCE)/bow_english.csv

full_tfidf_model.tfidf:data/mxm_dataset_train.txt topic_maker_tfidf.py
	python topic_maker_tfidf.py

data/only_tfidf.csv:train_data_tfidf.py full_tfidf_model.tfidf
	python train_data_tfidf.py

test_score:data/only_tfidf.csv NB_tfidf.py
	python NB_tfidf.py
