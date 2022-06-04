"""
Clustering Algorithms in graph abstraction
Ludvig Widén
2022-04-11
"""
import random

"""
A State is a pair of two medoids
"""
class State:
    def __init__(self, medoid_par):
        self.medoid_par = medoid_par
        self.neighbors = []

    def add_neighbors(self, neighbor):
        self.neighbors.append(neighbor)

    def get_neighbors(self):
        return self.neighbors

    def get_points(self):
        return self.medoid_par[0], self.medoid_par[1]

    def get_medoids(self):
        return self.medoid_par

    def is_neighbor(self, medoid):
        np1,np2 = medoid.get_points()
        p1,p2 = self.get_points()
        return (p1==np1 or p1 == np2 or p2==np1 or p2 == np2)

def distance_to(p1, p2):
    # 2D
    if not isinstance(p1, int): # If data consists of 2D samples
        dX = abs(p2[0]-p1[0])
        dY = abs(p2[1]-p1[1])
        return dX+dY
    else: # 1D Samples
        return abs(p2-p1)


"""
Create a graph abstraction
"""
def make_graph(points):
    num_of_points = len(points)
    medoid_pars = []
    # Generate medoids
    for i in range(num_of_points-1):
        p1 = points[i]
        for j in range(i+1, num_of_points):
            p2 = points[j]
            medoid_pars.append(State((p1, p2)))
    # Update neighbors
    for m1 in medoid_pars:
        for m2 in medoid_pars:
            if m1.get_points() != m2.get_points():
                if m1.is_neighbor(m2):
                    m1.add_neighbors(m2)
    return medoid_pars

def assign_calculate_cost(p1,p2,data):
    cluster1 = []
    cluster2 = []
    total_cost = 0
    # Assign each remaining object to nearest medoids
    for point in data:
        cost1 = distance_to(p1, point)
        cost2 = distance_to(p2, point)
        # Assign to clusters and calculate the total cost
        if(cost1 < cost2):
            cluster1.append(point)
            total_cost += cost1
        else:
            cluster2.append(point)
            total_cost += cost2
    return cluster1, cluster2, total_cost

"""
PAM Algorithm
"""
def PAM(graph, data):
    iterations = 5
    # Arbitrary choose 2 objects as initial medoids
    medoids = random.choice(graph)
    p1, p2 = medoids.get_points()

    # Assign each remaining object to nearest medoids
    cluster1,cluster2,total_cost = assign_calculate_cost(p1,p2,data)
    print("Initial Medoids:", medoids.get_points())
    print("Initial Cluster 1:",cluster1)
    print("Initial Cluster 2:",cluster2)
    print("Initial Total cost:",total_cost)

    # Loop for a certain number of iterations or until there is no improvement.
    for it in range(1, iterations+1):
        #print_neighbors(medoids)
        swaps = 0
        # Find the best neighbor medoid par
        for n in medoids.get_neighbors():
            p1,p2 = n.get_points()
            new_cluster1,new_cluster2,new_cost=assign_calculate_cost(p1,p2,data)
            cost_diff = new_cost-total_cost

            # Swap O with O_neighbor for best pair if quality is improved
            if cost_diff < 0:
                swaps += 1
                medoids = n
                cluster1 = new_cluster1
                cluster2 = new_cluster2
                total_cost = new_cost

        print("------Iteration {0}-------------------".format(it))
        print("Medoids:", medoids.get_points())
        print("Cluster 1:",cluster1)
        print("Cluster 2:",cluster2)
        print("Total cost:",total_cost)
        print("Swaps:", swaps)
        print("-----------------------------------")
        if swaps == 0:
            print("Done: No change")
            break;


def print_graph(graph):
    for medo in graph:
        print("Medoid:",medo.get_medoids())
        for neighbors in medo.get_neighbors():
            print("Neighbor:",neighbors.get_points())

def print_neighbors(medo):
    for n in medo.get_neighbors():
        print(n.get_points())

"""
CLARA Algorithm
"""
def CLARA(graph):
    iterations = 1
    pass


"""
CLARANS Algorithm
"""
def CLARANS(graph):
    iterations = 1
    pass


def main(data, algorithm):
    print("\n")
    G = make_graph(data)
    #print_graph(G)
    if algorithm == "PAM":
        PAM(G, data)
    elif algorithm == "CLARA":
        CLARAN(G)
    else:
        CLARANS(G)



if __name__ == '__main__':
    data_set1 = [(0,0),(0,1),(4,4),(5,3)]
    data_set2 = [0, 7, 8, 10, 2, 4, 13, 14, 17, 25, 3, 19, 1, 22, 5]
    main(data_set2, "PAM")
