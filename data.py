
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Asset Pricing Theory empirical definition                                                  -- #
# -- data.py : It's a python script for data collection and processing                                   -- #
# -- author: @bmanica                                                                                    -- #
# -- license: GNU General Public License v3.0                                                            -- #
# -- repository: https://github.com/bmanica/aptmodel-lab2.git                                            -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# ====================================== Required packages ================================================ #

### Libraries to use
import pandas as pd
import json

# ================================= Data object definition ================================================ #

### Let's start for the OrderBook data
file = open('files/orderbooks_05jul21.json')
orderbooks = json.load(file)

# Take each one of the exchanges
ob_data_bit = orderbooks['bitfinex']
ob_data_kra = orderbooks['kraken']

# Drop None keys
ob_data_bit = {key: value for key, value in ob_data_bit.items() if value is not None}
ob_data_kra = {key: value for key, value in ob_data_kra.items() if value is not None}

# Convert into pandas dataframe and rearange columns
ob_data_bit = {orderbook: pd.DataFrame(ob_data_bit[orderbook])[['bid_size', 'bid', 'ask', 'ask_size']]
               for orderbook in list(ob_data_bit.keys())}

ob_data_kra = {orderbook: pd.DataFrame(ob_data_kra[orderbook])[['bid_size', 'bid', 'ask', 'ask_size']]
               for orderbook in list(ob_data_kra.keys())}