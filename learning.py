import gensim

def gensim_lsi_run(corpus, num_topics, id2word):
    lsi = gensim.models.lsimodel.LsiModel(corpus, num_topics=num_topics, id2word=id2word
    for index, topic in lsi.print_topics(num_topics=10, num_words = 3):
        print(index)
        print("  " + topic)

    lsi.save('./song_topics.lsi')
