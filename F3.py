import numpy.polynomial.polynomial as poly

def vmeno2(model, i, n):
    return model.Double_Binary[i, n] == model.Binary_Buy_A[n] * model.Binary_Day_A[i, n]
def vmeno1(model, i, n):
    return model.Portata_scelta_dai_tratti[i, n] == sum(model.Binary_A[i, n, f] * model.Portata_A_dip[i, n, f] for f in model.tratti)

def v0(model, i, n):
    return model.Portata_Turbina_A[i, n] == model.Double_Binary[i, n] * model.Portata_scelta_dai_tratti[i, n]

#def v0(model, i, n):
#   return model.Portata_Turbina_A[i, n] == model.Binary_Buy_A[n] * model.Binary_Day_A[i, n] * sum(model.Binary_A[i, n, f] * model.Portata_A_dip[i, n, f] for f in model.tratti)

def v1(model, i, n):
    return sum(model.Binary_A[i, n, f] for f in model.tratti) == 1

def v2(model, i):
    return model.Somma_portate[i] == sum(model.Portata_Turbina_A[i, n] for n in model.nmax)

def v3(model, i):
    return model.Somma_portate[i] <= model.Duration_Curve[i]

def v4(model, i, n):
    return model.Hnet_A[i, n] == model.Hgross[i] - model.Coeff * (model.Portata_Turbina_A[i, n]**2)

def v5(model, i, n, f):
    return model.Etas[i, n, f] == poly.polyval(model.Portata_A_dip[i, n, f], [model.Coeff_lin[f, 1], model.Coeff_lin[f, 2]])#1 rendimento per ogni tratto, per ogni turbina, per ogni giorno

def v6(model, i, n):
    return model.Betas[i, n] == sum(model.Binary_A[i, n, f] * model.Etas[i, n, f] for f in model.tratti)#ne esce 1 rendimento per turbina per giorno

def vv71(model, i, n):
    return model.QtEta[i, n] == model.Betas[i, n] * model.Portata_Turbina_A[i, n]

def v7(model, i):
    return model.Potenza_giorn_A[i] == (10**3) * 9.81 * sum(model.QtEta[i, n] * model.Hnet_A[i, n] for n in model.nmax)

def v8(model):
    return model.EnergiaAnnua == sum(model.Potenza_giorn_A[i] for i in model.giorni)*24*model.Eta_aux*1e-6#[MWh]

def v9(model):
    return model.Costo_Turbine_Variabile == sum(model.Binary_Buy_A[n] * model.Cost_turb for n in model.nmax)

def v10(model):
    return model.INV_COST == model.Inv_Cost + model.Costo_Turbine_Variabile

def V_foo1(model):
    return model.Revenues == model.EnergiaAnnua * model.Revenues_Specific#[€/MWh]
def V_foo2(model):
    return model.Costs_forTax == model.INV_COST * (model.Perc_OeM + (1 / model.Ammortization))
def V_foo3(model):
    return model.Costs_forCF == model.INV_COST * model.Perc_OeM
def V_foo4(model):
    return model.Taxes_first == (model.Revenues - model.Costs_forTax) * model.Taxes
def V_foo5(model):
    return model.Taxes_second == (model.Revenues - model.Costs_forCF) * model.Taxes
def V_foo6(model):
    return model.CF_first == model.Revenues - model.Costs_forCF - model.Taxes_first
def V_foo7(model):
    return model.CF_second == model.Revenues - model.Costs_forCF - model.Taxes_second

def V_forNPV(model):
    return model.cf == model.Act_1 * model.CF_first + model.Act_2 * model.CF_second
def Net_Present_Value(model): #objective!!
    return - model.INV_COST + model.cf
