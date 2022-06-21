
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Asset Pricing Theory and Roll model empirical definition                                   -- #
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
from statsmodels.tsa.stattools import acovf

# =================================== APT model check functions =========================================== #

### Function definition for all orders
def apt_check_all(ob_data:dict) -> dict:

    """
    Test APT model function (for all orders contained on each orderbook)

    Parameters
    ----------

    ob_data:dict (default:None) --> Required parameter
        Input data from orderbook, it has to be a dict of data frames with the following structure:

        'timestamp': Principal key, correspond to the timestamp associated to each orderbook
        'bid_size': First column on each data frame, correspond to the bid volume associated to each bid price order
        'bid': Second column of the data frame, correspond to the highest price a buyer is willing to buy
        'ask': Third column of the data frame, correspond to the lowest price a seller is willing to sell
        'ask_size': Fourth column of the data frame, correspond to the ask volume associated to each ask price order

    Returns
    -------

    r_data: dict
        Return data, it's a dict of data frames where each one of them contains the result of the proposing experiments
        the dict of return follows the next structure:

        'simple_mid_price': First key, contains all the experiments developed for APT model testing with simple
                            mid-price
        'weighted_mid_price': Second key, contains all the experiments developed for APT model testing with weighted
                              mid-price

    References
    ----------

    [1] https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
    """

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
        sub_data['mid_price'] = (sub_data['bid'] + sub_data['ask'])*0.5 # Simple mid-price
        sub_data['weighted_mid'] = round(w_mid(sub_data['bid'], sub_data['bid_size'],
                                               sub_data['ask'], sub_data['ask_size'], len(sub_data)), 2)

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
        e1_mid = sum([price_data['mid_price'][i] == price_data['mid_price'][i+1]
                      for i in range(len(price_data)-1)])

        e1_wmid = sum([price_data['weighted_mid'][i] == price_data['weighted_mid'][i+1]
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
    simple_mid['P. Exp 2'] = 1 - simple_mid['P. Exp 1']
    simple_mid.index = pd.Series(final_df.index.values).unique()
    simple_mid.index.name = 'Time'

    weighted_mid['Exp 1'] = [i[1] for i in exp1_list]
    weighted_mid['Exp 2'] = [i[1] for i in exp2_list]
    weighted_mid['P. Exp 1'] = np.round(np.array(weighted_mid['Exp 1']) / np.array(total_list), 2)
    weighted_mid['P. Exp 2'] = 1 - weighted_mid['P. Exp 1']
    weighted_mid.index = pd.Series(final_df.index.values).unique()
    weighted_mid.index.name = 'Time'

    # -- Return definition -- #
    r_data = {'simple_mid_price': simple_mid, 'weighted_mid_price': weighted_mid}
    return r_data

### Function definition for top of the book orders
def apt_check_tob(ob_data:dict) -> dict:

    """
    Test APT model function (just for top of the book orders contained on each orderbook)

    Parameters
    ----------

    ob_data:dict (default:None) --> Required parameter
        Input data from orderbook, it has to be a dict of data frames with the following structure:

        'timestamp': Principal key, correspond to the timestamp associated to each orderbook
        'bid_size': First column on each data frame, correspond to the bid volume associated to each bid price order
        'bid': Second column of the data frame, correspond to the highest price a buyer is willing to buy
        'ask': Third column of the data frame, correspond to the lowest price a seller is willing to sell
        'ask_size': Fourth column of the data frame, correspond to the ask volume associated to each ask price order

    Returns
    -------

    r_data: dict
        Return data, it's a dict of data frames where each one of them contains the result of the proposing experiments
        the dict of return follows the next structure:

        'simple_mid_price': First key, contains all the experiments developed for APT model testing with simple
                            mid-price
        'weighted_mid_price_a': Second key, contains all the experiments developed for APT model testing with weighted
                                mid-price (the first way of calculation).
        'weighted_mid_price_b': Second key, contains all the experiments developed for APT model testing with weighted
                                mid-price (the second way of calculation)

    References
    ----------

    [1] https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
    """

    # -- General lambda functions definition -- #
    calc_inbalace = lambda b, a, d: np.sum(b[:d]) / np.sum(np.add(b[:d], a[:d]))
    w_mid = lambda b,bv,a,av,d: (bv[:d]/np.add(bv[:d],av[:d]))*a[:d]+(av[:d]/np.add(bv[:d],av[:d]))*b[:d]
    apt_check = lambda df: sum(df['Simple Mid-Price'].shift() == df['Simple Mid-Price'])
    apt_check_a = lambda df: sum(df['Weighted Mid-Price A'].shift() == df['Weighted Mid-Price A'])
    apt_check_b = lambda df: sum(df['Weighted Mid-Price B'].shift() == df['Weighted Mid-Price B'])

    # -- Data frame of analysis definition -- #
    price_df = pd.DataFrame.from_dict({i: [(ob_data[i].iloc[0,:]['ask'] + ob_data[i].iloc[0,:]['bid'])*0.5,

                                       round((calc_inbalace(ob_data[i]['bid_size'],
                                                            ob_data[i]['ask_size'],
                       len(ob_data[i])))*((ob_data[i].iloc[0,:]['ask']+ob_data[i].iloc[0,:]['bid'])*0.5),2),

                                            round(w_mid(ob_data[i]['bid'], ob_data[i]['bid_size'],
                                                   ob_data[i]['ask'], ob_data[i]['ask_size'],1)[0], 2)]

                                            for i in ob_data}).T

    price_df.index = pd.to_datetime(pd.Series(price_df.index.values))
    price_df.columns = ['Simple Mid-Price', 'Weighted Mid-Price A', 'Weighted Mid-Price B']

    # -- Grouping by 1 minute frequency -- #
    # First data frame defined for simple mid-price
    apt_mid_e1 = price_df.groupby(pd.Grouper(freq='1min')).apply(apt_check).tolist()
    apt_mid_total = price_df.groupby(pd.Grouper(freq='1min')).count()['Simple Mid-Price']
    apt_mid_e2 = (np.array(apt_mid_total) - np.array(apt_mid_e1)).tolist()

    # Second data frame defined for weighted mid-price a
    apt_wmida_e1 = price_df.groupby(pd.Grouper(freq='1min')).apply(apt_check_a).tolist()
    apt_wmida_e2 = (np.array(apt_mid_total) - np.array(apt_wmida_e1)).tolist()

    # Third data frame defined for weighted mid-price b
    apt_wmidb_e1 = price_df.groupby(pd.Grouper(freq='1min')).apply(apt_check_b).tolist()
    apt_wmidb_e2 = (np.array(apt_mid_total) - np.array(apt_wmidb_e1)).tolist()

    # -- Data frame with final results for each -- #
    simple_mid = pd.DataFrame(columns=['Exp 1', 'Exp 2',
                                       'P. Exp 1', 'P. Exp 2'])

    weighted_mid_a = simple_mid.copy()
    weighted_mid_b = simple_mid.copy()

    simple_mid['Exp 1'] = apt_mid_e1
    simple_mid['Exp 2'] = apt_mid_e2
    simple_mid['P. Exp 1'] = list(np.round(np.array(apt_mid_e1) / np.array(apt_mid_total),2))
    simple_mid['P. Exp 2'] = 1 - simple_mid['P. Exp 1']
    simple_mid.index = apt_mid_total.index.values
    simple_mid.index.name = 'Time'

    weighted_mid_a['Exp 1'] = apt_wmida_e1
    weighted_mid_a['Exp 2'] = apt_wmida_e2
    weighted_mid_a['P. Exp 1'] = list(np.round(np.array(apt_wmida_e1) / np.array(apt_mid_total),2))
    weighted_mid_a['P. Exp 2'] = 1 - weighted_mid_a['P. Exp 1']
    weighted_mid_a.index = apt_mid_total.index.values
    weighted_mid_a.index.name = 'Time'

    weighted_mid_b['Exp 1'] = apt_wmidb_e1
    weighted_mid_b['Exp 2'] = apt_wmidb_e2
    weighted_mid_b['P. Exp 1'] = list(np.round(np.array(apt_wmidb_e1) / np.array(apt_mid_total),2))
    weighted_mid_b['P. Exp 2'] = 1 - weighted_mid_b['P. Exp 1']
    weighted_mid_b.index = apt_mid_total.index.values
    weighted_mid_b.index.name = 'Time'

    # -- Return data -- #
    r_data = {'simple_mid_price': simple_mid, 'weighted_mid_price_a': weighted_mid_a,
              'weighted_mid_price_b': weighted_mid_b}

    return r_data

# =================================== Roll model check function =========================================== #

### Function definition for Roll model validation
def roll_model_check(ob_data:dict,
                     pt_data:pd.DataFrame) -> dict:

    # -- Generalized lambda functions -- #
    prob_evo = lambda series,end,counter: round(list(series[0:end]).count(counter) / len(series[0:end]), 4)

    # -- Data frame definition -- #
    roll_df = pd.DataFrame.from_dict({i: (ob_data[i]['bid_size'].iloc[0], ob_data[i]['bid'].iloc[0],
                                          ob_data[i]['ask'].iloc[0], ob_data[i]['ask_size'].iloc[0],
                                          (ob_data[i].iloc[0]['bid'] + ob_data[i].iloc[0]['ask'])*0.5)
                                      for i in ob_data}).T

    roll_df.index = pd.to_datetime(roll_df.index.values)
    roll_df.index.name = 'Time'
    roll_df.columns = ['bid_size', 'bid', 'ask', 'ask_size', 'mid_price']

    # -- Differences between prices -- #
    diff_prices = [roll_df['mid_price'][i+1] - roll_df['mid_price'][i] for i in range(len(roll_df)-1)]

    # -- Theoretical spread calculation -- #
    # Model spread definition --> Spread = 2*C: C = sqrt(-gamma_1): gamma_1 = Cov(delta(p_t-1)*delta(p_t))
    # First let's define a generalized spread for all orderbook data
    ob_teo_spread = round(np.sqrt(np.abs(acovf(np.array(diff_prices), adjusted=True, nlag=1)[1]))*2, 6)

    # Now let's describe the evolution of that theoretical spread
    teo_spread = [np.sqrt(np.abs(acovf(np.array(diff_prices[0:i]), adjusted=True, nlag=1)[1]))*2
                  for i in range(2, len(diff_prices)+1)]

    # -- Data frame consolidation for theoretical and real spread -- #
    roll_df['real_spread'] = roll_df['ask'] - roll_df['bid']
    roll_df['theoretical_spread'] = [0.0, 0.0] + teo_spread # Add zeros because of time lags
    roll_df['theoretical_bid'] = roll_df['mid_price'] - ob_teo_spread
    roll_df['theoretical_ask'] = roll_df['mid_price'] + ob_teo_spread

    # -- Data frame definition for probability of buy or sell -- #
    sell_evo = [prob_evo(pt_data.side, i, "sell") for i in range(1,50001)] # 50000 scenarios
    buy_evo = list((1-np.array(sell_evo)))

    pt_data_sample = pt_data[0:50000]
    pt_data_sample['prob_sell'] = sell_evo
    pt_data_sample['prob_buy'] = buy_evo
    pt_data_sample['timestamp'] = pd.to_datetime(pt_data_sample['timestamp'])

    # -- Return data -- #
    r_data = {'spread_definition': roll_df, 'prob_evolution': pt_data_sample}

    return r_data