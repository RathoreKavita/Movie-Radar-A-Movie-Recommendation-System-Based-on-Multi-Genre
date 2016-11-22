import random
import math
import matplotlib.pyplot as plt
import csv

a = []
with open('DataDist.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        for i in range(1,22):
            row[i]=float(row[i])+float(1.0/21)  #smoothing
        a.append(row)

movie_name=[]
for i in range(len(a)):
    name=a[i].pop(0)
    movie_name.append(name)

def distance(point, center):
	sum=0
	for i in range(7):
		num=float(point[i])-float(center[i])
		sum=sum+math.pow(num,2)
	return math.sqrt(sum)





def classifyPoints(centroids):
	# x contains clusters
	x = [[] for i in range(len(centroids))]
	#print(len(centroids))
	for i in range(len(a)):   #replace with 210
		min_dist=10000;
		label=51;
		for j in range(len(centroids)):
			dist=distance(a[i],centroids[j])
			#print(type(a[i]))
			#print(dist)
			if(dist<min_dist):
				min_dist=dist
				label=j;
				#print(j)
		x[label].append(a[i]) 		#clusters
	return x




def getCentroids(clusters):
	new_centroid=[];
	for i in range(len(clusters)):
		curr_cluster=clusters[i]
		if(len(curr_cluster)==0):
			print("zero length")
		else:
			avg=[]

			for k in range(21):
				summ=0;
				for j in range(len(curr_cluster)):
					summ=summ+float(curr_cluster[j][k])
				avge=summ/len(curr_cluster)
				avg.append(avge)
			new_centroid.append(avg)
	return new_centroid



def kmeans(k):
	distn=1000
	dist_list=[]
	print(k)
	threshold_dist=5;
	centroids=getRandomCentroids(k);
	iterations = 0

	while(iterations<200):
		iterations=iterations+1
		print(iterations)
		oldCentroids = centroids
		clusters=classifyPoints(centroids)
		new_cent=getCentroids(clusters)
		centroids=new_cent

def getRandomCentroids(k):
	cent=[]
	l1=random.sample(range(0,210),k)
	for i in range(k):
		cent.append(a[l1[i]])
		#print(type(cent))
	return cent



kmeans(50)






