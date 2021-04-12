from urllib.parse import urlparse

import PageRankCalculator
from bs4 import BeautifulSoup
import requests
from graphviz import Digraph
from tabulate import tabulate
import csv

DOMAIN = 'twitter.com'
HOST = 'http://' + DOMAIN
helping_map = []
dot = Digraph(comment='graph')
d = {}
FORBIDDEN_PREFIXES = ['#', 'tel:', 'mailto:']
links = set()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(HOST, headers=headers)


def add_all_links(depth, url, max_depth):
    if depth > max_depth:
        return
    links_to_handle_recursive = []
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, 'lxml')
    for tag_a in soup.find_all('a', href=lambda v: v is not None):
        link = tag_a['href']
        if all(not link.startswith(prefix) for prefix in
               FORBIDDEN_PREFIXES):
            if link.startswith('/') and not link.startswith('//'):
                link = HOST + link
            if urlparse(link).netloc == DOMAIN:
                if depth != max_depth:
                    if link not in links:
                        dot.node(str(len(links)), link)
                        dot.edge(str(get_key(d, url)), str(len(links)))
                        helping_map.append([get_key(d, url), len(d)])
                        d[len(links)] = link
                        links.add(link)
                        links_to_handle_recursive.append(link)
                    else:
                        dot.edge(str(get_key(d, url)), str(get_key(d, link)))
                        helping_map.append([get_key(d, url), get_key(d, link)])
                else:
                    if link in links:
                        dot.edge(str(get_key(d, url)), str(get_key(d, link)))
                        helping_map.append([get_key(d, url), get_key(d, link)])
    if depth < max_depth:
        for link in links_to_handle_recursive:
            add_all_links(depth + 1, link, max_depth=max_depth)


def links_traversal(root_url, max_depth):
    links.add(root_url)
    dot.node(str(0), root_url)
    d[0] = root_url
    add_all_links(0, root_url, max_depth=max_depth)


def get_key(a, value):
    for k, v in a.items():
        if v == value:
            return k


def creating_matrix_of_transitivity(a):
    count = 0
    for i in range(len(a)):
        if a[i][1] > count:
            count = a[i][1]
    count += 1
    matrix = [[0] * count for i in range(count)]
    outLinks = [0] * count
    for i in range(len(a)):
        matrix[a[i][0]][a[i][1]] += 1
        outLinks[a[i][0]] += 1
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if outLinks[i] != 0:
                matrix[i][j] /= outLinks[i]
    f = open('TransitionMatrix.txt', 'w')
    f.write(str(tabulate(matrix)))
    f.close()
    return matrix


def sum_of_elements(v):
    sum = 0
    for i in range(len(v)):
        sum += v[i]
    return sum


def main():
    links_traversal(HOST + '/', 3)
    for link in links:
        print(link)
    print(dot.source)
    dot.render('D:\\PythonProjects\\secondProject\\graph', view=True)
    array = creating_matrix_of_transitivity(helping_map)
    v = [1 / len(links) for i in range(len(links))]
    e = [1 for i in range(len(links))]
    v = PageRankCalculator.calc(array, v, e, len(links))
    rating_of_pg = {}
    for i in range(len(v)):
        rating_of_pg[d.get(i)] = v[i]
    list_items = list(rating_of_pg.items())
    list_items.sort(key=lambda i: i[1], reverse=True)
    f = open('rating.txt', 'w')
    for i in list_items:
        f.write(str(i[0]) + ' : ' + str(i[1]) + '\n')
    f.write('\n' + 'SUM = ' + str(sum_of_elements(v)))
    f.close()


if __name__ == '__main__':
    main()
