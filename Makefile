engine := $(shell which python)
RSRC   := $(patsubst "%",%, $(shell jq '.storage_path' resource.json))

check_resource: resource.json
	echo $(RSRC)

bow_english_year.csv: $(RSRC)/bow_english_year.csv
$(RSRC)/bow_english_year.csv: $(RSRC)/bow_english.csv year_dict.py
	$(engine) year_dict.py $(RSRC)/bow_english.csv $(RSRC)/bow_english_year.csv

bow_english.csv:$(RSRC)/bow_english.csv
$(RSRC)/bow_english.csv:bow_to_english.py bow_runner.csv
	$(engine) bow_to_english.py $(RSRC)/bow_runner.csv $(RSRC)/bow_english.csv

bow_runner.csv:$(RSRC)/bow_runner.csv
$(RSRC)/bow_runner.csv:$(RSRC)/tracks_per_year.txt scrape.py
	$(engine) scrape.py $(RSRC)/tracks_per_year.txt $(RSRC)/bow_runner.csv




full_tfidf_model.tfidf:data/mxm_dataset_train.txt topic_maker_tfidf.py
	$(engine) topic_maker_tfidf.py

data/only_tfidf.csv:train_data_tfidf.py full_tfidf_model.tfidf
	$(engine) train_data_tfidf.py

test_score:data/only_tfidf.csv NB_tfidf.py
	$(engine) NB_tfidf.py
