import pandas as pd
import csv
import xlsxwriter

def Risultati(instance, Optimization_Goal):

    EE = instance.EnergiaAnnua.value  # [MWh]

    x = instance.INV_COST.value
    y = instance.cf.value

    print('\n Energia Annua:', round(EE, 5), "[MWh]", '\n Net Present Value:', round(-x+y, 5), '[€]')

    bbb = instance.Binary_A.get_values()
    print('\nBinaria che chiude i tratti:', bbb)

    Pta = instance.Portata_Turbina_A.get_values()
    print('\nPortata Turbina A finale:', Pta)

    okko = instance.Binary_Day_A.get_values()
    print('\nBinaria che chiude la portata nel giorno:', okko)
    daadsa = instance.Binary_Buy_A.get_values()
    print('\nBinaria che chiude la turbina(non compra):', daadsa)

    jaja = instance.Coeff_lin.extract_values()
    #print('\nCoefficienti: vediamo se sono giusti:',jaja)

    from F1_more import estremi_p, estremi_eta, serie_Portate, serie_Efficiency
    import pandas as pd
    import numpy.polynomial.polynomial as poly
    import numpy as np
    import matplotlib.pyplot as plt

    x1 = np.linspace(estremi_p[0], estremi_p[1], 100)
    fit1 = poly.polyval(x1, [jaja[1, 1],jaja[1, 2]]) 

    x2 = np.linspace(estremi_p[1], estremi_p[2], 100)
    fit2 = poly.polyval(x2, [jaja[2, 1], jaja[2, 2]])

    x3 = np.linspace(estremi_p[2], estremi_p[3], 100)
    fit3 = poly.polyval(x3, [jaja[3,1],jaja[3,2]])

    x4 = np.linspace(estremi_p[3], estremi_p[4], 100)
    fit4 = poly.polyval(x4, [jaja[4,1],jaja[4,2]])

    x5 = np.linspace(estremi_p[4], estremi_p[5], 100)
    fit5 = poly.polyval(x5, [jaja[5,1],jaja[5,2]])

    x6 = np.linspace(estremi_p[5], estremi_p[6], 100)
    fit6 = poly.polyval(x6, [jaja[6,1],jaja[6,2]])

    x7 = np.linspace(estremi_p[6], estremi_p[7], 100)
    fit7 = poly.polyval(x7, [jaja[7,1],jaja[7,2]])

    x8 = np.linspace(estremi_p[7], estremi_p[8], 100)
    fit8 = poly.polyval(x8, [jaja[8,1],jaja[8,2]])

    x9 = np.linspace(estremi_p[8], estremi_p[9], 100)
    fit9 = poly.polyval(x9, [jaja[9,1],jaja[9,2]])

    plt.plot(serie_Portate, serie_Efficiency, 'ro', x1, fit1, 'b', x2, fit2, x3, fit3, x4, fit4, x5, fit5, x6, fit6, x7,
             fit7,
             x8, fit8, x9, fit9)
    plt.show()

    return
