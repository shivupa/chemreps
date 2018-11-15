import numpy as np
connectivity = [[1, 2],
        [1, 6],
        [1, 8],
        [2, 9],
        [2, 4],
        [3, 2],
        [3, 4],
        [4, 12],
        [4, 5],
        [5, 15],
        [5, 14],
        [7, 1],
        [10, 3],
        [11, 3],
        [13, 5]]
connectivity = np.array(connectivity)

def adjacency_matrix(connectivity):
    num_atoms = np.max(connectivity.ravel())
    adj_mat = np.zeros((num_atoms,num_atoms))
    for pair in connectivity:
        adj_mat[pair[0]-1,pair[1]-1] = 1
        adj_mat[pair[1]-1,pair[0]-1] = 1
    return adj_mat
adj_mat = adjacency_matrix(connectivity)
adj_mat = np.nonzero(adj_mat)
# print(np.nonzero(adj_mat))
for i,j in zip(adj_mat[0],adj_mat[1]):
    print(i,j)
# print(np.dot(adj_mat,adj_mat))








def torsions(conn):
    torsion = []
    for i in range(len(conn)):
        a = conn[i][1]
        for j in range(len(conn)):
            if conn[j][0] == a:
                b = conn[j][1]
                for k in range(len(conn)):
                    if (conn[k][0] == a) or (conn[k][1] == a):
                        pass
                    elif conn[k][0] == b:
                        c = conn[k][1]
                        for l in range(len(conn)):
                            if (conn[l][0] == (a or b)):
                                pass
                            elif (conn[l][1] == (a or b)):
                                pass
                            elif conn[l][0] == c:
                                d = conn[l][1]
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torsion:
                                        torsion.append(abcd)
                            elif conn[l][1] == c:
                                d = conn[l][0]
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torsion:
                                        torsion.append(abcd)
                    elif conn[k][1] == b:
                        c = conn[k][0]
                        for l in range(len(conn)):
                            if (conn[l][0] == (a or b)):
                                pass
                            elif (conn[l][1] == (a or b)):
                                pass
                            elif conn[l][0] == c:
                                d = conn[l][1]
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torsion:
                                        torsion.append(abcd)
                            elif conn[l][1] == c:
                                d = conn[l][0]
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torsion:
                                        torsion.append(abcd)
            elif conn[j][1] == a:
                b = conn[j][0]
                for k in range(len(conn)):
                    if (conn[k][0] == a) or (conn[k][1] == a):
                        pass
                    elif conn[k][0] == b:
                        c = conn[k][1]
                        for l in range(len(conn)):
                            if (conn[l][0] == (a or b)):
                                pass
                            elif (conn[l][1] == (a or b)):
                                pass
                            elif conn[l][0] == c:
                                d = conn[l][1]
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torsion:
                                        torsion.append(abcd)
                            elif conn[l][1] == c:
                                d = conn[l][0]
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torsion:
                                        torsion.append(abcd)
                    elif conn[k][1] == b:
                        c = conn[k][0]
                        for l in range(len(conn)):
                            if (conn[l][0] == (a or b)):
                                pass
                            elif (conn[l][1] == (a or b)):
                                pass
                            elif conn[l][0] == c:
                                d = conn[l][1]
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torsion:
                                        torsion.append(abcd)
                            elif conn[l][1] == c:
                                d = conn[l][0]
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torsion:
                                        torsion.append(abcd)

    return duplicate(torsion)


def duplicate(k):
    newtor = []
    for i in k:
        if i not in newtor:
            newtor.append(i)
    return newtor


# tors = torsions(connectivity)
# print(tors)
# print(len(tors))
