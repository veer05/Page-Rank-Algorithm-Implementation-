import math
#Repesents the inlink graph
doc_id_inlink_dict = dict()
#Represents the outlink graph
doc_id_outlink_dict = dict()
#number of pages with no outlinks
num_of_outlinks = dict()
#Page and PageRank dictonary
PR = dict()
new_PR=dict()
#Damping Factor
d = 0.85
#P represents the total number of pages
P = []
#Number of sink pages
S = []
# Read the Graph and generate Inlink dictionary
def read_inlinks_from_file(filename):
    file = open(filename, "r+")
    line = file.readlines()
    doc_id = []
    # Creating a Dictionary which has DocID and List of incoming links from other DocID
    for i in line:
        j = i.strip()
        id = j.split()
        doc_id.append(id[0])
    for doc in doc_id:
        doc_id_inlink_dict.setdefault(doc, [])
    #Giving Values to Key in the Dictionary
    for i in line:
        j = i.strip()
        docs = j.split()
        doc_id_inlink_dict[docs[0]] = list(set(docs[1:]))
    file.close()
#    print(doc_id_inlink_dict)
#generate outlink for the given graph
def generate_outlinks():
    for key in doc_id_inlink_dict.keys():
        doc_id_outlink_dict.setdefault(key,[])
    for key,value in doc_id_inlink_dict.iteritems():
        for i in value:
            if i in doc_id_inlink_dict:
                doc_id_outlink_dict[i].append(key)
 #   print(doc_id_outlink_dict)
#calculate number of pages with no outlinks
def pages_with_no_outlinks():
    P = doc_id_inlink_dict.keys()
    inlink_set = set((doc_id_inlink_dict.keys()))
    for docs in P:
        in_cominglink = doc_id_inlink_dict[docs]
        for link in in_cominglink:
            if link in num_of_outlinks:
                num_of_outlinks[link] = num_of_outlinks[link] + 1
            else:
                num_of_outlinks[link] = 1
#    print(num_of_outlinks)
    num_outlink_set = set(num_of_outlinks.keys())
    S = (list(inlink_set - num_outlink_set))
    print "sink ", (len (S))
#calculate page rank
def calc_pg():
    d = 0.85
    P = doc_id_inlink_dict.keys()
    perplexity_convergence_count = 0
    num_outlink_set = set(num_of_outlinks.keys())
    inlink_set = set((doc_id_inlink_dict.keys()))
    S = (list(inlink_set - num_outlink_set))
#    print(S)
    perp = 0
#    print(P)
    for page in P:
        PR[page] = (1.0 / len (P))
#    print(P)
    while perplexity_convergence_count < 4:
        sinkPR = 0
        print perp
        old_perplexity = perp
        for sink in S:
            sinkPR = sinkPR + PR[sink]
#        print(sinkPR)
        for page in P:
            new_PR[page] = (1 - d) / len (P)
            new_PR[page] += d * sinkPR / len (P)
            try:
                for q in doc_id_inlink_dict[page]:
                    new_PR[page] += d * PR[q] / (num_of_outlinks[q])
            except:
                pass
        for page in P:
            PR[page] = new_PR[page]
        entropy = calc_entropy()
#        print(entropy)
        perp = math.pow(2, -entropy)
        if abs(old_perplexity - perp) < 1:
            perplexity_convergence_count += 1
        else:
            perplexity_convergence_count=0
# Calculate Entropy
def calc_entropy():
    entropy = 0
    P = doc_id_inlink_dict.keys()
    for i in P:
        entropy += PR[i] * math.log(float(PR[i]), 2)
    return entropy
#print outputfile with sorted ranks
def print_output():
    ranked_pages = (list(set(PR.values())))
    rank_list = sorted (ranked_pages, reverse=True)
    f=open("PAGERANK_DFS_1.txt",'w+')
    for entry in rank_list[0:50]:
        for key, val in PR.iteritems():
            if entry == val:
                f.write(str(key)+' '+ str(entry)+'\n')

    f.close()
# GENRATES Inlinks Outlinks and calculates PageRank
def rank_pages():
    read_inlinks_from_file('gfs_new_graph_new.txt')
    generate_outlinks()
    pages_with_no_outlinks()
    calc_pg()
    print_output()


#CALLING MAIN FUNCTION
rank_pages()