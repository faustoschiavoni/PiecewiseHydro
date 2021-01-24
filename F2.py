from pyomo.environ import Param, RangeSet, NonNegativeReals, NonNegativeIntegers, Var, Set, PositiveIntegers, Reals, Binary
from pyomo.core import *
from F1 import Initialize_Duration_Curve, Initialize_Hgross, Initialize_Act
from F1_more import _New_bounds_rule, _New_coef_tot, Buy_binary, Day_binary, Num_intervalli, grado_poly

def Model_Creation(model, Optimization_Goal):
    #Param. per Sets
    model.Giorni = Param(within=NonNegativeReals)
    model.Nmax = Param(within=NonNegativeIntegers)
    #Sets
    model.giorni = RangeSet(model.Giorni)
    model.nmax = RangeSet(model.Nmax)

    #Parametri singoli
    model.DMV = Param(within=NonNegativeReals)
    model.Eta_aux = Param(within=NonNegativeReals)
    model.Revenues_Specific = Param(within=NonNegativeReals)
    model.Perc_OeM = Param(within=NonNegativeReals)
    model.Inv_Cost = Param(within=NonNegativeReals)
    model.Ammortization = Param(within=NonNegativeReals)
    model.Taxes = Param(within=NonNegativeReals)
    model.Discount_Rate = Param(within=NonNegativeReals)
    model.Lifetime = Param(within=NonNegativeIntegers)
    model.Coeff = Param(within=NonNegativeReals)

    #Param. multi-ingresso indicizzati sul numero di turbine diversi prevsisto (2: A e B)
    model.Portata_Nom = Param(within=NonNegativeReals)
    model.Cost_turb = Param(within=NonNegativeReals)

    #Param. inizializzati da me da excel (da dare come input)
    model.Duration_Curve = Param(model.giorni, within=NonNegativeReals, initialize=Initialize_Duration_Curve)#già tolto il DMV
    model.Hgross = Param(model.giorni, within=NonNegativeReals, initialize=Initialize_Hgross)


    #Inizio SPEZZATA_bounds

    model.Hnet_A = Var(model.giorni, model.nmax, within=NonNegativeReals)
    model.EnergiaAnnua = Var()
    model.Costo_Turbine_Variabile = Var()
    model.cf = Var(within=Reals)
    model.INV_COST = Var(within=NonNegativeReals)

    #Var per NPV
    model.Revenues = Var(within=NonNegativeReals)
    model.Costs_forTax = Var(within=NonNegativeReals)
    model.Costs_forCF = Var(within=NonNegativeReals)
    model.Taxes_first = Var()
    model.Taxes_second = Var()
    model.CF_first = Var()
    model.CF_second = Var()

    Act_1, Act_2 = Initialize_Act()

    model.Act_1 = Param(initialize=Act_1)
    model.Act_2 = Param(initialize=Act_2)

    #Var per modellare portate
    #Set per numero tratti/intervalli della spezzata
    model.Tratti = Param(initialize=Num_intervalli)
    model.tratti = RangeSet(model.Tratti)
    #Var Binarie
    model.Binary_Buy_A = Var(model.nmax, within=Binary)#, initialize=Buy_binary)
    model.Binary_Day_A = Var(model.giorni, model.nmax, within=Binary, initialize=Day_binary)
    model.Binary_A = Var(model.giorni, model.nmax, model.tratti, within=Binary)

    #Var normali
    model.Portata_A_dip = Var(model.giorni, model.nmax, model.tratti, bounds=_New_bounds_rule)

    model.Portata_Turbina_A = Var(model.giorni, model.nmax, within=NonNegativeReals, initialize=2.8)
    model.Somma_portate = Var(model.giorni, within=NonNegativeReals, initialize=2.8)
    model.Potenza_giorn_A = Var(model.giorni, within=NonNegativeReals)#, bounds=(0, 2*1e6))

    model.Etas = Var(model.giorni, model.nmax, model.tratti, bounds=(0, 1))

    model.Coeff_lin = Param(model.tratti, range(1, grado_poly + 2), initialize=_New_coef_tot)#initialize=coef_tot)

    model.Betas = Var(model.giorni, model.nmax, initialize=0.8, bounds=(0, 1))

    model.QtEta = Var(model.giorni, model.nmax)#, bounds=(0, 3))

    model.Portata_scelta_dai_tratti = Var(model.giorni, model.nmax)#, bounds=(0, 3))
    model.Double_Binary = Var(model.giorni, model.nmax)#, bounds=(0, 1))
