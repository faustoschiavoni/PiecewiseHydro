import pandas as pd
import re
import numpy.polynomial.polynomial as poly
from F1 import df3

Data_file = "Inputs/Data.dat"
Data_import = open(Data_file).readlines()
for i in range(len(Data_import)):
    if "param: Portata_Nom" in Data_import[i]:
        Pnom_A = float(re.findall('\d+\.\d+', Data_import[i])[0])
        #Pnom_A = float(re.findall('\d+\.\d+', Data_import[i + 1])[0]) #se ci fossero più valori dovrei prendere il "i + 1" (riga sotto)

serie_Efficiency = []
serie_Portate = []
for i in range(0, len(df3)):
    serie_Efficiency += [df3.loc[i][1] / 100]
    serie_Portate += [df3.loc[i][0] * Pnom_A]

Num_intervalli = 9
Num_punti = Num_intervalli + 1
grado_poly = 1

def _Sorting(list1, list2, length_newlist):
    somelist1 = list1
    somelist2 = list2

    a = min(somelist1)
    b = max(somelist1)

    chunk_size = (b-a)/(length_newlist-1)

    new_list1 = []
    new_list2 = []
    for t in range(length_newlist):
        index = a+t*chunk_size
        da_append1 = min(somelist1, key=lambda x: abs(x-index))
        new_list1.append(da_append1)
        da_append2 = somelist2[somelist1.index(da_append1)]
        new_list2.append(da_append2)
        if t != 0:
            while new_list1[t] == new_list1[t-1]:
                new_list1.pop(t)
                new_list2.pop(t)
                somelist1.remove(da_append1)
                da_append1 = min(somelist1, key=lambda x: abs(x-index))
                new_list1.append(da_append1)
                da_append2 = somelist2[somelist1.index(da_append1)]
                new_list2.append(da_append2)


    return new_list1, new_list2


def _Intervals():
    return _Sorting(serie_Portate, serie_Efficiency, Num_punti)

estremi_p, estremi_eta = _Intervals()


def _New_bounds_rule(model, i, n, p):
    return (estremi_p[p-1], estremi_p[p])


def _New_coef_tot(model, p, c):
    p -= 1
    est_p, est_eta = estremi_p[p:p + 2], estremi_eta[p:p + 2]

    coefs = poly.polyfit(est_p, est_eta, grado_poly)

    return coefs[c-1]

'''Funzioni per efficientare modello inizializzando dei parametri'''

def Buy_binary(model, n):
    a = [1, 1, 0]#cambiare dimensione lista al variare del numero di turbine (in questo caso è 3)
    return a[n-1]

def Day_binary(model, i, n):
    if 100 >= i >= 1:
        if 2 >= n >= 1:
            return 1
        else:
            return 0
    if 220 >= i >= 101:
        if 3 >= n >= 0:
            return 1
        else:
            return 0
    if 365 >= i >= 221:
        if 4 >= n >= 0:
            return 1
        else:
            return 0
