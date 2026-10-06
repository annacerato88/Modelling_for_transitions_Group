"""Build and solve the PyPSA energy model."""

# ============================================================
# IMPORTS
# ============================================================
# Import all necessary external packages 
# the preprocessing functions

# Pypsa for energy modelling
import pypsa

# Numpy and Pandas for handling data
import pandas as pd
import numpy as np

# Logging to control running log output
import logging
logging.getLogger("pypsa").setLevel(logging.ERROR)
logging.getLogger("linopy").setLevel(logging.ERROR)
logging.getLogger("gurobipy").setLevel(logging.ERROR)

# Preprocessing functions
from .preprocessing import (
    preprocess_demand,
    preprocess_supply,
    preprocess_technologies,
)


# ============================================================
# MODEL HELPER FUNCTIONS
# ============================================================
# At the end of part 3 of practical.ipynb we defined several 
# helper functions to calculate annuitized costs and to 
# facilitate working with technologies. We need them again here.

def annuity(discount_rate, lifetime):
    """Calculate the annuity factor for an investment."""
    return discount_rate / (1.0 - 1.0 / (1.0 + discount_rate) ** lifetime)


def investment_cost(technology, year, technologies, discount_rate):
    """Calculate the annualised investment cost of a technology."""
    capex = technologies.at[(technology,'CAPEX'),year] 
    fom = technologies.at[(technology,'FOM'),year] 
    lt = technologies.at[(technology,'Lifetime'),year]
    return (capex*annuity(discount_rate, lt) + fom) # (€/activity output unit) 
    

def techs_by_type(technologies, tech_type):
    """Return the technologies belonging to a given PyPSA component type."""
    types = technologies.query("Parameter=='Type'").reset_index()
    return list(types[types['Value']==tech_type]['Technology'].unique())

def get_topology(technologies, technology):
    """Return the network topology associated with a technology."""
    techdf = technologies.loc[(technology,slice(None)),:].reset_index()
    techdf = techdf[techdf.Parameter.str.startswith('bus')].set_index('Parameter')
    return techdf

def start_year(technologies, technology, default_year):
    """Return the first year in which a technology can be built."""
    try: 
        sy = technologies.at[(technology,'Start year'),'Value']
    except KeyError:
        sy = default_year[0]
    return sy


# ============================================================
# MAIN MODEL FUNCTION
# ============================================================

