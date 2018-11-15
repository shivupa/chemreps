'''
Function for reading common molecule files and creating bags of bonds/pairwise
interactions, angles, and torsions to be used in creating a bond, angle,
torsion style of representation representation.
'''

import copy
import glob
from math import sqrt
import numpy as np
from itertools import chain
from .utils.molecule import Molecule
from .utils.bag_handler import bag_updater
from .utils.bag_handler import bag_organizer
from .utils.calcs import length
from .utils.calcs import angle
from .utils.calcs import torsion


def bag_maker(dataset):
    '''
    Parameters
    ---------
    dataset: path
        path to all molecules in the dataset

    Returns
    -------
    bags: dict
        dict of all bags for the dataset
    bag_sizes: dict
        dict of size of the largest bags in the dataset
    '''
    # iterate through all of the molecules in the dataset
    #   and get the sizes of the largest bags
    bond_sizes = {}
    angle_sizes = {}
    torsion_sizes = {}
    for mol_file in glob.iglob("{}/*".format(dataset)):
        current_molecule = Molecule(mol_file)
        if current_molecule.ftype != 'sdf':
            raise NotImplementedError(
                'file type \'{}\'  is unsupported. Accepted formats: sdf.'.format(current_molecule.ftype))
        # build bags
        bond_bag = {}
        angle_bag = {}
        torsion_bag = {}

        # grab bonds/nonbonds
        for i in range(current_molecule.n_atom):
            for j in range(i, current_molecule.n_atom):
                atomi = current_molecule.sym[i]
                atomj = current_molecule.sym[j]
                zi = current_molecule.at_num[i]
                zj = current_molecule.at_num[j]
                if i == j:
                    pass
                else:
                    if zj > zi:
                        atomi, atomj = atomj, atomi
                    bond = "{}{}".format(atomi, atomj)
                    if bond in bond_bag:
                        bond_bag[bond] += 1
                    else:
                        bond_bag[bond] = 1

        # update bag_sizes with larger value
        bag_updater(bond_bag, bond_sizes)

        # grab angles
        angles = []
        angcon = []
        for i in range(current_molecule.n_connect):
            connect = []
            for j in range(current_molecule.n_connect):
                if i in current_molecule.connect[j]:
                    if i == current_molecule.connect[j][0]:
                        connect.append(int(current_molecule.connect[j][1]))
                    elif i == current_molecule.connect[j][1]:
                        connect.append(int(current_molecule.connect[j][0]))
            if len(connect) > 1:
                for k in range(len(connect)):
                    for l in range(k + 1, len(connect)):
                        a = current_molecule.sym[connect[k] - 1]
                        b = current_molecule.sym[i - 1]
                        c = current_molecule.sym[connect[l] - 1]
                        if c < a:
                            # swap for lexographic order
                            a, c = c, a
                        angle = a + b + c
                        angles.append(angle)
                        angcon.append([connect[k], i, connect[l]])
        for i in range(len(angles)):
            if angles[i] in angle_bag:
                angle_bag[angles[i]] += 1
            else:
                angle_bag[angles[i]] = 1

        # update bag_sizes with larger value
        bag_updater(angle_bag, angle_sizes)

        # grab torsions
        torcon = []
        for i in range(current_molecule.n_connect):
            a = int(current_molecule.connect[i][1])
            for j in range(current_molecule.n_connect):
                if int(current_molecule.connect[j][0] == a):
                    b = int(current_molecule.connect[j][1])
                    for k in range(current_molecule.n_connect):
                        if (int(current_molecule.connect[k][0]) == a) or (int(current_molecule.connect[k][1]) == a):
                            pass
                        elif int(current_molecule.connect[k][0] == b):
                            c = int(current_molecule.connect[k][1])
                            for l in range(current_molecule.n_connect):
                                if (int(current_molecule.connect[l][0]) == (a or b)):
                                    pass
                                elif (int(current_molecule.connect[l][1]) == (a or b)):
                                    pass
                                elif int(current_molecule.connect[l][0]) == c:
                                    d = int(current_molecule.connect[l][1])
                                    abcd = [a, b, c, d]
                                    dcba = [d, c, b, a]
                                    if len(abcd) == len(set(abcd)):
                                        if dcba not in torcon:
                                            torcon.append(abcd)
                                elif int(current_molecule.connect[l][1]) == c:
                                    d = int(current_molecule.connect[l][0])
                                    abcd = [a, b, c, d]
                                    dcba = [d, c, b, a]
                                    if len(abcd) == len(set(abcd)):
                                        if dcba not in torcon:
                                            torcon.append(abcd)
                        elif int(current_molecule.connect[k][1] == b):
                            c = int(current_molecule.connect[k][0])
                            for l in range(current_molecule.n_connect):
                                if (int(current_molecule.connect[l][0]) == (a or b)):
                                    pass
                                elif (int(current_molecule.connect[l][1]) == (a or b)):
                                    pass
                                elif int(current_molecule.connect[l][0]) == c:
                                    d = int(current_molecule.connect[l][1])
                                    abcd = [a, b, c, d]
                                    dcba = [d, c, b, a]
                                    if len(abcd) == len(set(abcd)):
                                        if dcba not in torcon:
                                            torcon.append(abcd)
                                elif int(current_molecule.connect[l][1]) == c:
                                    d = int(current_molecule.connect[l][0])
                                    abcd = [a, b, c, d]
                                    dcba = [d, c, b, a]
                                    if len(abcd) == len(set(abcd)):
                                        if dcba not in torcon:
                                            torcon.append(abcd)
                elif int(current_molecule.connect[j][1]) == a:
                    b = int(current_molecule.connect[j][0])
                    for k in range(current_molecule.n_connect):
                        if (int(current_molecule.connect[k][0]) == a) or (int(current_molecule.connect[k][1]) == a):
                            pass
                        elif int(current_molecule.connect[k][0] == b):
                            c = int(current_molecule.connect[k][1])
                            for l in range(current_molecule.n_connect):
                                if (int(current_molecule.connect[l][0]) == (a or b)):
                                    pass
                                elif (int(current_molecule.connect[l][1]) == (a or b)):
                                    pass
                                elif int(current_molecule.connect[l][0]) == c:
                                    d = int(current_molecule.connect[l][1])
                                    abcd = [a, b, c, d]
                                    dcba = [d, c, b, a]
                                    if len(abcd) == len(set(abcd)):
                                        if dcba not in torcon:
                                            torcon.append(abcd)
                                elif int(current_molecule.connect[l][1]) == c:
                                    d = int(current_molecule.connect[l][0])
                                    abcd = [a, b, c, d]
                                    dcba = [d, c, b, a]
                                    if len(abcd) == len(set(abcd)):
                                        if dcba not in torcon:
                                            torcon.append(abcd)
                        elif int(current_molecule.connect[k][1] == b):
                            c = int(current_molecule.connect[k][0])
                            for l in range(current_molecule.n_connect):
                                if (int(current_molecule.connect[l][0]) == (a or b)):
                                    pass
                                elif (int(current_molecule.connect[l][1]) == (a or b)):
                                    pass
                                elif int(current_molecule.connect[l][0]) == c:
                                    d = int(current_molecule.connect[l][1])
                                    abcd = [a, b, c, d]
                                    dcba = [d, c, b, a]
                                    if len(abcd) == len(set(abcd)):
                                        if dcba not in torcon:
                                            torcon.append(abcd)
                                elif int(current_molecule.connect[l][1]) == c:
                                    d = int(current_molecule.connect[l][0])
                                    abcd = [a, b, c, d]
                                    dcba = [d, c, b, a]
                                    if len(abcd) == len(set(abcd)):
                                        if dcba not in torcon:
                                            torcon.append(abcd)

        tors = []
        for i in torcon:
            if i not in tors:
                tors.append(i)
        torsions = []
        for i in range(len(tors)):
            a = current_molecule.sym[tors[i][0] - 1]
            b = current_molecule.sym[tors[i][1] - 1]
            c = current_molecule.sym[tors[i][2] - 1]
            d = current_molecule.sym[tors[i][3] - 1]
            if d < a:
                # swap for lexographic order
                a, b, c, d = d, c, b, a
            abcd = a + b + c + d
            torsions.append(abcd)
        for i in range(len(torsions)):
            if torsions[i] in torsion_bag:
                torsion_bag[torsions[i]] += 1
            else:
                torsion_bag[torsions[i]] = 1

        # update bag_sizes with larger value
        bag_updater(torsion_bag, torsion_sizes)

    bag_sizes = bond_sizes.copy()
    bag_sizes.update(angle_sizes)
    bag_sizes.update(torsion_sizes)

    # make empty bags to fill
    bags = {}
    bag_keys = list(bag_sizes.keys())
    for i in range(len(bag_keys)):
        bags.update({bag_keys[i]: []})

    return bags, bag_sizes


