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

def angles(adj_mat, return_adj_mat_sq=False):
    num_atoms = np.shape(adj_mat)[0]
    if return_adj_mat_sq:
        adj_mat_sq = np.dot(adj_mat,adj_mat)
        # adj_mat_sq[np.tril_indices(num_atoms,-1)]
        adj_mat_sq_masked = adj_mat_sq
        adj_mat_sq_masked[np.tril_indices(num_atoms)] = 0
    else:
        adj_mat_sq_masked = np.dot(adj_mat,adj_mat)
        adj_mat_sq_masked[np.tril_indices(num_atoms)] = 0
    angles = []
    for atom_i in range(num_atoms):
        atom_i_angles_with = np.nonzero(adj_mat_sq_masked[atom_i])[0]
        atom_i_bonded_to = np.nonzero(adj_mat[atom_i])[0]
        for atom_k in atom_i_angles_with:
            atom_k_bonded_to = np.nonzero(adj_mat[atom_k])[0]
            atoms_ik_connections_through = set(atom_i_bonded_to) & set(atom_k_bonded_to)
            for atom_j in atoms_ik_connections_through:
                angles.append([atom_i,atom_j,atom_k])
    # for i in angles:
        # print(i)
    if return_adj_mat_sq:
        return angles,adj_mat_sq
    else:
        return angles

def torsions(adj_mat, adj_mat_sq = None):
    num_atoms = np.shape(adj_mat)[0]
    if adj_mat_sq is None:
        adj_mat_sq = np.dot(adj_mat,adj_mat)
    adj_mat_cb = np.dot(adj_mat,adj_mat_sq)
    adj_mat_cb[np.tril_indices(num_atoms)] = 0
    torsions = []
    for atom_i in range(num_atoms):
        atom_i_bonded_to = np.nonzero(adj_mat[atom_i])[0]
        atom_i_angles_with = np.nonzero(adj_mat_sq[atom_i])[0]
        atom_i_torsions_with = np.nonzero(adj_mat_cb[atom_i])[0]
        for atom_l in atom_i_torsions_with:
            atom_l_bonded_to = np.nonzero(adj_mat[atom_l])[0]
            atom_l_angles_with = np.nonzero(adj_mat_sq[atom_l])[0]
            paths_starting_at_i_through = set(atom_i_bonded_to) & set(atom_l_angles_with)
            paths_starting_at_l_through = set(atom_l_bonded_to) & set(atom_i_angles_with)
            if len(paths_starting_at_i_through) > 0:
                for atom_j in paths_starting_at_i_through:
                    atom_j_bonded_to = np.nonzero(adj_mat[atom_j])[0]
                    atoms_jl_connections_through = set(atom_j_bonded_to) & set(atom_l_bonded_to)
                    atoms_jl_connections_through -= {atom_l}
                    atoms_jl_connections_through -= {atom_i}
                    for atom_k in atoms_jl_connections_through:
                        torsions.append([atom_i,atom_j,atom_k,atom_l])
            if len(paths_starting_at_l_through) > 0:
                for atom_k in paths_starting_at_l_through:
                    atom_k_bonded_to = np.nonzero(adj_mat[atom_k])[0]
                    atoms_ik_connections_through = set(atom_i_bonded_to) & set(atom_k_bonded_to)
                    atoms_ik_connections_through -= {atom_i}
                    atoms_ik_connections_through -= {atom_l}
                    for atom_j in atoms_ik_connections_through:
                        torsions.append([atom_i,atom_j,atom_k,atom_l])
    return torsions


adj_mat = adjacency_matrix(connectivity)
# print(adj_t)
# adj_mat = np.nonzero(adj_mat)
angles,adj_mat_sq = angles(adj_mat,return_adj_mat_sq=True)
# print(adj_ma
torsions = torsions(adj_mat,adj_mat_sq)
for i in torsions:
    print(i)
print(len(torsions))
# print(np.nonzero(adj_mat))
# for i,j in zip(adj_mat[0],adj_mat[1]):
#     print(i,j)
# print(np.dot(adj_mat,adj_mat))







