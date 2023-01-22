#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 14:32:31 2021

@author: Chaimae
"""

"""
Chaimae ERREBIAI - Matthieu AKHAVAN NIAKI
"""

from sympy import symbols, Eq, solve
import itertools

def proportionnel(CostList):
    n = len(CostList)
    varbs = symbols('x(:'+str(n)+')') #(x0, x1, x2, x3)
    eqs = [ (x/cout) for x,cout in zip(varbs,CostList) ]
    maxLC = max(CostList)
    listEq = []
    E = eqs[0]
    ssum = sum(varbs)
    for e in eqs[1:] :
        listEq.append(Eq(e,E))
        E=e
    listEq.append(Eq(ssum,maxLC))
    s=solve(listEq, varbs)
    sol = list(s.values())
    return sol

# List contains : Nom,Ville,prixkm*Distance
def print_cout_si_seul(List):
    s = "La liste des coûts si seuls :"
    for x in List :
        s = s+ "\n\t"+ x[0] + " irait a "+x[1]+" pour "+ str(x[2])
    return s

def separation(CostList):
    sol = []
    x = 0.
    y = 0.
    temp = 0.
    taille = len(CostList)
    for e in range(taille):
        y += x 
        x = CostList[e] - y
        temp += x / (taille - e)
        
        sol.append(temp )
    return sol


def is_noyau(List,prop,cb):
    mecontents = []
    couts_si_seuls = []
    f = list(itertools.combinations(range(len(List)), cb))
    for ff in f:
        L = 0
        p = 0
        for i in ff:
            L += List[i][2]
            p += prop[i]
        personnes = [ List[i][0] for i in ff ]
        
        couts_si_seuls.append((personnes,L))
        #print((personnes,L))
        if L <= p :
            mecontents.append(personnes)
    return mecontents,couts_si_seuls

def stand_alone_cost(List,prop):
    mecontents = []
    for i in range(len(List)):
        if List[i][2] <= prop[i]:
            mecontents.append(List[i][0])
    return mecontents


def resolution_du_pbm(taille,prixkm,List,Dist):
    # print("--------------------------------")
    # le cout total est maxi
    maxi = max(Dist)
    # print("le cout total est de : ", maxi)
    # les couts si seuls, to display s
    s = print_cout_si_seul(List)
    print("--------------------------------")
    s1 = "--------------------------------\nMéthodes par Proportionnalité :"
    #print("Méthodes par Proportionnalité :")
    prop = proportionnel(Dist)
    ll = []
    ll1 = []
    for i in range(taille):
        ph = "\t\nLe trajet de " +List[i][0] + " lui revient à " + str(round(float(prop[i]),2)) + " pour aller jusqu'à " + List[i][1] 
        ll.append(ph)
        # print("\tLe trajet de " +List[i][0] + " lui revient à " + str(round(float(prop[i]),2)) + " pour aller jusqu'à " + List[i][1] )
    s2 = "--------------------------------"
    # print("--------------------------------")
    s3 = "Méthodes par Séparabilité :"
    # print("Méthodes par Séparabilité :")
    sep = separation(Dist)
    for i in range(taille):
        ph1 = "\t\nLe trajet de "+List[i][0] + " lui revient à " + str(round(sep[i],2)) + " pour aller jusqu'à " + List[i][1]
        ll1.append(ph1)
        # print("\tLe trajet de "+List[i][0] + " lui revient à " + str(round(sep[i],2)) + " pour aller jusqu'à " + List[i][1] )
    # print("--------------------------------")
    #evaluation_de_prop(List,maxi)
    return maxi, s, s1, ll, ll1, s2, s3


#taille,prixkm,List,Dist = definition_du_pbm()
#resolution_du_pbm(taille,prixkm,List,Dist)





