#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 14:32:31 2021

@author: matt
"""
from sympy import symbols, Eq, solve
import itertools


def input_float(texte):
    y = 0.
    while True :
        try :
            y = float(input(texte))
            break
        except ValueError :
            print("Mauvaise saisie, entrez un nombre")
    return y


def definition_du_pbm():
    List = []
    taille =int( input("Combien de personnes participent au trajet ? (tapez le nombre puis Entrée) -> "))
    prixkm = input_float("Quel est le prix par km parcouru ? (ex. : 1.556) -> ")
    print("--------------------------------")
    print("Spécifiez maintenant les voyageurs, leur destination et leur distance au départ.")
    print("--------------------------------")
    n = 1
    while len(List)< taille:
        Nom = input("Comment se nomme le voyageur n°" + str(n) +" ? -> ")
        Ville = input("Dans quelle ville se rend t'il ? -> ")
        Distance = input_float("Quelle est sa distance au départ ? -> ")
        List.append((Nom,Ville,prixkm*Distance))
        n +=1
    List = sorted(List, key=lambda x: x[2])
    Dist = [ x[2] for x in List ]
    return taille,prixkm,List,Dist


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


def print_cout_si_seul(List):
    s = "La liste des coûts si seuls :"
    for x in List :
        s = s+ "\n\t"+ x[0] + " irait a "+x[1]+" pour "+ str(x[2])
    print(s)


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

            
def evaluation_de_prop(List,maxi):
    X = input("Ajouter une allocation pour l'evaluer ? (Oui/N) ")
    while (X.upper() == 'OUI') :
        prop = []
        for pers in (List):
            xx = input_float("Choix de coût pour "+ pers[0]+" -> ")
            prop.append(xx)
        print("Allocation : ",prop)
        if sum(prop) != maxi:
            print("La somme de cette allocation est différente du coût total.")
        print("---Voici les mecontents pour le stand alone test : ")
        print(stand_alone_cost(List,prop))
        print("---Voici les binomes mécontents pour le test noyau (vide si allocation noyau): ")
        mct2,css2 = is_noyau(List, prop,2)
        print(mct2,"\nAvec les couts si seuls par binome",css2,"\n")
        if len(List) >2 :
            print("---Voici les trinomes mécontents pour le test noyau (vide si allocation noyau): ")
            mct3,css3 = is_noyau(List, prop,3)
            print(mct3,"\nAvec les couts si seuls par trinome",css3,"\n")
        X = input("Proposer une allocation de nouveau ? (Oui/N) ")


def stand_alone_cost(List,prop):
    mecontents = []
    for i in range(len(List)):
        if List[i][2] <= prop[i]:
            mecontents.append(List[i][0])
    return mecontents


def resolution_du_pbm(taille,prixkm,List,Dist):
    print("--------------------------------")
    maxi = max(Dist)
    print("le cout total est de : ", maxi)
    print_cout_si_seul(List)
    print("--------------------------------")
    print("Méthodes par Proportionnalité :")
    prop = proportionnel(Dist)
    for i in range(taille):
        print("\tLe trajet de " +List[i][0] + " lui revient à " + str(round(float(prop[i]),2)) + " pour aller jusqu'à " + List[i][1] )
    print("--------------------------------")
    print("Méthodes par Séparabilité :")
    sep = separation(Dist)
    for i in range(taille):
        print("\tLe trajet de "+List[i][0] + " lui revient à " + str(round(sep[i],2)) + " pour aller jusqu'à " + List[i][1] )
    print("--------------------------------")
    evaluation_de_prop(List,maxi)


#taille,prixkm,List,Dist = definition_du_pbm()
#resolution_du_pbm(taille,prixkm,List,Dist)





