import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#Reading the data
dataset = pd.read_csv('netflix_titles.csv').drop(labels=['show_id', 'date_added'], axis=1)
dataset.loc[dataset['type'] == 'TV Show', 'type'] = 'Show'

#Preprocessing of data
tfid = TfidfVectorizer(stop_words='english')
attributes = ['type', 'title', 'cast', 'rating', 'listed_in']
dataset.fillna('', inplace=True)

#combining the desired features
dataset['combined_features'] = dataset[attributes].apply(lambda x: ' '.join(x), axis=1) 
tfidf_matrix = tfid.fit_transform(dataset['combined_features'])

#equivalent to cosine similarity between the movies
cosine = linear_kernel(tfidf_matrix, tfidf_matrix)

#recommending through similar watches
def recommend_by_title(title, count=5):
    index = pd.Series(dataset.index, index=dataset['title'].drop_duplicates())
    idx = index[title]
    similar = list(enumerate(cosine[idx]))
    similar = sorted(similar, key=lambda x: x[1], reverse=True)
    result_indices = [score[0] for score in similar[1:count+1]]
    result = dataset.loc[result_indices, 'title']
    return list(result)

#recommending by the movie/show's details
def recommend_by_keyword(choice, keyword, type, count):
    recommending_list = []
    new_data = dataset.loc[dataset['type']==choice, ['title', type]]
    for theme in list(enumerate(row for row in new_data[type])):
        words = theme[1].split(' ')
        for element in words:
          for gen in keyword.split(' '):
            if element.lower() == gen.lower():
              recommending_list.append(new_data['title'].iloc[theme[0]])
    
    if len(recommending_list) == 0:
        print('No suitable recommendation available')
        return
    
    result = random.sample(recommending_list, count)
    for x in result:
        print(x)


#recommending by the time period
def recommend_by_date(type, option, count):
    years = [1925, 1960, 1990, 2010, 2021]
    new_data = dataset.loc[dataset['type']==type, ['title']]
    new_data = new_data.loc[dataset['release_year']<=years[option]]
    new_data = new_data.loc[dataset['release_year']>years[option-1]]

    result = random.sample(list(new_data['title']), count)
    for x in result:
        print(x)


if __name__ == '__main__':
    columns = ['listed_in', 'cast', 'director']
    while(True):
        type = int(input("----------Welcome to Netflix Recommendations----------\n\n1. Movies\n2. Shows\n3. Similar Content\nEnter your preference number: "))
        if type in [1,2]:
            column = int(input("1. Genre\n2. Cast\n3. Director\n4. Date of release\n\nWhich of the following would you like to search?: "))
            count = int(input("Specify the number of recommendations: "))
            if column in [1,2,3]:
                keyword = input("Enter the name(s): ")
                print("------Recommendations------\n")
                recommend_by_keyword('Movie' if type == 1 else 'Show', keyword, columns[column-1], count)
                break
            elif column == 4:
                duration = int(input("1. 1925 - 1960\n2. 1960 - 1990\n3. 1990 - 2010\n4. 2010 - 2021\n\nEnter the period number: "))
                print("------Recommendations------\n")
                recommend_by_date('Movie' if type == 1 else 'Show', duration, count)
                break
            else:
                print('Invalid input. Try Again')
        elif type == 3:
            title = input("Enter the movie/show you recently watched: ")
            count = int(input("Specify the number of recommendations: "))
            print("------Recommendations------\n")
            result = recommend_by_title(title, count)
            for x in result:
                print(x)
            break
        else:
            print('Invalid input. Try Again')
           