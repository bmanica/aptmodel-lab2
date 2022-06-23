
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Asset Pricing Theory and Roll model empirical definition                                   -- #
# -- visualizations.py : It's a python script with data visualization functions                          -- #
# -- author: @bmanica                                                                                    -- #
# -- license: GNU General Public License v3.0                                                            -- #
# -- repository: https://github.com/bmanica/aptmodel-lab2.git                                            -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# ====================================== Required packages ================================================ #

### Libraries to use
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ============================== Stacked bar chart for APT model test ===================================== #

### Function definition
def plot_stacked_bar(exp_df:pd.DataFrame,
                     minutes:int=None):

    """
    Stacked bar plot generator for the experiments proposed in APT model testing

    Parameters
    ----------

    exp_df: DataFrame (default:None) --> Required parameter
        Principal input data, correspond to a data frame where Exp. 1 and Exp. 2 where developed, it has to follow the
        next structure:

        'Time': Datetime data frame index consolidated by minute
        'Exp 1': Number of occurrences where mid-price(t) == mid-price(t+1)
        'Exp 2': Number of occurrences where mid-price(t) != mid-price(t+1)
        'P. Exp 1': Proportion of observations that satisfies the first experiment
        'P. Exp 2': Proportion of observations that satisfies the second experiment

    minutes: Integer (default:None) --> Optional parameter
        Number of minutes that the user want to see in the chart (it has to follow the time frame structure of data)

    Returns
    -------

    fig: Figure
        Plotly figure containing a stacked bar chart with the proportion of the developed experiments in APT model
        testing

    References
    ----------

    [1] https://plotly.com/python/horizontal-bar-charts/
    """

    # -- Define the minutes structure -- #
    if minutes is None:

        # Plot definition
        fig = go.Figure(data=[

            go.Bar(name='Exp. 1', x=pd.Series(exp_df.index.values), y=exp_df['Exp 1'],
                   marker={'color': '#15569B'}),

            go.Bar(name='Exp. 2', x=pd.Series(exp_df.index.values), y=exp_df['Exp 2'],
                   marker={'color': '#C22911'})
        ])

        # Plot configurations
        fig.update_layout(barmode='stack', height=500,
                          font_family='Oswald, sans-serif', title_text='<b>Experiment frequency for APT<b>')
        fig['layout']['title']['font'] = dict(size=19)
        fig.update_yaxes(title_text='Experiments frequency')
        fig.update_xaxes(title_text='Time')

        return fig

    else:

        # Data segmentation
        plot_data = exp_df[:minutes]

        # Plot definition
        fig = go.Figure(data=[

            go.Bar(name='Exp. 1', x=pd.Series(plot_data.index.values), y=plot_data['Exp 1'],
                   marker={'color': '#15569B'}),

            go.Bar(name='Exp. 2', x=pd.Series(plot_data.index.values), y=plot_data['Exp 2'],
                   marker={'color': '#C22911'})
        ])

        # Plot configurations
        fig.update_layout(barmode='stack', height=500,
                          font_family='Oswald, sans-serif', title_text='<b>Experiment frequency for APT<b>')
        fig['layout']['title']['font'] = dict(size=19)
        fig.update_yaxes(title_text='Experiments frequency')
        fig.update_xaxes(title_text='Time')

        return fig

# ============================= Theoretical spread plot vs real spread ==================================== #

