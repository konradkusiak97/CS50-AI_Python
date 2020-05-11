import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    #if len(sys.argv) != 2:
     #   sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl('corpus0')
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    numPages = len(corpus)
    numLinks = len(corpus[page])
    probDict = dict()
    if numLinks == 0:
        probability = 1/numPages
        for myPage in corpus:
            probDict[myPage] = probability
        return probDict
    
    everyProb = (1-damping_factor)/numPages
    linkProb = damping_factor/numLinks
    for link in corpus[page]:
        probDict[link] = everyProb+linkProb
    for myPage in corpus:
        if myPage not in probDict:
            probDict[myPage] = everyProb

    return probDict

        


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    finalValues = dict()
    numPages = len(corpus)
    pages = list(corpus.keys())

    # Initializing all probabilities to 0
    for p in pages:
        finalValues[p] = 0

    currentPage = random.choice(pages)
    finalValues[currentPage] += 1
    for j in range(n):
        distribution = transition_model(corpus, currentPage, damping_factor)
        population = list(distribution.keys())
        weights = list(distribution.values())
        currentPage = random.choices(population, weights)[0]
        finalValues[currentPage] += 1
    
    for newPage in finalValues:
        finalValues[newPage] /= n
    
    return finalValues
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # The newCorpus is going to have the same keys but different values.
    # The values will be a set of pages that link to this page, not the other way
    
    k = set(corpus.keys())          # Managing the '0 outgoing links' situation
    for p in corpus:
        if len(corpus[p]) == 0:
            corpus[p] = k

    # changing corpus 
    newCorpus = dict()
    for p in corpus:
        links = set()
        for j in corpus:
            if p in corpus[j]:
                links.add(j)
        newCorpus[p] = links

    # Initialization
    numPages = len(corpus)
    pageRank = dict()
    for page in corpus:
        pageRank[page] = 1/numPages

    # Main pageRank calculations
    stable = False
    while not stable:
        currentPageRank = copy.deepcopy(pageRank)
        for page in newCorpus:
            links  = newCorpus[page]
            pr = (1-damping_factor)/numPages
            for l in links:
                pr += damping_factor * pageRank[l]/len(corpus[l])
            pageRank[page] = pr
        # Checking if the result is stable up to 0.001
        i = 0 
        for newPr in pageRank:
            change = pageRank[newPr]-currentPageRank[newPr]
            if abs(change) > 0.001:
                break
            i += 1
        if i == len(pageRank):
            stable = True
    return pageRank

if __name__ == "__main__":
    main()
