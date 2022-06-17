
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Asset Pricing Theory empirical definition                                                  -- #
# -- functions.py : It's a python script with principal model calculation                                -- #
# -- author: @bmanica                                                                                    -- #
# -- license: GNU General Public License v3.0                                                            -- #
# -- repository: https://github.com/bmanica/aptmodel-lab2.git                                            -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# ====================================== Required packages ================================================ #

### Libraries to use
import pandas as pd
import numpy as np
import datetime

# =================================== APT model check functions ========================================== #

### Function definition for all orders
def apt_check_all(ob_data):

    # -- General lambda functions definition -- #
    data_adder = lambda each_list, values: each_list.append(values)
    w_mid = lambda b,bv,a,av,d: (bv[:d]/np.add(bv[:d],av[:d]))*a[:d] + (av[:d]/np.add(bv[:d],av[:d]))*b[:d]

    # -- Lists to fill -- #
    exp1_list = []
    total_list = []
    exp2_list = []
    df_list = [] # For big data frame definition

    # -- Generate data frame with all registered orders on each orderbook -- #
    for i in ob_data:

        sub_data = ob_data[i]
        sub_data['mid_price'] = (sub_data['bid'] + sub_data['ask'])*0.5 # Simple mid price
        sub_data['weighted_mid'] = round(w_mid(sub_data['bid'], sub_data['bid_size'],
                                               sub_data['ask'], sub_data['ask_size'], 1), 2) # Weighted mid

        new_i = pd.to_datetime(i) # Datetime type index
        sub_data.index = [datetime.datetime(new_i.year, new_i.month,
                                            new_i.day, new_i.hour, new_i.minute)] * len(sub_data)
        sub_data.index.name = 'times'

        data_adder(df_list, sub_data)

    final_df = pd.concat(df_list)  # Data frame with all orders information

    # -- Calculate experiments for mid and weighted-mid prices -- #
    # Experiment 1 --> mid-price_t == mid-price_t+1
    # Experiment 2 --> mid-price_t != mid-price_t+1

    for i in pd.Series(final_df.index.values).unique():
        price_data = final_df.loc[i]

        # Count each scenario data len
        total = len(price_data) - 1
        data_adder(total_list, total)

        # Experiment 1 definition for each mid-price type
        e1_mid = sum([price_data[i]['mid_price'] == price_data[i+1['mid_price']]
                      for i in range(len(price_data)-1)])

        e1_wmid = sum([price_data[i]['weighted_mid'] == price_data[i+1['weighted_mid']]
                       for i in range(len(price_data)-1)])

        data_adder(exp1_list, [e1_mid, e1_wmid])

        # Experiment 2 definition for each mid-price type
        e2_mid = total - e1_mid
        e2_wmid = total - e1_wmid

        data_adder(exp2_list, [e2_mid, e2_wmid])

    # -- Data frame with final results for each -- #
    simple_mid = pd.DataFrame(columns=['Exp 1', 'Exp 2',
                                       'P. Exp 1', 'P. Exp 2'])

    weighted_mid = simple_mid.copy()

    simple_mid['Exp 1'] = [i[0] for i in exp1_list]
    simple_mid['Exp 2'] = [i[0] for i in exp2_list]
    simple_mid['P. Exp 1'] = np.round(np.array(simple_mid['Exp 1'])/np.array(total_list),2)
    simple_mid.index = pd.Series(final_df.index.values).unique()
    simple_mid.index.name = 'Time'

    weighted_mid['Exp 1'] = [i[1] for i in exp1_list]
    weighted_mid['Exp 2'] = [i[1] for i in exp2_list]
    weighted_mid['P. Exp 1'] = np.round(np.array(weighted_mid['Exp 1']) / np.array(total_list), 2)
    weighted_mid.index = pd.Series(final_df.index.values).unique()
    weighted_mid.index.name = 'Time'

    # -- Return definition -- #
    r_data = {'simple_mid_price': simple_mid, 'weighted_mid_price': weighted_mid}
    return r_data

### Function definition for top of the book orders
def apt_check_top(ob_data):