### Function definition
def plot_teo_spread(spread_data:pd.DataFrame):

    """
        Line charts for Roll model testing. It can be for theoretical spread, bid and ask comparison with real
        observed data

        Parameters
        ----------

        spread_data: DataFrame (default:None) --> Required parameter
            Principal input data, correspond to a data frame with the definition of theoretical spread, bid and ask,
            it has to follow the next structure:

            'Time': Datetime data frame index, defined for each orderbook
            'bid_size': Bid volume (top of the book)
            'bid': Bid price in USD (top of the book)
            'ask': Ask price in USD (top of the book)
            'ask_size': Ask volume (top of the book)
            'mid_price': Mid-price in USD for each orderbook
            'real_spread': Real observed spread between bid and ask (top of the book)
            'theoretical_spread': Calculated spread with Roll model definition
            'spread_diff': Difference between real and theoretical spread
            'theoretical_bid': Calculated bid with Roll model definition (Mid-price - Theoretical spread)
            'theoretical_ask': Calculated ask with Roll model definition (Mid-price + Theoretical spread)

        Returns
        -------

        fig_spread: Figure
            Plotly figure containing a line chart where it's compared theoretical vs real spread

        fig_diff: Figure
            Plotly figure containing a bar chart where it's compared the difference between theoretical and
            real spread

        fig_bid: Figure
            Plotly figure containing a line chart where it's compared theoretical vs real bid

        fig_ask: Figure
            Plotly figure containing a line chart where it's compared theoretical vs real ask

        fig_theo: Figure
            Plotly figure containing a line chart where it's compared all theoretical metrics

        fig_real: Figure
            Plotly figure containing a line chart where it's compared all observed metrics

        References
        ----------

        [1] https://plotly.com/python/line-charts/
        """

    # -- Figure and plot definition for theoretical spreads -- #

    fig_spread = go.Figure(data=[

        go.Scatter(name='Real Spread', x=spread_data.index.values, y=spread_data['real_spread'],
                   mode='lines', marker={'color': '#B2B641'}),

        go.Scatter(name='Theoretical Spread', x=spread_data.index.values, y=spread_data['theoretical_spread'],
                   mode='lines', marker={'color': '#4785C2'})
    ])

    # Plot configuration
    fig_spread.update_layout(height=500, font_family='Oswald, sans-serif',
                             title_text='<b>Theoretical vs Real Spread<b>')
    fig_spread['layout']['title']['font'] = dict(size=19)
    fig_spread.update_yaxes(title_text='Spread')
    fig_spread.update_xaxes(title_text='Time')

    # -- Figure and plot definition for theoretical spreads differences -- #

    fig_diff = go.Figure(data=[

        go.Bar(name='Diff Spreads', x=spread_data.index.values, y=spread_data['spread_diff'],
               marker=np.where(spread_data['spread_diff']<0, '#C22911', '#15569B'))
    ])

    # Plot configuration
    fig_diff.update_layout(barmode='stack', height=500,
                           font_family='Oswald, sans-serif', title_text='<b>Theoretical vs Real Spread Diff<b>')
    fig_diff['layout']['title']['font'] = dict(size=19)
    fig_diff.update_yaxes(title_text='Spreads difference')
    fig_diff.update_xaxes(title_text='Time')

    # -- Figure and plot definition for theoretical and real bid -- #

    fig_bid = go.Figure(data=[

        go.Scatter(name='Real Bid', x=spread_data.index.values, y=spread_data['bid'],
                   mode='lines', marker={'color': '#B2B641'}),

        go.Scatter(name='Theoretical Bid', x=spread_data.index.values, y=spread_data['theoretical_bid'],
                   mode='lines', marker={'color': '#4785C2'}),

        go.Scatter(name='Mid-Price', x=spread_data.index.values, y=spread_data['mid_price'],
                   mode='lines', marker={'color': '#000000'})
    ])

    # Plot configuration
    fig_bid.update_layout(height=500, font_family='Oswald, sans-serif',
                          title_text='<b>Theoretical vs Real Bid<b>')
    fig_bid['layout']['title']['font'] = dict(size=19)
    fig_bid.update_yaxes(title_text='Bid price')
    fig_bid.update_xaxes(title_text='Time')

    # -- Figure and plot definition for theoretical and real ask -- #

    fig_ask = go.Figure(data=[

        go.Scatter(name='Real Ask', x=spread_data.index.values, y=spread_data['ask'],
                   mode='lines', marker={'color': '#B2B641'}),

        go.Scatter(name='Theoretical Ask', x=spread_data.index.values, y=spread_data['theoretical_ask'],
                   mode='lines', marker={'color': '#4785C2'}),

        go.Scatter(name='Mid-Price', x=spread_data.index.values, y=spread_data['mid_price'],
                   mode='lines', marker={'color': '#000000'})
    ])

    # Plot configuration
    fig_ask.update_layout(height=500, font_family='Oswald, sans-serif',
                          title_text='<b>Theoretical vs Real Ask<b>')
    fig_ask['layout']['title']['font'] = dict(size=19)
    fig_ask.update_yaxes(title_text='Ask price')
    fig_ask.update_xaxes(title_text='Time')

    # -- Figure and plot definition for theoretical metrics -- #

    fig_theo = go.Figure(data=[

        go.Scatter(name='Theoretical Bid', x=spread_data.index.values, y=spread_data['theoretical_bid'],
                   mode='lines', marker={'color': '#B2B641'}),

        go.Scatter(name='Theoretical Ask', x=spread_data.index.values, y=spread_data['theoretical_ask'],
                   mode='lines', marker={'color': '#4785C2'}),

        go.Scatter(name='Mid-Price', x=spread_data.index.values, y=spread_data['mid_price'],
                   mode='lines', marker={'color': '#000000'})
    ])

    # Plot configuration
    fig_theo.update_layout(height=500, font_family='Oswald, sans-serif',
                           title_text='<b>Theoretical values with Roll model<b>')
    fig_theo['layout']['title']['font'] = dict(size=19)
    fig_theo.update_yaxes(title_text='Theoretical prices')
    fig_theo.update_xaxes(title_text='Time')

    # -- Figure and plot definition for real metrics -- #

    fig_real = go.Figure(data=[

        go.Scatter(name='Real Bid', x=spread_data.index.values, y=spread_data['bid'],
                   mode='lines', marker={'color': '#B2B641'}),

        go.Scatter(name='Real Ask', x=spread_data.index.values, y=spread_data['ask'],
                   mode='lines', marker={'color': '#4785C2'}),

        go.Scatter(name='Mid-Price', x=spread_data.index.values, y=spread_data['mid_price'],
                   mode='lines', marker={'color': '#000000'})
    ])

    # Plot configuration
    fig_real.update_layout(height=500, font_family='Oswald, sans-serif',
                           title_text='<b>Real observed metrics<b>')
    fig_real['layout']['title']['font'] = dict(size=19)
    fig_real.update_yaxes(title_text='Real prices')
    fig_real.update_xaxes(title_text='Time')

    # -- Return data definition -- #
    r_data = {'spread': fig_spread, 'diff': fig_diff, 'bid': fig_bid, 'ask': fig_ask,
              'theo': fig_theo, 'real': fig_real}

    return r_data

