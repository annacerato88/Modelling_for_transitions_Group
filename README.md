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
    - CAPEX: same as initial model
    - FOM: same as initial model
    - VOM: same as initial model
    - Efficiency same as initial model 
    - Lifetime: same as initial model 

- DYNAMIC PARAMETERS - HEAT PUMP: 
    - CAPEX: same as initial model [discounted every 10 years by 5%]
    - Subsidy: 30% of initial investment (CAPEX)
    - FOM: same as initial model
    - VOM: same as initial model
    - Efficiency: same as initial model
    - Lifetime: same as initial model

4. We changed how investment_cost is calculated to be able to sweep subsidy levels 

## DEMAND
1. Demand for residential heat was split as follows: 
- Residential heating high insulation 
- Residential heating low insulation 

2. To each demand, the following parameter was added:  
- 'Total_demand': 84890293 MWh -> total demand for water and space heating in the NL for 2020 [https://ec.europa.eu/eurostat/databrowser/view/NRG_D_HHQ__custom_23114672/default/table]

3. We changed how demand is propagated to be able to sweep K (maximum saturation of highly insulated houses)

### Parameters 
Given the changes to the functions, new parameters were added and we determined the following values. 

| Parameter | Symbol | Value | Justification and sources |
|---|---|---|---|
| Initial share of well-insulated homes | s(0) | ~26% | RVO reports that 32% of registered NTA labels meet the insulation standard in 2025 (RVO, 2025).<br>A separate CPB/TNO study agrees roughly: about 5.4M of 8M homes still need work, so around a third don't (Mot et al., 2024).<br>No source measures compliance in 2020, so the figure is back-cast using energy labels as a proxy: the share of homes with label C or better rose from 68% in 2020 (RVO, 2021, p. 25) to 74% in 2025 (RVO, 2025, p. 19), a gain of 6 percentage points.<br>32% − 6 points = 26%, which is about 2.1M of the roughly 8.0M homes in 2020.<br>**ESTIMATE!!**<br>The 6-point gain is borrowed from labels, not measured for the standard, so this is an assumption.<br>Labels changed method in 2021, so the 68% and 74% are not perfectly comparable (RVO, 2024).<br>RVO states its 32% is not representative of the whole housing stock (RVO, 2025). |
| Annual growth rate of well-insulated homes | r | ~3.2% | RVO estimates that around 200k houses per year were brought up to the insulation standard between 2022 and 2026 (RVO, 2025).<br>According to CBS (2026), the Netherlands had approximately 8.345 million homes at the beginning of 2026, with approximately 69,200 newly built homes completed during 2025.<br>Accounting for both the conversion of existing houses and assuming all new buildings meet the insulation standard, this gives a growth rate of 3.2% annually. |
| Gas reduction from insulation | R | ~32% | CPB & TNO (2024) model going from pre-1992 gas-heated homes to the standard. The reduction is 32% of gas use, about 400 m³ per home (gas savings of about 32% of original gas use). A sensitivity test varies it by ±25%, which gives a range of 24–40%.<br>**Measured real-world results are lower (!!!):** the paper mentions that other real-world results find about 20% lower gas use after insulation. |
| Maximum share of well-insulated homes, baseline | K | 70% | This K allows the function to reach the goal of 2.5 million houses by 2030.<br>It assumes the calculation of the stock of well-insulated houses in 2026 was correct (32%).<br>The well-insulated stock reaches around 46% by 2050. |
| Maximum share of well-insulated homes, pessimistic | K | 50% | This K does not allow the function to reach the goal of 2.5 million houses by 2030.<br>It assumes the stock of well-insulated houses in 2026 was overestimated (around 29% instead of 32%).<br>The well-insulated stock reaches around 40% by 2050. |
| Maximum share of well-insulated homes, optimistic | K | 90% | This K allows the function to reach the goal of 2.5 million houses by 2030.<br>It assumes the stock of well-insulated houses in 2026 was underestimated (around 35% instead of 32%).<br>The well-insulated stock reaches around 63% by 2050. |
| Subsidy growth, baseline | subsidy_growth | −0.50 | The subsidy stays constant through 2030 (up to 30%), but is likely lower in the coming decade, as the government is already considering lowering it by almost half (so it would go to 15%) (RVO, 2026; Overheid, 2025). |
| Subsidy growth, pessimistic | subsidy_growth | −1.0 | The subsidy (up to 30%) stops at 2030. |
| Subsidy growth, optimistic | subsidy_growth | 0.0 | The subsidy (up to 30%) lasts through 2050, in line with the Dutch goal to phase out gas and fossil fuels by 2050 (Rijksoverheid, 2026). |
| Efficiency, heat pumps | | 3.0 | Heat pumps typically deliver 3–5 units of heat for every unit of electricity consumed, whereas modern condensing gas boilers deliver approximately 0.90–0.98 units of heat for every unit of gas energy consumed. |
| Efficiency, gas boilers | | 0.90 | See above. |


# Other parameters in excel:  
CAPEX Heat pumps: contrasting data regarding the real reduction in CAPEX for heat pumps, so we kept if to around 5% every 10 years  
- https://research.cbs.dk/en/publications/experience-rates-of-low-carbon-domestic-heating-technologies-in-t/ 
https://ukerc.ac.uk/publications/heat-pump-cost-review/ 

Subsidy for Heat Pumps: around 30% of investment  
- https://www.rijksoverheid.nl/themas/klimaat-milieu-en-natuur/duurzame-energie/vraag-en-antwoord/energie-thuis/krijg-ik-subsidie-voor-een-warmtepomp 

## Bibliography: 
CBS. (2026). Growth of housing stock slows for third year in a row. https://www.cbs.nl/en-gb/news/2026/05/growth-of-housing-stock-slows-for-third-year-in-a-row

International Energy Agency. (2022). The Future of Heat Pumps. https://www.iea.org/reports/the-future-of-heat-pumps/how-a-heat-pump-works

Ministerie van Klimaat en Groene Groei. (2025). Regeling van de Minister van Klimaat en Groene Groei van 4 december 2025, nr. WJZ/100257243, tot wijziging van de Regeling nationale EZ-, LVVN- en KGG-subsidies in verband met de verlenging van de subsidiemodule Investeringssubsidie duurzame energie en energiebesparing (ISDE), titel 4.5. Staatscourant 2025, 42053. https://zoek.officielebekendmakingen.nl/stcrt-2025-42053.html

Mot, E., Mulder, P., Schippers, V., Phan, N., Tigchelaar, C., Zwamborn, A., Fernández Gómez, K., Schulenberg, R., & Griffioen, E. (2024). Inkomenseffecten van woningisolatie naar de isolatiestandaard. Centraal Planbureau & TNO. https://www.cpb.nl/system/files/cpbmedia/omnidownload/CPB-TNO-Publicatie-inkomenseffecten-van-woningisoliatie-naar-de-isolatiestandaard.pdf

Rijksdienst voor Ondernemend Nederland. (2021). Monitor Energiebesparing Gebouwde Omgeving 2021. Ministerie van Binnenlandse Zaken en Koninkrijksrelaties. https://www.rvo.nl/sites/default/files/2021/12/monitor-energiebesparing-gebouwde-omgeving-2021.pdf

Rijksdienst voor Ondernemend Nederland. (2024). Standaard en streefwaarden voor woningisolatie. https://www.rvo.nl/onderwerpen/wetten-en-regels-gebouwen/standaard-streefwaarden-woningisolatie

Rijksdienst voor Ondernemend Nederland. (2025). Monitor Verduurzaming Gebouwde Omgeving 2025. Ministerie van Volkshuisvesting en Ruimtelijke Ordening. https://www.rvo.nl/sites/default/files/2025-12/Monitor%20Verduurzaming%20Gebouwde%20Omgeving%202025.pdf

Rijksdienst voor Ondernemend Nederland. (2026). ISDE: wat wijzigt er vanaf 2027? https://www.rvo.nl/subsidies-financiering/isde/isde-wat-wijzigt-er-2027

Rijksoverheid. (2026). Hoe lang kan ik nog koken en stoken op gas? https://www.rijksoverheid.nl/themas/klimaat-milieu-en-natuur/energie-thuis/vraag-en-antwoord/duurzame-energie/hoe-lang-kan-ik-nog-koken-op-gas

