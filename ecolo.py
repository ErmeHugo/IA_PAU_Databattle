from math import *
import numpy as np
from enum import Enum
from read_sql import * 

taux_de_change = {
    'EUR': 1.0,
    'USD': 0.917,
    'AUD': 0.63,
    'CAD': 0.68,
    'GBP': 1.16,
    'INR': 0.012,
    'SEK': 0.087,
    'FRF': 0.15,
    'JPY': 0.0061,
    'CHF': 0.98,
    'MYR': 0.19,
    'BRL': 0.18,
    'LACS':0.015,
    'DZD': 0.0068,
    'KRW': 0.00069,
    # Ajoutez d'autres devises avec leur taux de change ici...
}

class Monnaie(Enum):
    EUR = 2
    USD = 3
    AUD = 4
    CAD = 5
    GBP = 6
    INR = 7
    SEK = 8
    FRF = 9
    JPY = 10
    CHF = 11
    MYR = 12
    BRL = 13
    LACS= 14
    DZD = 15
    KRW = 16

class UniteEnergieConvertible(Enum):
    GJ = 2    
    GWh = 3    
    kWh = 5   
    MMBtu = 11 
    MWh = 12  
    tep = 14  
    gallon = 21 
    therms = 23 
      
class UniteEnergieNonConvertible(Enum):
    NONE = 1
    litre = 7
    m3 = 9
    tonnes = 15
    kW = 16   
    pounds = 22
    pourcentage = 34 
    kWh_par_m2 = 41
    kVA = 30 

class CodePeriodeEnergie(Enum):
    NONE = 1    # Aucune période spécifiée
    AN0  = 3    # Par année
    JOUR = 4    # Par jour

class GainFinancierPeriodeRex(Enum):
    NONE = 1
    _    = 2    # Aucune période spécifiée
    AN   = 3    # Par année

def obtenir_monnaie_par_chiffre(chiffre):
    for monnaie in Monnaie:
        if monnaie.value == chiffre:
            return monnaie
    return None  # Retourner None si aucune monnaie correspondante n'est trouvée

def obtenir_unite_energie_par_chiffre(chiffre):
    for unite in list(UniteEnergieConvertible) + list(UniteEnergieNonConvertible):
        if unite.value == chiffre:
            return unite
    return None  # Retourner None si aucune unite correspondante n'est trouvée


def moy_argent_C02_energie(L):
    M=[]
    chiffre = L[2]
    monnaie = obtenir_monnaie_par_chiffre(chiffre)
    if monnaie and chiffre != 2 and L[1]!= None:  # Vérifier si la monnaie existe et n'est pas EUR
        L[1] = L[1] * taux_de_change.get(monnaie.name, 1.0)
    if L[6] == CodePeriodeEnergie.JOUR.value:
        # Si oui, multiplier la valeur de l'énergie par 365
        L[4] = L[4]*365
    chiffre_unite_energie = L[5]
    unite_energie = obtenir_unite_energie_par_chiffre(chiffre_unite_energie)
    if unite_energie in UniteEnergieConvertible:
        # Conversion en kWh
        if unite_energie == UniteEnergieConvertible.GJ:
            L[4] = L[4] * 277.778  # Conversion de gigajoules (GJ) en kWh
        elif unite_energie == UniteEnergieConvertible.GWh:
            L[4] = L[4] * 1000000  # Conversion de gigawattheures (GWh) en kWh
        elif unite_energie == UniteEnergieConvertible.MMBtu:
            L[4] = L[4] * 293.071  # Conversion de millions de British thermal units (MMBtu) en kWh
        elif unite_energie == UniteEnergieConvertible.MWh:
             L[4] = L[4] * 1000
        elif unite_energie == UniteEnergieConvertible.tep:
             L[4] = L[4] * 11630 
        elif unite_energie == UniteEnergieConvertible.gallon:
             L[4] = L[4] * 33.41
        elif unite_energie == UniteEnergieConvertible.therms:
             L[4] = L[4] * 29,3
    if unite_energie in UniteEnergieNonConvertible:
        L[4] = None
    

    # Vérifier si la période du gain financier est NONE
    if not L[3] or L[3] == GainFinancierPeriodeRex.NONE.value or L[3]==GainFinancierPeriodeRex._.value:
    # Si L[5] est vide ou égal à NONE, attribuer None à la valeur du gain financier
        L[1] = None
    M.append(L[1])
    M.append(L[4])
    M.append(L[7])
    return(M)
    
M = []
for i in range(len(codeEtudesBilans)):
    MM = []
    for j in range(len(codeEtudesBilans[i])):
        MM.append(moy_argent_C02_energie(codeEtudesBilans[i][j]))
    M.append(MM)
print(M)



############################### Calcul de moyenne / mediane #################################

import statistics

def supprimer_aberrations_iqr(liste):
    # Calculer le premier et le troisième quartile
    Q1 = np.percentile(liste, 25)
    Q3 = np.percentile(liste, 75)
    # Calculer l'IQR (Interquartile Range)
    IQR = Q3 - Q1
    # Calculer les limites supérieure et inférieure pour détecter les valeurs aberrantes
    limite_inf = Q1 - 1.5 * IQR
    limite_sup = Q3 + 1.5 * IQR
    # Filtrer les valeurs aberrantes
    valeurs_filtrees = [x for x in liste if (x >= limite_inf) and (x <= limite_sup)]
    for x in liste: 
        if (x <= limite_inf) or (x >= limite_sup):
            print("Voici des valeurs filtrées : ", x)
    return valeurs_filtrees

def moy(valeurs_filtrees):
    return(statistics.mean(valeurs_filtrees))
    

def final_eco(A):
    Final = []
    for i in range(len(A)):
        Argent = []
        Energie = []
        co2 = []
        FinalI = []
        for k in range(len(A[i])):  # Correction de la boucle range
            if A[i][k][0]!=None:
                Argent.append(A[i][k][0])
            if A[i][k][1]!=None:   
                Energie.append(A[i][k][1])  # Correction de l'indexing de la liste Energie
            if A[i][k][2]!=None:
                co2.append(A[i][k][2])
        if Argent != []:
            Argent=supprimer_aberrations_iqr(Argent)
            FinalI.append(statistics.mean(Argent))
        else :
            FinalI.append(None)
        if Energie != []:
            Energie=supprimer_aberrations_iqr(Energie)
            FinalI.append(statistics.mean(Energie))
        else :
            FinalI.append(None)
        if co2 != []:
            co2=supprimer_aberrations_iqr(co2)
            print(co2)
            FinalI.append(statistics.mean(co2))
        else :
            FinalI.append(None)
        Final.append(FinalI)
    return(Final)

print("Voici les bilans finaux : ",final_eco(M))

    



 

    


    