# ============================== Probability evolution in orders plot ===================================== #

### Function definition
def plot_prob_evo(pt_data:pd.DataFrame):

    """
        Line chart to describe the evolution of probability between orders and their changes. The goal of this
        plot is to show in the probability of occurrence converge to a specific value

        Parameters
        ----------

        pt_data: DataFrame (default:None) --> Required parameter
            Public trades data frame, it has to follow the next structure:

            'timestamp': First column, correspond to the timestamp associated to each registered trade
            'price': USD price at which the transaction was made
            'amount': Traded volume at a specific price and timestamp
            'side': Traded order direction (sell or buy)
            'prob_sell': Probability evolution of sell orders
            'prob_buy': Probability evolution of buy orders
            'direction': -1 if there is a sell order and 1 for buy order

        Returns
        -------

        fig: Figure
            Plotly figure containing a line chart showing the probability convergence between orders

        References
        ----------

        [1] https://plotly.com/python/line-charts/
        """

    # -- Figure definition for probability evolution -- #
    fig = go.Figure(data=[

        go.Scatter(name='Sell', x=pt_data['timestamp'], y=pt_data['prob_sell']*100,
                   mode='lines', marker={'color': '#B68D2F'}),

        go.Scatter(name='Buy', x=pt_data['timestamp'], y=pt_data['prob_buy']*100,
                   mode='lines', marker={'color': '#434BC7'}),

        go.Scatter(name='Convergence', x=pt_data['timestamp'], y=[50]*len(pt_data),
                   mode='lines', marker={'color': '#000000'})
    ])

    # Plot configuration
    fig.update_layout(height=500, font_family='Oswald, sans-serif',
                      title_text='<b>Probability Evolution Between Orders<b>')
    fig['layout']['title']['font'] = dict(size=19)
    fig.update_yaxes(title_text='Probability evolution in %')
    fig.update_xaxes(title_text='Time')

    # -- Return figure -- #
    return fig