#
# def torsions(conn):
#     torsion = []
#     for i in range(len(conn)):
#         a = conn[i][1]
#         for j in range(len(conn)):
#             if conn[j][0] == a:
#                 b = conn[j][1]
#                 for k in range(len(conn)):
#                     if (conn[k][0] == a) or (conn[k][1] == a):
#                         pass
#                     elif conn[k][0] == b:
#                         c = conn[k][1]
#                         for l in range(len(conn)):
#                             if (conn[l][0] == (a or b)):
#                                 pass
#                             elif (conn[l][1] == (a or b)):
#                                 pass
#                             elif conn[l][0] == c:
#                                 d = conn[l][1]
#                                 abcd = [a, b, c, d]
#                                 dcba = [d, c, b, a]
#                                 if len(abcd) == len(set(abcd)):
#                                     if dcba not in torsion:
#                                         torsion.append(abcd)
#                             elif conn[l][1] == c:
#                                 d = conn[l][0]
#                                 abcd = [a, b, c, d]
#                                 dcba = [d, c, b, a]
#                                 if len(abcd) == len(set(abcd)):
#                                     if dcba not in torsion:
#                                         torsion.append(abcd)
#                     elif conn[k][1] == b:
#                         c = conn[k][0]
#                         for l in range(len(conn)):
#                             if (conn[l][0] == (a or b)):
#                                 pass
#                             elif (conn[l][1] == (a or b)):
#                                 pass
#                             elif conn[l][0] == c:
#                                 d = conn[l][1]
#                                 abcd = [a, b, c, d]
#                                 dcba = [d, c, b, a]
#                                 if len(abcd) == len(set(abcd)):
#                                     if dcba not in torsion:
#                                         torsion.append(abcd)
#                             elif conn[l][1] == c:
#                                 d = conn[l][0]
#                                 abcd = [a, b, c, d]
#                                 dcba = [d, c, b, a]
#                                 if len(abcd) == len(set(abcd)):
#                                     if dcba not in torsion:
#                                         torsion.append(abcd)
#             elif conn[j][1] == a:
#                 b = conn[j][0]
#                 for k in range(len(conn)):
#                     if (conn[k][0] == a) or (conn[k][1] == a):
#                         pass
#                     elif conn[k][0] == b:
#                         c = conn[k][1]
#                         for l in range(len(conn)):
#                             if (conn[l][0] == (a or b)):
#                                 pass
#                             elif (conn[l][1] == (a or b)):
#                                 pass
#                             elif conn[l][0] == c:
#                                 d = conn[l][1]
#                                 abcd = [a, b, c, d]
#                                 dcba = [d, c, b, a]
#                                 if len(abcd) == len(set(abcd)):
#                                     if dcba not in torsion:
#                                         torsion.append(abcd)
#                             elif conn[l][1] == c:
#                                 d = conn[l][0]
#                                 abcd = [a, b, c, d]
#                                 dcba = [d, c, b, a]
#                                 if len(abcd) == len(set(abcd)):
#                                     if dcba not in torsion:
#                                         torsion.append(abcd)
#                     elif conn[k][1] == b:
#                         c = conn[k][0]
#                         for l in range(len(conn)):
#                             if (conn[l][0] == (a or b)):
#                                 pass
#                             elif (conn[l][1] == (a or b)):
#                                 pass
#                             elif conn[l][0] == c:
#                                 d = conn[l][1]
#                                 abcd = [a, b, c, d]
#                                 dcba = [d, c, b, a]
#                                 if len(abcd) == len(set(abcd)):
#                                     if dcba not in torsion:
#                                         torsion.append(abcd)
#                             elif conn[l][1] == c:
#                                 d = conn[l][0]
#                                 abcd = [a, b, c, d]
#                                 dcba = [d, c, b, a]
#                                 if len(abcd) == len(set(abcd)):
#                                     if dcba not in torsion:
#                                         torsion.append(abcd)
#
#     return duplicate(torsion)
#
#
# def duplicate(k):
#     newtor = []
#     for i in k:
#         if i not in newtor:
#             newtor.append(i)
#     return newtor


# tors = torsions(connectivity)
# print(tors)
# print(len(tors))
