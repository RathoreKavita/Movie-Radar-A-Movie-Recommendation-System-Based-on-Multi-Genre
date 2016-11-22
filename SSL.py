from sklearn.neighbors import NearestNeighbors
import numpy as np
from scipy.spatial import distance
from scipy import spatial
import csv
import re
data=[]
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

movie_from_radar=[.33,0,0,0,.33,0,0,0,0,0,0,0,0,0,0,0,0,.1,0,0,.33]
distance_list=[];
distanceVar=raw_input("enter the distance")
option_var=input("enter the option")
print(type(option_var))

if option_var==1:
    testVar = raw_input("Ask user for movie name.")
    ## movie name to index
    for i in range(len(movie_name)):
        name=movie_name[i]
        if testVar.lower() in name.lower():
            k=i
            break

    movie_data=data[k]

if option_var==2:
    movie_data=movie_from_radar

if distanceVar == 'euclidean':
    print("dsdsd")
    for i in range(len(data)):
        dist = distance.euclidean(movie_data,data[i])
        distance_list.append(dist)

if distanceVar == 'cosine':
    print("cosine")
    for i in range(len(data)):
        dist = spatial.distance.cosine(movie_data,data[i])
        distance_list.append(dist)

if distanceVar == 'hamming':
    print("inside hamming")
    for i in range(len(data)):
        dist = distance.hamming(movie_data,data[i])
        distance_list.append(dist)

if distanceVar == 'minkowski':
    print("inside ")
    for i in range(len(data)):
        dist = distance.minkowski(movie_data,data[i],5)
        distance_list.append(dist)


index_list=[i[0] for i in sorted(enumerate(distance_list), key=lambda x:x[1])]


for i in range(6):
    j=int(index_list[i])
    #print(type(j))
    print(movie_name[j])






