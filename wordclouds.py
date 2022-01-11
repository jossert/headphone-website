import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import nltk
nltk.download('stopwords')
import sqlite3

sql_connect = sqlite3.connect('/Users/jossertshi/Desktop/app/Headphone.db', check_same_thread=False)
cursor = sql_connect.cursor()

query = 'SELECT DISTINCT brand, model FROM Reviews'
cursor.execute(query)
sql_connect.commit()
data = cursor.fetchall()
stopwords = nltk.corpus.stopwords.words('english')
stopwords += ['headphone','also','headphones', 'earbuds', 'make', 'airpods', 'apple','could','1000xm4','1000xm3','sony']

for i in data:
    brand, model = i[0],i[1]
    query2 = 'SELECT * FROM Reviews WHERE Brand = \'' + brand +'\''+ ' AND Model= \'' + model +'\''
    cursor.execute(query2)
    sql_connect.commit()
    data2 = cursor.fetchall()
    corpus = [" ".join(i[7] for i in data2)]
    stopwords += [model,brand]
    vectorizer = TfidfVectorizer(stop_words=stopwords,ngram_range = (1,1))
    X = vectorizer.fit_transform(corpus)

    feature_names = vectorizer.get_feature_names()

    dense = X.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)
    df.head()
    data = df.transpose()
    data.columns = ['review']

    wordcloud = WordCloud(background_color="white",
                          width=500, height=350, max_words=500).generate_from_frequencies(data['review'])

    wordcloud.to_file("static/wordcloud/" + model + ".png")