def bat(mol_file, bags, bag_sizes):
    '''
    Paramters
    ---------
    mol_file: file
        molecule file for reading in coordinates
    bags: dict
        dict of all bags for the dataset
    bag_sizes: dict
        dict of size of the largest bags in the dataset

    Returns
    -------
    bat: vector
        vector of all bonds, angles, torsions in the molecule
    '''
    # copy bags dict to ensure it does not get edited
    bag_set = copy.deepcopy(bags)
    current_molecule = Molecule(mol_file)
    if current_molecule.ftype != 'sdf':
        raise NotImplementedError(
            'file type \'{}\'  is unsupported. Accepted formats: sdf.'.format(current_molecule.ftype))
    # grab bonds/nonbonds
    for i in range(current_molecule.n_atom):
        for j in range(i, current_molecule.n_atom):
            atomi = current_molecule.sym[i]
            atomj = current_molecule.sym[j]
            zi = current_molecule.at_num[i]
            zj = current_molecule.at_num[j]

            if i == j:
                pass # This might need to be filled in to best represent BAML
            else:
                if zj > zi:
                        # swap ordering
                    atomi, atomj = atomj, atomi
                bond = "{}{}".format(atomi, atomj)
                rij = length(current_molecule, i, j)
                mij = (zi * zj) / rij
                bag_set[bond].append(mij)

    # grab angles
    for i in range(current_molecule.n_connect):
        connect = []
        for j in range(current_molecule.n_connect):
            if i in current_molecule.connect[j]:
                if i == current_molecule.connect[j][0]:
                    connect.append(int(current_molecule.connect[j][1]))
                elif i == current_molecule.connect[j][1]:
                    connect.append(int(current_molecule.connect[j][0]))
        if len(connect) > 1:
            for k in range(len(connect)):
                for l in range(k + 1, len(connect)):
                    k_c = connect[k] - 1
                    i_c = i - 1
                    l_c = connect[l] - 1
                    a = current_molecule.sym[k_c]
                    b = current_molecule.sym[i_c]
                    c = current_molecule.sym[l_c]
                    if c < a:
                        # swap for lexographic order
                        a, c = c, a
                    abc = a + b + c
                    theta = angle(current_molecule, k_c, i_c, l_c)
                    bag_set[abc].append(theta)

    # grab torsions
    # grab torsions
    torcon = []
    for i in range(current_molecule.n_connect):
        a = int(current_molecule.connect[i][1])
        for j in range(current_molecule.n_connect):
            if int(current_molecule.connect[j][0] == a):
                b = int(current_molecule.connect[j][1])
                for k in range(current_molecule.n_connect):
                    if (int(current_molecule.connect[k][0]) == a) or (int(current_molecule.connect[k][1]) == a):
                        pass
                    elif int(current_molecule.connect[k][0] == b):
                        c = int(current_molecule.connect[k][1])
                        for l in range(current_molecule.n_connect):
                            if (int(current_molecule.connect[l][0]) == (a or b)):
                                pass
                            elif (int(current_molecule.connect[l][1]) == (a or b)):
                                pass
                            elif int(current_molecule.connect[l][0]) == c:
                                d = int(current_molecule.connect[l][1])
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torcon:
                                        torcon.append(abcd)
                            elif int(current_molecule.connect[l][1]) == c:
                                d = int(current_molecule.connect[l][0])
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torcon:
                                        torcon.append(abcd)
                    elif int(current_molecule.connect[k][1] == b):
                        c = int(current_molecule.connect[k][0])
                        for l in range(current_molecule.n_connect):
                            if (int(current_molecule.connect[l][0]) == (a or b)):
                                pass
                            elif (int(current_molecule.connect[l][1]) == (a or b)):
                                pass
                            elif int(current_molecule.connect[l][0]) == c:
                                d = int(current_molecule.connect[l][1])
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torcon:
                                        torcon.append(abcd)
                            elif int(current_molecule.connect[l][1]) == c:
                                d = int(current_molecule.connect[l][0])
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torcon:
                                        torcon.append(abcd)
            elif int(current_molecule.connect[j][1]) == a:
                b = int(current_molecule.connect[j][0])
                for k in range(current_molecule.n_connect):
                    if (int(current_molecule.connect[k][0]) == a) or (int(current_molecule.connect[k][1]) == a):
                        pass
                    elif int(current_molecule.connect[k][0] == b):
                        c = int(current_molecule.connect[k][1])
                        for l in range(current_molecule.n_connect):
                            if (int(current_molecule.connect[l][0]) == (a or b)):
                                pass
                            elif (int(current_molecule.connect[l][1]) == (a or b)):
                                pass
                            elif int(current_molecule.connect[l][0]) == c:
                                d = int(current_molecule.connect[l][1])
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torcon:
                                        torcon.append(abcd)
                            elif int(current_molecule.connect[l][1]) == c:
                                d = int(current_molecule.connect[l][0])
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torcon:
                                        torcon.append(abcd)
                    elif int(current_molecule.connect[k][1] == b):
                        c = int(current_molecule.connect[k][0])
                        for l in range(current_molecule.n_connect):
                            if (int(current_molecule.connect[l][0]) == (a or b)):
                                pass
                            elif (int(current_molecule.connect[l][1]) == (a or b)):
                                pass
                            elif int(current_molecule.connect[l][0]) == c:
                                d = int(current_molecule.connect[l][1])
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torcon:
                                        torcon.append(abcd)
                            elif int(current_molecule.connect[l][1]) == c:
                                d = int(current_molecule.connect[l][0])
                                abcd = [a, b, c, d]
                                dcba = [d, c, b, a]
                                if len(abcd) == len(set(abcd)):
                                    if dcba not in torcon:
                                        torcon.append(abcd)

    tors = []
    for i in torcon:
        if i not in tors:
            tors.append(i)
    torsions = []
    for i in range(len(tors)):
        a = tors[i][0] - 1
        b = tors[i][1] - 1
        c = tors[i][2] - 1
        d = tors[i][3] - 1
        a_sym = current_molecule.sym[a]
        b_sym = current_molecule.sym[b]
        c_sym = current_molecule.sym[c]
        d_sym = current_molecule.sym[d]
        if d_sym < a_sym:
            # swap for lexographic order
            a_sym, b_sym, c_sym, d_sym = d_sym, c_sym, b_sym, a_sym
        abcd = a_sym + b_sym + c_sym + d_sym
        theta = torsion(current_molecule, a, b, c, d)
        bag_set[abcd].append(theta)


    # sort bags by magnitude, pad, concactenate
    bat = bag_organizer(bag_set, bag_sizes)

    # flatten bob into one list and store as a np.array
    bat = np.array(list(chain.from_iterable(bat)))

    return bat
