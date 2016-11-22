import SimpleHTTPServer
import SocketServer
import cgi
import json
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import LSHForest
import numpy as np
from scipy.spatial import distance
from scipy import spatial
import csv
import re

PORT = 8010
data=[]
with open('DataDist1.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        for i in range(1,22):
            row[i]=float(row[i])+float(1.0/21)  #smoothing
        data.append(row)

perc=[]
with open('DataPerc1.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        for i in range(1,22):
            row[i]=float(row[i])  #smoothing
        perc.append(row)


movie_name=[]
# removing movies name
for i in range(len(data)):
    name=data[i].pop(0)
    movie_name.append(name)

movie_name1=[]
# removing movies name
for i in range(len(perc)):
    name=perc[i].pop(0)
    movie_name1.append(name)

for i in range(len(data)):
    for j in range(21):
        data[i][j]=float(data[i][j])

for i in range(len(perc)):
    for j in range(21):
        perc[i][j] = float(perc[i][j])

lshf1 = LSHForest(min_hash_match=4, n_candidates=50, n_estimators=10,
          n_neighbors=5, radius=1.0, radius_cutoff_ratio=0.9,
          random_state=80)
lshf1.fit(perc)
lshf2=  LSHForest(min_hash_match=4, n_candidates=50, n_estimators=10,
          n_neighbors=5, radius=1.0, radius_cutoff_ratio=0.9,
          random_state=80)
lshf2.fit(data)

# movie_from_radar=[.33,0,0,0,.33,0,0,0,0,0,0,0,0,0,0,0,0,.1,0,0,.33]


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")

    def do_GET(self):
        print('((((((((((((')
        for kk in  self.headers.keys():
            print kk+"::::"+self.headers[kk]

        # url = self.headers['Referer']
        # parsed = urlparse.urlparse(url)
        # print parsed
        #print urlparse.parse_qs(parsed.query)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        # print ('*********')
        # for item in form.list:
        #     print (item)
        # print ('*********')
        numarg = form.getvalue('numarg')

        stringarg= form.getvalue('stringarg')
        if(int(numarg)==1):
            sum=0
            pp = [float(i)/100 for i in stringarg.split(',')]
            print pp
           # movie_data = pp
            distance_list1=[]
            # for i in range(len(movie_name1)):
            #     name = movie_name1[i]
            #     if stringarg.lower() in name.lower():
            #         k = i
            #         break

            #movie_data = data[k]

            # X_train = [[5, 5, 2], [21, 5, 5], [1, 1, 1], [8, 9, 1], [6, 10, 2]]
            # X_test = [[9, 1, 6], [3, 1, 10], [7, 10, 3]]

            distances, indices = lshf1.kneighbors(pp, n_neighbors=6)
            # print(distances)
            print(indices)
            i = indices[0, 1]
            sss=[]
            for i in range(len(indices)):
                for j in range(0, len(indices[i])):
                    t=[]
                    t.append(movie_name1[indices[i][j]])
                    sss.append(t)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            #  sss=['Dark Knight','Pride Predu','XYZ MOVIE']
            self.wfile.write('{"end":' +  json.dumps(sss) + '}')


        if(int(numarg)==2):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            print stringarg
            for i in range(len(movie_name)):
                name = movie_name[i]
                if stringarg.lower() in name.lower():
                    k = i
                    break

            movie_data = data[k]


            distances, indices = lshf2.kneighbors(movie_data, n_neighbors=6)
            # print(distances)
            print(indices)
            i = indices[0, 1]
            sss=[]
            for i in range(len(indices)):
                for j in range(0, len(indices[i])):
                    t=[]
                    t.append(movie_name[indices[i][j]])
                    sss.append(t)

            self.wfile.write('{"end":' +  json.dumps(sss) + '}')

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()