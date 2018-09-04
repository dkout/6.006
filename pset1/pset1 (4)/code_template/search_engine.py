import os
import math
import re
import pdb

def extract_corpus(corpus_dir = "articles"):
    """
    Returns a corpus of articles from the given directory.

    Args:
        corpus_dir (str): The location of the corpus.

    Returns:
        dict: A dictionary with key = title of the article,
              value = list of words in the article
    """
    corpus = {}
    num_documents = 0
    for filename in os.listdir(corpus_dir):
        with open(os.path.join(corpus_dir, filename)) as f:
            corpus[filename] = re.sub("[^\w]", " ",  f.read()).split()
    return corpus
class SearchEngine(object):
    """
    Represents an instance of a search engine. Instances of the search engine are
    initialized with a corpus.

    Args:
        corpus (dict): A dictionary of (article title, article text) pairs.
    """
    def __init__(self, corpus):
        # The corpus of (article title, article text) pairs.
        self.corpus = corpus
        self.corpus_dic=dict()
        for article in self.corpus:
            wordcount=dict()
            for word in self.corpus[article]:
                if not word.islower():
                    word=word.lower()
                if word in wordcount:
                    wordcount[word]+=1
                else:
                    wordcount[word]=1
            self.corpus_dic[article]=wordcount
        self.idf=dict()
        df=dict()
        for article in self.corpus_dic:
            for word in self.corpus_dic[article]:
                for article2 in self.corpus_dic:
                    if word in self.corpus_dic[article2]:
                        if word in df:
                            df[word]+=1
                            break
                        else:
                            df[word]=1
                            break
        for word in df:
            self.idf[word]=math.log(len(self.corpus_dic)/df[word])
        self.tf_idf={}
        for article in self.corpus_dic:
            self.tf_idf[article]={}
            for word in self.corpus_dic[article]:
                self.tf_idf[article][word]=self.corpus_dic[article][word]*self.idf[word]
    def angle_finder(self, doc1, doc2):
        inner_product, sq_d1, sq_d2=0,0,0

        for w in doc1:
            sq_d1+=(doc1[w])**2
            if w in doc2:
                inner_product += doc1[w]*doc2[w]
        for w in doc2:
            sq_d2+=(doc2[w])**2
        angle=inner_product/((sq_d1*sq_d2)**0.5)
        return angle
    def get_relevant_articles_doc_dist(self, title, k):
        """
        Returns the articles most relevant to a given document, limited to at most
        k results. Uses the normal document distance score.
        Args:
            title (str): The title of the article being queried (assume it exists).
        Returns:
            An array of the k most relevant (article title, document distance) pairs, ordered
            by decreasing relevance.

            Specifications:
                * Case is ignored entirely
                * If two articles have the same distance, titles should be in alphabetical order
"""
        inner_product=0
        distances=list()
        for article in self.corpus_dic:
            if not article==title:
                angle=self.angle_finder(self.corpus_dic[title], self.corpus_dic[article])
                distances.append((article, math.acos(angle)))
        distances=sorted(distances, key=lambda tup: tup[1])
        print (distances[:k])
        return distances[:k]

    def get_relevant_articles_tf_idf(self, title, k):
        """
        Returns the articles most relevant to a given document, limited to at most
        k results. Uses the document distance with TF-IDF scores.

        Args:
            title (str): The title of the article being queried (assume it exists).

        Returns:
            An array of the k most relevant (article title, document distance) pairs, ordered
            by decreasing relevance.

            Specifications:
                * Case is ignored entirely
                * If two articles have the same distance, titles should be in alphabetical order
        """


        inner_product=0
        distances=list()
        for article in self.tf_idf:
            if not article==title:
                angle=self.angle_finder(self.tf_idf[title], self.tf_idf[article])
                distances.append((article, math.acos(angle)))
        distances=sorted(distances, key=lambda tup: tup[1])
        print (distances[:k])
        return distances[:k]

    def search(self, query, k):
        """
        Returns the articles most relevant to a given query, limited to at most
        k results.

        Args:
            query (str): The query for the search engine. Doesn't contain any special characters.

        Returns:
            An array of the k best (article title, tf-idf score) pairs, ordered by decreasing score.

            Specifications:
                * Only consider articles with a positive tf-idf score.
                * If there are fewer than k results with a positive tf-idf score, return those results.
                  If there are more, return only the k best results.
                * If two articles have the same score, titles should be in alphabetical order
        """
        docs={}
        for term in set(query.split(' ')):
            for article in self.tf_idf:
                if term in self.tf_idf[article]:
                    if article in docs:
                        docs[article]+=self.tf_idf[article][term]
                    else:
                        docs[article]=self.tf_idf[article][term]
        docs_sort=sorted(docs.items(), key=lambda p: (p[1],p[0]), reverse=True)
        docs_sort=[x for x in docs_sort if x[1] >= 0]
        if len(docs_sort)<k:
            print (docs)
            return docs
        else:
            print (docs_sort[:k])
            return docs_sort[:k]


if __name__ == '__main__':
    corpus = extract_corpus()
    e = SearchEngine(corpus)
    print("Welcome to 6006LE! We hope you have a wonderful experience. To exit, type 'exit.'")
    print("\nSuggested searches: the yummiest fruit in the world, child prodigy, operating system, red tree, coolest algorithm....")
    while True:
        query = input('\nEnter query here: ').strip()
        if query == "exit":
            print("Good bye!")
            break
        results = e.search(query, 5)
        if len(results) == 0:
            print("There are no results for that query. :(")
        else:
            print("Top results: ")
            for title, score in e.search(query, 5):
                print ("    - %s (score %f)" % (title, score))
