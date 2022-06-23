
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Asset Pricing Theory and Roll model empirical definition                                   -- #
# -- main.py : It's a python script with the main functionality of the whole project                     -- #
# -- author: @bmanica                                                                                    -- #
# -- license: GNU General Public License v3.0                                                            -- #
# -- repository: https://github.com/bmanica/aptmodel-lab2.git                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# =================================== Required packages and scripts ======================================= #
# Required packages
import pandas as pd
import numpy as np
import warnings

# Required local scripts
import data as dt
import functions as fn
import visualizations as vz

# ======================================== Data description =============================================== #

# -- For OrderBook data -- #
# Let's visualize the keys range.
ob_data = dt.ob_data_bit
range_ob = pd.to_datetime(pd.Series(list(ob_data.keys()))).sort_values()
print(f'El primer tiempo registrado está en: {range_ob[0]}, y el último en: {range_ob.tail(1).item()}')

# Let's see how many books do we have
print(f'En una hora de tiempo contamos con {len(list(ob_data.keys())):,} libros')

# Let's see the first orderbook values
print(f'Este primer orderbook corresponde al punto en el tiempo. {range_ob[0]}:')
list(ob_data.values())[0].head(5)

# -- For PublicTrades data -- #
# Let's visualize the df range.
pt_data = dt.pt_data
range_pt = pd.to_datetime(pt_data.timestamp).sort_values()
print(f'''El primer tiempo registrado está en: 
{range_pt.head(1).item()}, y el último en: {range_pt.tail(1).item()}''')

# Let's see the public trades dataframe
print(f'Los public trades con los que contamos tienen un total de {pt_data.shape[0]:,} filas')
pt_data.head()

# ======================================== APT model testing ============================================== #

# -- Run functions -- #
apt_all = fn.apt_check_all(ob_data)
apt_tob = fn.apt_check_tob(ob_data)

print(f'The keys for apt model test with all orders are: {list(apt_all.keys())}')
print(f'The keys for apt model test with tob orders are: {list(apt_tob.keys())}')

# -- Test all orders contained -- #
# Let's see the data frame for simple mid-price test
print(f'''The min proportion where the mid-price follows martingale process is: 
{apt_all['simple_mid_price']['P. Exp 1'].min()}
and it happened on {apt_all['simple_mid_price']['P. Exp 1'].idxmin()}''')
print("")
print(f'''The mean proportion where the mid-price follows martingale process is:
{round(apt_all['simple_mid_price']['P. Exp 1'].mean(),4)*100}%''')

apt_all['simple_mid_price'].head()

# Let's see the data frame for weighted mid-price test
print(f'''The max proportion where the mid-price follows martingale process is:
{apt_all['weighted_mid_price']['P. Exp 1'].max()}
and it happened on {apt_all['weighted_mid_price']['P. Exp 1'].idxmax()}''')
print("")
print(f'''The mean proportion where the mid-price follows martingale process is:
{round(apt_all['weighted_mid_price']['P. Exp 1'].mean(),4)*100}%''')

apt_all['weighted_mid_price'].head()

# -- Test top of the book orders -- #
# Now let's render the simple mid-price experiment just for tob
print(f'''The min proportion where the mid-price follows martingale process is:
{apt_tob['simple_mid_price']['P. Exp 1'].min()}
and it happened on {apt_tob['simple_mid_price']['P. Exp 1'].idxmin()}''')
print("")
print(f'''The mean proportion where the mid-price follows martingale process is:
{round(apt_tob['simple_mid_price']['P. Exp 1'].mean(),4)*100}%''')

apt_tob['simple_mid_price'].head()

# Let's see the mean proportion for experiment 1.
print(f'''With all orders we have a mean proportion of:
{round(apt_all['simple_mid_price']['P. Exp 1'].mean(),4)*100}%''')
print(f'''With tob orders we have a mean proportion of:
{round(apt_tob['simple_mid_price']['P. Exp 1'].mean(),4)*100}%''')

# Let's see now the tob experiments for the first way of calculation of weighted mid-price (A)
print(f'''The min proportion where mid-price follows martingale process is:
{apt_tob['weighted_mid_price_a']['P. Exp 1'].min()}
and it happened on {apt_tob['weighted_mid_price_a']['P. Exp 1'].idxmin()}''')
print("")
print(f'''The mean proportion where the mid-price follows martingale process is:
{round(apt_tob['weighted_mid_price_a']['P. Exp 1'].mean(),4)*100}%''')

apt_tob['weighted_mid_price_a'].head()

# Now let's compare it with the alternative way of calculating weighted mid-price (B)
print(f'''The min proportion where mid-price follows martingale process is:
{apt_tob['weighted_mid_price_b']['P. Exp 1'].min()}
and it happened on {apt_tob['weighted_mid_price_b']['P. Exp 1'].idxmin()}''')
print("")
print(f'''The mean proportion where the mid-price follows martingale process is:
{round(apt_tob['weighted_mid_price_b']['P. Exp 1'].mean(),4)*100}%''')

apt_tob['weighted_mid_price_b'].head()

# ======================================== Roll model testing ============================================= #

# -- Run functions -- #
warnings.filterwarnings("ignore")
pt_data = dt.pt_data
roll_model = fn.roll_model_check(ob_data, pt_data)
print(f'The keys for roll model testing functions are: {roll_model.keys()}')


# =================================== Results and visual resources ======================================== #

# -- APT model charts -- #
# Let's see how stands the proportion of times where the price follows a martingale process (all orders)
vz.plot_stacked_bar(apt_all['simple_mid_price'], minutes=30)

# Let's see how stands the proportion of times where the price follows a martingale process (tob orders)
vz.plot_stacked_bar(apt_tob['simple_mid_price'], minutes=30)

# -- Roll model charts -- #
# Let's see how theoretical spread stands againts real observed spread
vz.plot_teo_spread(roll_model['spread_definition'])['spread']

# Let's see how is the difference between spreads (theoretical vs observed)
vz.plot_teo_spread(roll_model['spread_definition'])['diff']

# Let's see how all of our theoretical metrics are defined
vz.plot_teo_spread(roll_model['spread_definition'])['theo']

# Let's see how the bid value behave
vz.plot_teo_spread(roll_model['spread_definition'])['bid']

# Let's see how the ask value behave
vz.plot_teo_spread(roll_model['spread_definition'])['ask']

# Let's see how all of our real observed metrics are defined
vz.plot_teo_spread(roll_model['spread_definition'])['real']

# Let's see the probability evolution within orders type
vz.plot_prob_evo(roll_model['prob_evolution'])
