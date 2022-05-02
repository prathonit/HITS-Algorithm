import time
from hits import HITS
from argparse import ArgumentParser
from nltk.stem import PorterStemmer
from tabulate import tabulate

ps = PorterStemmer()


"""
This program calculates the hub and auth scores of a given search query for a web graph
"""


def pre_process_query(term):
    """To preprocess the search term, converts to lower case, strips whitespaces and stems the term"""
    term = term.lower()
    term = term.strip()
    term = ps.stem(term)
    return term


def serialize(scores):
    for i in range(len(scores)):
        scores[i][1] = round(scores[i][1], 5)
        scores[i][2] = round(scores[i][1], 5)
    return scores


def main():
    """Accepts the command line arguments and passes those to an instance of HITS class, prints the result"""
    arguments = ArgumentParser()
    arguments.add_argument("-f", "--query", help="Search term")
    args = arguments.parse_args()

    h = HITS()
    start = time.time()
    hits_res = h.calc_hit_score(pre_process_query(args.query))
    # if hits_res is None:
    #     return
    end = time.time()
    scores = serialize(hits_res['scores'])
    root_set = hits_res['root_set']
    base_set = hits_res['base_set']
    base_set.sort()
    print('Root Set: ', root_set)
    print('Base Set: ', base_set)
    scores.sort(key=lambda x: (x[0]))
    print('Auth Hub Scores: ')
    print(tabulate(scores, headers=['DocID', 'Auth Score', 'Hub Score']))
    print()
    top_auth_scores = []
    top_hub_scores = []
    scores.sort(key=lambda x: (-x[1], x[0]))
    for i in range(3):
        if i < len(scores):
            top_auth_scores.append((scores[i][0], scores[i][1]))
    scores.sort(key=lambda x: (-x[2], x[0]))
    for i in range(3):
        if i < len(scores):
            top_hub_scores.append((scores[i][0], scores[i][2]))
    print('Top auth scores: ')
    print(tabulate(top_auth_scores, headers=['DocID', 'Auth Score']))
    print()
    print('Top hub scores: ')
    print(tabulate(top_hub_scores, headers=['DocID', 'Hub Score']))
    print('Runtime: ', (end - start) * 1000, 'milli secs')


if __name__ == "__main__":
    main()


