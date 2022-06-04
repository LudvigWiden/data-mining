
"""
Apriori Algorithm for generating frequent itemsets
Ludvig Widén
2022-04-10
"""

from tabulate import tabulate

"""
Runs the apriori algorithm and prints each step.
"""
def apriori(D, minsup):
    # D Transactional database
    # minsup Minimum Support
    # output all the large datasets in D in a dictionary.
    not_frequent = []
    itemsets = refactor(D)
    col_names = ['Itemset', 'Sup']

    # Change to list of sets instead of list of lists.
    C0 = [set(items) for items in itemsets]
    # Generate string format for printing
    C_str = [[c] for c in C0]
    print("Candidates\n{0}".format(tabulate(C_str, headers=['itemset'], tablefmt="fancy_grid")))

    C1 = count_sup(C0, D)
    print("C1\n{0}".format(tabulate(C1, headers=col_names, tablefmt="fancy_grid")))
    L1 = filter_minsup(C1, minsup, not_frequent)
    print("L1\n{0}".format(tabulate(L1, headers=col_names, tablefmt="fancy_grid")))


    # Change to list of sets
    L1 = [set(t[0]) for t in L1]

    # Initialize dictionary for large datasets
    Ls = {0: set(), 1 : L1}

    # Iteration variables
    k_start = 2
    max_k = len(itemsets)
    for k in range(k_start, max_k):
        if k-1 in Ls and k-1 != {}:
            # Genereates a list of frequent itemsets
            C = apriori_gen(Ls[k-1], k, not_frequent)
            C_str = [[c] for c in C]
            print("Candidates\n{0}".format(tabulate(C_str, headers=['itemset'], tablefmt="fancy_grid")))
            C_ = count_sup(C, D)
            print("C{0}\n{1}".format(k,tabulate(C_, headers=col_names, tablefmt="fancy_grid")))
            L_ = filter_minsup(C_, minsup, not_frequent)
            print("L{0}\n{1}".format(k,tabulate(L_, headers=col_names, tablefmt="fancy_grid")))
            # New list that only contains the itemsets and not support.
            L_ = [t[0] for t in L_]
            Ls[k] = L_
    return Ls


"""
Create a new list that contains unique items from the transactional database
i.e. [['A'], ['B'] ['C']]
"""
def refactor(D):
    itemsets = []
    for TID in D:
        for item in TID[1]:
            if item not in itemsets:
                itemsets.append(item)
    return itemsets


"""
Generate candidate itemsets
"""
def apriori_gen(itemset, k, not_frequent):
    C = []
    for i in itemset:
        for j in itemset:
            if valid_candidate(C, i.union(j), k, not_frequent):
                C.append(i.union(j))
    return C

"""
Filter candidate itemsets that are: supersets of infrequent itemsets, don't have
the correct length or are already in C (don't add copies).
"""
def valid_candidate(C, candidate,k,not_frequent):
    for nf in not_frequent:
        if nf.issubset(candidate):
            return False

    if (len(candidate) == k):
        for c in C:
            if c.issubset(candidate):
                return False
        return True
    else:
        return False


"""
Scan the transactional database and calculate number of occurencies of a itemset
"""
def count_sup(C, D):
    P = []
    for i in range(len(C)):
        P.append([C[i], 0])
        for t in D:
            items = set(t[1])
            if C[i].issubset(items):
                P[i][1] +=1

    return P


"""
Remove infrequent itemsets
"""
def filter_minsup(C, minsup, not_frequent):
    Ci = []
    for itemset in C:
        if itemset[1] >= minsup:
            Ci.append(itemset)
        else:
            not_frequent.append(itemset[0])
    return Ci


def main(data, minsup):
    tables = {}
    col_names = ["TID", "Items"]
    print("Running the Apriori Algorithm with the following data and minsup {1} \n{0}\n".format(tabulate(data, headers=col_names, tablefmt="fancy_grid"), minsup))
    frequent_itemsets = apriori(data, minsup)
    print()


if __name__ == '__main__':
    data = [
            ['1',['A','B','C','D']],
            ['2',['A','B','D','E']],
            ['3',['A','C','D']],
            ['4',['B','C','D']],
            ['5',['A','B','C','E']]
            ]
    minsup = 2
    main(data, minsup)
