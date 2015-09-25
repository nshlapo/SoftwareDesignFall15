import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from pattern.web import *

w = Wikipedia()
record = open('record.txt', 'w')

def get_related_articles(query):
    article = w.search(query)
    related_list = []
    print "Searching through " + str(article.title)
    for section in article.sections: # find the See Also section
        if section.title == 'See also':
            links = section.links
            for link in links:
                if 'List of' not in link and 'Lists of' not in link:
                    related_list.append(link)
    return related_list

def scan_articles(input_dict):
    temp_dict = {}
    for key in input_dict:
        for ele in input_dict[key]:
            if (not test_dict.has_key(ele)) and (type(ele) is not 'NoneType'):
                temp_dict[ele] = get_related_articles(ele)
    test_dict.update(temp_dict)

test_dict = {}
search = 'Film'
test_dict[search] = get_related_articles(search)

scan_articles(test_dict)
# scan_articles(test_dict)
# scan_articles(test_dict)
# print test_dict

G = nx.Graph(test_dict)
# nx.draw_networkx(G, cmap)
# plt.show()
D = nx.to_dict_of_dicts(G)
print D

""" To do:
Hover over nodes to display label
Click on label to open Wikipedia article
Color nodes by depth
Display total number of nodes dependant on initial search
Display interconnectedness??
"""

