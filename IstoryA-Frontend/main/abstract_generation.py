from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

def sentence_similarity(sentence1, sentence2, stopwords=None):
    if stopwords is None:
        stopwords = []
    sentence1 = [word.lower() for word in sentence1]
    sentence2 = [word.lower() for word in sentence2]
    all_words = list(set(sentence1 + sentence2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    for word in sentence1:
        if word in stopwords:
            continue
        vector1[all_words.index(word)] += 1

    for word in sentence2:
        if word in stopwords:
            continue
        vector2[all_words.index(word)] += 1

    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for index1 in range(len(sentences)):
        for index2 in range(len(sentences)):
            if index1 == index2:
                continue
            similarity_matrix[index1][index2] = sentence_similarity(sentences[index1], sentences[index2], stop_words)
    return similarity_matrix

def generate_abstract(story, nb_sentence):
    stop_words = stopwords.words('english')
    resume_text = []
    words = []

    for sentence in story:
        words.append(sentence.replace("[^a-zA-Z]", " ").split(" "))

    sentence_similarity_martix = build_similarity_matrix(words, stop_words)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(words)), reverse=True)

    for i in range(nb_sentence):
        resume_text.append(" ".join(ranked_sentence[i][1]))

    return resume_text
