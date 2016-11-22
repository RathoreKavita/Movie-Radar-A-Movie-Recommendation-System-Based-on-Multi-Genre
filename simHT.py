import SimpleHTTPServer
import SocketServer
import cgi
import json
from sklearn.neighbors import NearestNeighbors
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
            print stringarg
            pp = [float(i)/100 for i in stringarg.split(',')]

            print pp
            movie_data = pp
            distance_list1=[]
            for i in range(len(perc)):
                dist = distance.euclidean(movie_data, perc[i])
                distance_list1.append(dist)
            index_list1=[]
            index_list1 = [i[0] for i in sorted(enumerate(distance_list1), key=lambda x: x[1])]
            sss=[]
            for i in range(6):
                j = int(index_list1[i])
                t = []
                t.append(movie_name1[j])
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
            distance_list = []
            for i in range(len(data)):
                dist = distance.euclidean(movie_data, data[i])
                distance_list.append(dist)
            index_list=[]
            index_list = [i[0] for i in sorted(enumerate(distance_list), key=lambda x: x[1])]
            sss=[]
            for i in range(6):
                j = int(index_list[i])
                # print(type(j))
                t=[]
                t.append(movie_name[j])
                sss.append(t)
            self.wfile.write('{"end":' +  json.dumps(sss) + '}')

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()