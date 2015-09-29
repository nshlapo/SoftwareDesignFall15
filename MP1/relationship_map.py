import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from pattern.web import *
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time

w = Wikipedia()

def get_related_articles(query):
    """Search the wikipedia page of query
    and return all related articles in a list.
    """

    article = w.search(query)
    related_list = []
    print "  Searching through " + str(article.title)
    # find the See Also section on the webpage
    for section in article.sections:
        if section.title == 'See also':
            # grab links from that section
            links = section.links
            for link in links:
                if 'List of' not in link and 'Lists of' not in link: # don't add wiki pages that are just lists
                    related_list.append(link)
    return related_list

def scan_articles(input_dict):
    """Add related articles to input dict for each value in dict."""

    temp_dict = {}
    for key in input_dict:
        for ele in input_dict[key]:
            # Don't search for value that is already a key, or doesn't exist
            if (not related_dict.has_key(ele)) and (type(ele) is not 'NoneType'):
                temp_dict[ele] = get_related_articles(ele)
    related_dict.update(temp_dict)

def onclick(event):
    """Open a node's webpage if it is clicked on."""

    global ix, iy
    # store click location
    ix, iy = event.xdata, event.ydata
    node = is_node(ix, iy)
    if node[0]:
        # open Wikipedia page of cliked node
        driver = webdriver.Firefox()
        driver.get("http://en.wikipedia.org/wiki/" + node[1])

def is_node(ix, iy):
    """Check if a click event occured on a node."""

    for ele in pos.items():
        # calculate distance from click location to node
        dx = ele[1][0] - ix
        dy = ele[1][1] - iy
        r = pow(pow(dx,2) + pow(dy,2),.5)
        if r < .05:
            return (True, ele[0], ele[1])
    return (False, 0)

# start program with user input
search = raw_input("What subject would you like to generate a map for?")
depth = raw_input("What depth should the map be (start with 1 or 2)?")

# perform the searches
related_dict = {}
related_dict[search] = get_related_articles(search)
for i in range(int(depth)):
    print "Depth " + str(i+1)
    scan_articles(related_dict)

# set up figure for plotting
fig=plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Articles related to ' + search + '\n Click on nodes to find out more about them')
plt.axis('off')

# create network graph
G = nx.Graph(related_dict)
pos=nx.spring_layout(G)
# pass button press event information
cid = fig.canvas.mpl_connect('button_press_event', onclick)
nx.draw_networkx(G, pos=pos, ax=ax, node_size=300)
plt.show()