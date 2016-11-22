from sklearn.neighbors import LSHForest
import csv
data=[]
import numpy as np

with open('DataDist.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        for i in range(1,22):
            row[i]=float(row[i])+float(1.0/21)  #smoothing
        data.append(row)


movie_name=[]
# removing movies name
for i in range(len(data)):
    name=data[i].pop(0)
    movie_name.append(name)

for i in range(len(data)):
    for j in range(21):
        data[i][j]=float(data[i][j])

testVar = raw_input("Ask user for movie name.")
for i in range(len(movie_name)):
    name=movie_name[i]
    if testVar.lower() in name.lower():
        k=i
        break

movie_data=data[k]


#X_train = [[5, 5, 2], [21, 5, 5], [1, 1, 1], [8, 9, 1], [6, 10, 2]]
#X_test = [[9, 1, 6], [3, 1, 10], [7, 10, 3]]
lshf = LSHForest(random_state=42)
lshf.fit(data)

LSHForest(min_hash_match=4, n_candidates=50, n_estimators=10,
          n_neighbors=5, radius=1.0, radius_cutoff_ratio=0.9,
          random_state=42)
distances, indices = lshf.kneighbors(movie_data, n_neighbors=6)
print(distances)
print(len(indices))
i=indices[0,1]

for i in range(len(indices)):
    for j in range(0,len(indices[i])):

        print(movie_name[indices[i,j]])
