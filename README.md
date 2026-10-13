# Modelling_for_transitions_Group
Group assignment for the course Modelling for Transitions

# Overarching plan 
In this assignment, we modified the main model built throughout the course to study the effect of different subsidies levels for heat pumps and different insulation levels on emissions and overall system costs. The following text provides an overview of the changes, and the notebook changes.ipynb illustrates the code sections that were changed. 

## TECHNOLOGIES
1. Three main technologies of interest 
- Gas boiler high 
- Gas boiler low
- Heat pump 

2. For each technology, static parameters read as follows: 
- STATIC PARAMETERS - GAS BOILER HIGH: 
    - Type: Link 
    - Sector: Residential 
    - bus0: Gas supply
    - bus1: Residential heating high insulation 
    - bus2: emissions  

- STATIC PARAMETERS - GAS BOILER LOW: 
    - Type: Link 
    - Sector: Residential 
    - bus0: Gas supply
    - bus1: Residential heating low insulation 
    - bus2: emissions  

- STATIC PARAMETERS - HEAT PUMP: 
    - Type: Link 
    - Sector: Residential 
    - bus0: Electricity
    - bus1: Residential heating high insulation  

3. For each technology, dynamic parameters were modified as follows:
- DYNAMIC PARAMETERS - GAS BOILER HIGH + GAS BOILER LOW: 
    - CAPEX: [TBD] -> find out the baseline CAPEX gas boilers 
    - FOM: [TBD] -> find out for both 
    - VOM: [TBD] -> find out for both
    - Efficiency [TBD] -> find out for both 
    - Lifetime: [TBD] -> find out for both 

- DYNAMIC PARAMETERS - HEAT PUMP: 
    - CAPEX: [TBD] -> find out the baseline CAPEX gas boilers
    - Subsidy: [TBD] -> set up baseline subsidy for heat pumps (so stopping at 2030) 
    - FOM: [TBD] -> find out for both 
    - VOM: [TBD] -> find out for both
    - Efficiency [TBD] -> find out for both 
    - Lifetime: [TBD] -> find out for both 

4. We changed how investment_cost is calculated to be able to sweep subsidy levels 

## DEMAND
1. Demand for residential heat was split as follows: 
- Residential heating high insulation 
- Residential heating low insulation 

2. To each demand, the following parameter was added:  
- 'Total_demand': 84890293 MWh -> total demand for water and space heating in the NL for 2020 [https://ec.europa.eu/eurostat/databrowser/view/NRG_D_HHQ__custom_23114672/default/table]

3. We changed how demand is propagated to be able to sweep K (maximum saturation of highly insulated houses)