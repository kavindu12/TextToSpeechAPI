import PyPDF2
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize
import re
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from gensim.summarization import summarize


file = open('E:\SLIIT\PDF\demo.pdf', mode='rb')
pdf_reader = PyPDF2.PdfFileReader(file)


extract_read = ""
count = pdf_reader.numPages
for x in range(count):
    extract_read += pdf_reader.getPage(x).extractText() + "\n"
extract_read = " ".join(extract_read.replace(u"\xa0", " ").strip().split())
# print(extract_read)

extract = str(re.findall(
        r'(?=(METHODOLOGY .*?)(?=RESULTS AND DISCUSSION |end))|(?=(Methodology .*?)(?=Results and Discussion |end))',
        extract_read, re.DOTALL))
print(extract)

'''
file = open('FinalPaper-19-120.pdf', mode='rb')
pdf_reader = PyPDF2.PdfFileReader(file)

for x in range(2, 3):
    page = pdf_reader.getPage(x)
    extract = page.extractText()
    print(extract)
'''

# split the the text in the article into sentences
sentences = sent_tokenize(extract)
# print(sentences)

# remove punctuations, numbers and special characters
clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

# make alphabets lowercase
clean_sentences = [s.lower() for s in clean_sentences]
# print(clean_sentences)

stop_words = stopwords.words('english')

# function to remove stopwords


def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new


# remove stopwords from the sentences
clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
# print(clean_sentences)

# Extract word vectors
word_embeddings = {}
f = open('glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

sentence_vectors = []
for i in clean_sentences:
  if len(i) != 0:
    v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()]) / (len(i.split()) + 0.001)
  else:
    v = np.zeros((100,))
  sentence_vectors.append(v)

len(sentence_vectors)
# print(length)

# similarity matrix
sim_mat = np.zeros([len(sentences), len(sentences)])

for i in range(len(sentences)):
  for j in range(len(sentences)):
    if i != j:
      sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1, 100),
                                                  sentence_vectors[j].reshape(1, 100))[0, 0]

nx_graph = nx.from_numpy_array(sim_mat)
scores = nx.pagerank(nx_graph)

ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

# Specify number of sentences to form the summary
sn = 7

# Generate summary
summarize_text="";
for i in range(sn):
    #print(ranked_sentences[i][1])
    # print(str(ranked_sentences[i][1]))
    summarize_text=summarize_text+str(ranked_sentences[i][1]);

print(summarize_text);









'''
extract_text = extract
summary = summarize(extract_text)
print(summary)
'''




