import pickle
import networkx as nx
from random import shuffle


alpha = 0.85
#number of nodes in webspam
nodes = 11402
c = 1 - alpha

G = nx.DiGraph()

with open("data/edges.txt", "rb") as f:
    edges = pickle.load(f)
f.close()


with open("data/spamlist.txt", "rb") as f:
    spam = pickle.load(f)
f.close()


with open("data/whitelist.txt", "rb") as f:
    whitelist = pickle.load(f)
f.close()

G.add_nodes_from(range(nodes))

G.add_weighted_edges_from(edges)

#sort whitelist by max outdegree
sorted_whitelist = sorted(whitelist, key=G.out_degree, reverse=True)

#Uncomment for obtaining a random perm of whitelist
#sorted_whitelist = whitelist
#shuffle(sorted_whitelist)


#personalization vectors
per1 = {key:0 for key in range(nodes)}
per1[sorted_whitelist[0]] = 10

per2 = {key:0 for key in range(nodes)}
per2[sorted_whitelist[1]] = 10

per3 = {key:0 for key in range(nodes)}
per3[sorted_whitelist[2]] = 10

per4 = {key:0 for key in range(nodes)}
per4[sorted_whitelist[3]] = 10

per5 = {key:0 for key in range(nodes)}
per5[sorted_whitelist[4]] = 10

per6 = {key:0 for key in range(nodes)}
per6[sorted_whitelist[5]] = 10

per7 = {key:0 for key in range(nodes)}
per7[sorted_whitelist[6]] = 10

per8 = {key:0 for key in range(nodes)}
per8[sorted_whitelist[7]] = 10


#Page rank for each personlization vector
pr1 = nx.pagerank(G, personalization=per1, weight=None)
pr2 = nx.pagerank(G, personalization=per2, weight=None)
pr3 = nx.pagerank(G, personalization=per3, weight=None)
pr4 = nx.pagerank(G, personalization=per4, weight=None)
pr5 = nx.pagerank(G, personalization=per5, weight=None)
pr6 = nx.pagerank(G, personalization=per6, weight=None)
pr7 = nx.pagerank(G, personalization=per7, weight=None)
pr8 = nx.pagerank(G, personalization=per8, weight=None)

#Computer min-wise page rank
pr_min = {}

for i in range(nodes):
    #pr_min[i] = min(pr1[i], pr2[i])
    #pr_min[i] = min(pr1[i], pr2[i], pr3[i], pr4[i])
    pr_min[i] = min(pr1[i], pr2[i], pr3[i], pr4[i], pr5[i], pr6[i], pr7[i], pr8[i])

#Compute the corresponding reset vector
reset = {}

for i in range(nodes):
    reset[i] = pr_min[i]/(1-c)
    sum_ = 0
    for x in G.in_edges(i):
        sum_ = sum_ + pr_min[x[0]]/(G.out_degree(x[0]))
    sum_ = c*sum_/(1-c)
    reset[i] = reset[i] - sum_

#Normailzie reset vector
factor = 1.0/sum(reset.itervalues())

for k in reset:
    reset[k] = reset[k]*factor

#Print Stats
print sum(reset[i] for i in spam)
print sum(reset[i] for i in whitelist)
print sum(reset[i] for i in spam)/len(spam)
print sum(reset[i] for i in whitelist)/len(whitelist)

avg = 1.0/(nodes-len(spam))
sum_a = 0.0
for i in range(nodes):
    if not i in spam:
        sum_a = sum_a + ((reset[i]-avg)*(reset[i]-avg))

print "Variance ", sum_a 


#Normalize page rank vector
#factor = 1.0/sum(pr_min.itervalues())

#for k in pr_min:
#    pr_min[k] = pr_min[k]*factor
