"""Build and solve the PyPSA energy model."""

# ============================================================
# IMPORTS
# ============================================================
# Import all necessary external packages 
# the preprocessing functions

# Pypsa for energy modelling
# ...
# Preprocessing functions


# ============================================================
# MODEL HELPER FUNCTIONS
# ============================================================
# At the end of part 3 of practical.ipynb we defined several 
# helper functions to calculate annuitized costs and to 
# facilitate working with technologies. We need them again here.

# def annuity(discount_rate, lifetime):
# def investment_cost(technology, year, technologies, discount_rate):
# def techs_by_type(technologies, tech_type):
# ...

# ============================================================
# MAIN MODEL FUNCTION
# ============================================================

# def model_run(db_dir, years, t_res, passenger_cars_cf, rt, rs):
    # """
    # Build and solve the energy model.
    # """

    # --------------------------
    # 1. PREPROCESS INPUT DATA
    # --------------------------
    # Call the preprocessing functions and store their outputs.

    # --------------------------
    # 2. CREATE PYPSA NETWORK
    # --------------------------
    # Usual code to create a new PyPSA network, 
    # define snapshots and investment periods from demand profiles index, 
    # and set weight and lenght of each period

    # --------------------------
    # 3. ADD BUSES AND LOADS
    # --------------------------
    # From the demand dataframe: add all buses and corresponding loads
 
     # --------------------------
    # 4. ADD RESOURCES
    # --------------------------
    # From the resources dataframe, loop over all resources 
    # and distinguish three separate cases:
    #   1. For Secondary resources add a bus
    #   2. For Reserves add a bus and a store
    #   3. For Emissions add a bus, a store and a maximum limit    
    
    # --------------------------
    # 5. ADD TECHNOLOGIES
    # --------------------------
    # Loop over periods to add all technologies, 
    # distinguishing three separate cases:
    #   1. Generators - loop through all generators and add them to the network
    #   2. Links - loop over all links, check type of link 
    #              (nr of inputs and outputs), and add to the network
    #   3. Storage Units - loop over all storage units and add them to the network

    # --------------------------
    # 6. SOLVE MODEL
    # --------------------------
    # Sanitize and solve, storing model status and condition, 
    # and logging in a separate log file

    # --------------------------
    # 7. RETURN RESULTS
    # --------------------------
    # Print model status and condition and return the network
