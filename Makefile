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
$(RSRC)/bow_runner.csv:$(RSRC)/tracks_per_year.txt scrape.py processed.txt
	touch $(RSRC)/bow_runner.csv
	$(engine) scrape.py $(RSRC)/tracks_per_year.txt $(RSRC)/bow_runner.csv

processed.txt:$(RSRC)/processed.txt
$(RSRC)/processed.txt:
	touch $(RSRC)/processed.txt

full_tfidf_model.tfidf: $(RSRC)/full_tfidf_model.tfidf
$(RSRC)/full_tfidf_model.tfidf:topic_maker_tfidf.py bow_english.csv
	$(engine) topic_maker_tfidf.py bow_english.csv full_tfidf_model.tfidf


only_tfidf.csv:$(RSRC)/only_tfidf.csv
$(RSRC)/only_tfidf.csv: make_tfidf_score.py full_tfidf_model.tfidf bow_english_year.csv
	$(engine) make_tfidf_score.py bow_english_year.csv full_tfidf_model.tfidf full_putput.csv only_tfidf.csv


clean:
	rm -rf $(RSRC)/{bow_english.csv,processed.txt,full_tfidf_model.tfidf,bow_english_year.csv,only_tfidf.csv}









data/only_tfidf.csv:train_data_tfidf.py full_tfidf_model.tfidf
	$(engine) train_data_tfidf.py

test_score:data/only_tfidf.csv NB_tfidf.py
	$(engine) NB_tfidf.py