def model_run(db_dir, years, t_res, passenger_cars_cf, rt, rs):
    """
    Build and solve the energy model.

    Parameters
    ----------
    db_dir
        Folder containing the input database.
    years
        Model periods.
    t_res
        Intra-year temporal resolution.
    passenger_cars_cf
        Conversion factor for passenger cars.
    rt
        Technical discount rate.
    rs
        Social discount rate.

    Returns
    -------
    pypsa.Network
        The optimized PyPSA network.
    """

    # --------------------------
    # 1. PREPROCESS INPUT DATA
    # --------------------------

    # Call the preprocessing functions and store their outputs.
    
    demands, demand_profiles_prj = preprocess_demand(
                db_dir, years, t_res
            )
    resources, resources_pars, ren_profiles = preprocess_supply(
            db_dir, years, t_res
        )
    techs_s, techs_d = preprocess_technologies(
            db_dir, years, passenger_cars_cf
        )


    # --------------------------
    # 2. CREATE PYPSA NETWORK
    # --------------------------
    # Usual code to create a new PyPSA network, 
    # define snapshots and investment periods from demand profiles index, 
    # and set weight and lenght of each period
    
    n = pypsa.Network()

    n.set_snapshots(demand_profiles_prj.index, 
                default_snapshot_weightings=t_res)

    n.investment_periods = years

    n.investment_period_weightings['years'] = list(np.diff(years)) + [list(np.diff(years))[-1]]

    T = 0
    for period, nyears in n.investment_period_weightings.years.items():
        discounts = [(1 / (1 + rs) ** t) for t in range(T, T + nyears)]
        n.investment_period_weightings.at[period, 'objective'] = sum(discounts)
        T += nyears

    # --------------------------
    # 3. ADD BUSES AND LOADS
    # --------------------------
    # From the demand dataframe: add all buses and corresponding loads
    
    ### YOUR CODE HERE
    for b in demands.Bus.unique():
        n.add("Bus", b, carrier=demands[demands.Bus==b]['Carrier'].values[0])

    # Add loads, with the right demand bus from the demands dataframe
    # and the right profile from the demand_profiles_prj dataframe
    for d in demands.index:
        ### YOUR CODE HERE ###
        n.add("Load", d, bus=demands.loc[d, "Bus"], p_set=demand_profiles_prj[d])
    ###

    # --------------------------
    # 4. ADD RESOURCES
    # --------------------------
    # From the resources dataframe, loop over all resources 
    # and distinguish three separate cases:
    #   1. For Secondary resources add a bus
    #   2. For Reserves add a bus and a store
    #   3. For Emissions add a bus, a store and a maximum limit    

    ### YOUR CODE HERE
    for s in resources['Resource'].unique():

        # for secondary resources add a bus
        if resources[resources.Resource==s]['Type'].values[0] == 'Secondary':
            n.add("Bus", s, carrier = resources[resources.Resource==s]['Carrier'].values[0])

        #  for reserves add a bus...
        elif resources[resources.Resource==s]['Type'].values[0] == 'Reserve':
            ### YOUR CODE HERE ###
            n.add("Bus", s, carrier = resources[resources.Resource==s]['Carrier'].values[0])
            ###
        
            # ... and a store
            n.add(
                "Store",
                s,
                carrier = resources[resources.Resource==s]['Carrier'].values[0],
                bus = s,
                # Max energy in the store at any given time:
                e_nom = resources_pars[(resources_pars.Resource==s) & (resources_pars.Parameter=='Reserves')][years[0]].values[0],
                # Initial energy in the store (it's a reserve, so we set it equal to e_nom)
                e_initial = resources_pars[(resources_pars.Resource==s) & (resources_pars.Parameter=='Reserves')][years[0]].values[0],
                # Whether the model can optimize e_nom
                e_nom_extendable = False,
                # Whether the stored energy has to return to e_initial at the end of a period
                e_cyclic = False,
                )
        
        # For emissions add a bus...
        elif resources[resources.Resource==s]['Type'].values[0] == 'Emissions':
            ### YOUR CODE HERE ###
            n.add("Bus", s, carrier = resources[resources.Resource==s]['Carrier'].values[0]) 
            ###

            # ... an upper value to limit maximum cumulated emissions at any snapshot within a given year...
            co2_max_profile = pd.Series(index=n.snapshots, dtype=float)
            for y in years:
                co2_max_profile.loc[y] = resources_pars[(resources_pars.Resource==s) &\
                                                        (resources_pars.Parameter=='Budget')][y].values[0]

            # ... and a store
            n.add(
                "Store",
                s,
                carrier=resources[resources.Resource==s]['Carrier'].values[0],
                bus=s,
                # For CO2 we add e_nom as a normalized value...
                e_nom=1,
                # ... and then we set the yearly max cumulated emissions relative to e_nom
                e_max_pu = co2_max_profile, 
                e_initial=0,
                e_nom_extendable=False,
                e_cyclic=False,
                )

    ###

    # --------------------------
    # 5. ADD TECHNOLOGIES
    # --------------------------
    # Loop over periods to add all technologies, 
    # distinguishing three separate cases:
    #   1. Generators - loop through all generators and add them to the network
    #   2. Links - loop over all links, check type of link 
    #              (nr of inputs and outputs), and add to the network
    #   3. Storage Units - loop over all storage units and add them to the network

    ### YOUR CODE HERE
    # Loop over model years to add all technologies:
    for y in years:
        print(y)

        # We use techs_by_type to distinguish generators, links and storage units

        # Generators:
        for t in techs_by_type(techs_s, 'Generator'):
            bus0 = techs_s.at[(t,'bus0'), 'Value'] # bus0 as carrier
            bus1 = techs_s.at[(t,'bus1'), 'Value'] # bus1 as bus

            n.add(
                'Generator',
                f'{t}_{y}',
                carrier = bus0,
                bus = bus1,
                p_nom_extendable = True,
                p_max_pu = ren_profiles[bus0].values, # apply renewable profiles as max availability factors
                build_year = max([start_year(techs_s,t,years),y]),  # make sure t won't be built before its start_year
                capital_cost = investment_cost(t, y, techs_d, rt),

                # Add marginal_cost, lifetime and efficiency direclty from techs_d
                ### YOUR CODE HERE ###
                
                marginal_cost= techs_d.at[(t,'VOM'), y],
                lifetime = techs_d.at[(t,'Lifetime'), y],
                efficiency = techs_d.at[(t,'Efficiency'), y],                      

                )
        
        # Links:
        for t in techs_by_type(techs_s,'Link'):

            # First, get the link topology dataframe
            topology = get_topology(techs_s, t)

            # Second, check if a cost is specified for any of the buses in the link
            bus_cost = {}
            for b in topology.index:
                try:
                    bus_cost[b] = resources_pars[(resources_pars.Resource==topology.at[b,'Value']) &\
                                                (resources_pars.Parameter=='Price')][y].values[0]
                    
                    # NOTE: empty price cell gives NaN (no error raised), so I set it to 0 if NaN 
                    if pd.isna(bus_cost[b]):
                        bus_cost[b] = 0
                # In case there are no costs specified and an error is raised, set the costs to 0:
                except IndexError:
                    bus_cost[b] = 0 
                except KeyError:
                    bus_cost[b] = 0 

            # For now we have two types of links: 

            # 1. Simple link, one input one output (two  buses)
            if len(topology)==2:
                n.add(
                    'Link',
                    f'{t}_{y}',
                    carrier = t, # for links we will use the technology name as carrier (it helps sorting out the results)
                    bus0 = topology.at['bus0','Value'], # input bus
                    bus1 = topology.at['bus1','Value'], # output bus
                    p_nom_extendable = True,
                    build_year = max([start_year(techs_s,t,years),y]),
                    capital_cost = investment_cost(t, y, techs_d, rt) * techs_d.at[(t,'Efficiency'), y], # for links costs are expressed in €/activity unit input
                    marginal_cost = techs_d.at[(t,'VOM'), y] + bus_cost['bus0'] + bus_cost['bus1']*techs_d.at[(t,'Efficiency'), y], # VOM + any costs associated with the inputs or the outputs
                    lifetime = techs_d.at[(t,'Lifetime'), y],
                    efficiency = techs_d.at[(t,'Efficiency'), y],
                    )
                
            # 2. Link with three buses (e.g. links with emissions)
            elif len(topology)==3:
                # Such a link will have two efficiencies:
                eff1 = techs_d.at[(t,'Efficiency'), y]
                eff2 = techs_d.at[(t,topology.at['bus2','Efficiency_link']), y]

                # Add the link as in the previous case, paying attention to the following:
                # - there are now three buses: bus0, bus1 and bus2
                # - marignal costs will be VOM + any costs related to any of the 3 buses
                # - there are two efficiencies: efficiency and efficiency2
                ### YOUR CODE HERE ###
                
                n.add(
                        'Link',
                        f'{t}_{y}',
                        carrier = t, 
                        bus0 = topology.at['bus0','Value'], # input bus
                        bus1 = topology.at['bus1','Value'], # output bus
                        bus2 = topology.at['bus2', 'Value'], # emissions bus
                        p_nom_extendable = True,
                        build_year = max([start_year(techs_s,t,years),y]),
                        capital_cost = investment_cost(t, y, techs_d, rt) * techs_d.at[(t,'Efficiency'), y], 
                        marginal_cost = techs_d.at[(t,'VOM'), y] + bus_cost['bus0'] + bus_cost['bus1']*eff1 + bus_cost['bus2']*eff2, 
                        lifetime = techs_d.at[(t,'Lifetime'), y],
                        efficiency = eff1,
                        efficiency2 = eff2
                                )
            
                ### 

        # StorageUnits
        for t in techs_by_type(techs_s,'StorageUnit'):
            n.add(
                'StorageUnit',
                f'{t}_{y}',
                bus = techs_s.at[(t,'bus0'), 'Value'],
                carrier = t,
                capital_cost = investment_cost(t,y,techs_d,rt),
                efficiency_store = techs_d.at[(t,'Efficiency'), y],
                efficiency_dispatch = techs_d.at[(t,'Efficiency'), y],
                build_year = max([start_year(techs_s,t,years),y]),
                p_nom_extendable=True,
                cyclic_state_of_charge=True,
            )
    ###

    # --------------------------
    # 6. SOLVE MODEL
    # --------------------------
    # Sanitize and solve, storing model status and condition, 
    # and logging in a separate log file

    n.sanitize()
    status, condition = n.optimize(multi_investment_periods=True, 
            solver_name='gurobi',
            log_to_console=False,          # No pypsa outputs
            include_objective_constant=False, 
            solver_options={
                # "LogFile": " results / solver_run.log",
                "LogToConsole": 0,
                "TimeLimit": 43200
                }
            )


    # --------------------------
    # 7. RETURN RESULTS
    # --------------------------
    # Print model status and condition and return the network

    print("\n")
    print(f"Model Status: {status}")
    print(f"Termination Condition: {condition}")
    
    return n