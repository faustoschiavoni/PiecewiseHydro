from pyomo.opt import SolverFactory
from pyomo.core import *
from pyomo.environ import *
from F3 import *
import time


def Model_Resolution(model, Optimization_Goal, datapath="Inputs/Data.dat"):

    if Optimization_Goal == 'NPV':
            model.ObjectiveFunction = Objective(rule=Net_Present_Value, sense=maximize)

    model.vmeno1 = Constraint(model.giorni, model.nmax, rule=vmeno1)
    model.vmeno2 = Constraint(model.giorni, model.nmax, rule=vmeno2)

    model.v0 = Constraint(model.giorni, model.nmax, rule=v0)
    model.v1 = Constraint(model.giorni, model.nmax, rule=v1)
    model.v2 = Constraint(model.giorni, rule=v2)
    model.v3 = Constraint(model.giorni, rule=v3)
    model.v4 = Constraint(model.giorni, model.nmax, rule=v4)
    model.v5 = Constraint(model.giorni, model.nmax, model.tratti, rule=v5)
    model.v6 = Constraint(model.giorni, model.nmax, rule=v6)

    model.vv71 = Constraint(model.giorni, model.nmax, rule=vv71)

    model.v7 = Constraint(model.giorni, rule=v7)
    model.v8 = Constraint(rule=v8)
    model.v9 = Constraint(rule=v9)
    model.v10 = Constraint(rule=v10)

    model.V_foo1 = Constraint(rule=V_foo1)
    model.V_foo2 = Constraint(rule=V_foo2)
    model.V_foo3 = Constraint(rule=V_foo3)
    model.V_foo4 = Constraint(rule=V_foo4)
    model.V_foo5 = Constraint(rule=V_foo5)
    model.V_foo6 = Constraint(rule=V_foo6)
    model.V_foo7 = Constraint(rule=V_foo7)

    model.V_forNPV = Constraint(rule=V_forNPV)

    #Carico i valori veri da recuperare dal Data.dat
    instance = model.create_instance(datapath)
    print('\nInstance created')
    print('\n\nOrario creazione Istanza: ', time.strftime("%H:%M:%S"))
    opt = SolverFactory('gurobi')


    
    opt.set_options('Method=-1 MIPGap=0.1 Basis=0 ImproveTime=30 Mipfocus=1 BarHomogeneous=1 NonConvex=2 Crossover=0 BarConvTol=1e-3 OptimalityTol=1e-3 FeasibilityTol=1e-5 IterationLimit=1e17')

    print('Calling solver...')
    print('\n\nOrario partenza risoluzione sistema: ', time.strftime("%H:%M:%S"), '\n\n')

    results = opt.solve(instance, tee=True, keepfiles=True)
    print('Instance solved')

    instance.solutions.load_from(results)
    return instance
