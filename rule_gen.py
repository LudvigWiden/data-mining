"""
Rule generation algorithm
Ludvig Widén
2022-04-
"""
from itertools import permutations

database = [
            ['A', 'B', 'C'],
            ['A', 'B', 'C', 'D', 'E'],
            ['A', 'C', 'D'],
            ['A', 'C', 'D','E'],
            ['A', 'B', 'C', 'D']
            ]


"""
Calculate the support of an item
"""
def support(item):
    count = 0
    for transaction in database:
        if set(item).issubset(set(transaction)):
            count+=1
    return count/len(database)


"""
Print unique rules
"""
def output(key, rule):
    key = str(key)

    if not key in d:
        d[key] = rule
        print(rule)


"""
Rule generation algorithm
@itemset the itemset to generate rules from
@subset recursion worker itemset
@minsup minimum support 0<minsup<=1
"""
def genrules(itemset, subset, minsup):
    N = len(subset)-1
    A = []

    pool = tuple(subset)
    n = len(pool)
    for indices in permutations(range(n), N):
        if sorted(indices) == list(indices):
            tup = [pool[i] for i in indices]
            if tup not in A:
                A.append(tup)

    for a in A:
        conf = support(itemset)/support(a)
        b = []
        for it in itemset:
            if it not in a:
                b.append(it)

        if conf >= minsup:
            key = (a,b)
            output(key,f"{a} --> {b}, with confidence {conf} and support {support(itemset)}")
            if len(subset)-1 > 1:
                genrules(itemset, a, minsup)



if __name__ == '__main__':
    confidence = 0.8
    itemset = ['A', 'B', 'C']
    d = {}
    rules = genrules(itemset, itemset, confidence)
