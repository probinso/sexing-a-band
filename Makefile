
full_tfidf_model.tfidf:data/mxm_dataset_train.txt topic_maker_tfidf.py
	python topic_maker_tfidf.py

data/only_tfidf.csv:train_data_tfidf.py full_tfidf_model.tfidf
	python train_data_tfidf.py