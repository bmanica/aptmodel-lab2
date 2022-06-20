
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

            go.Bar(name='Exp. 1', x=exp_df['P. Exp 1']*100, y=pd.Series(exp_df.index.values),
                   marker={'color':'#15569B'}, orientation='h'),

            go.Bar(name='Exp. 2', x=exp_df['P. Exp 2']*100, y=pd.Series(exp_df.index.values),
                   marker={'color':'#C22911'}, orientation='h')
        ])

        # Plot configurations
        fig.update_layout(barmode='stack', height=600,
                          font_family='Oswald, sans-serif', title_text='<b>Experiment proportions for APT<b>')
        fig['layout']['title']['font'] = dict(size=19)
        fig.update_yaxes(title_text='Time')
        fig.update_xaxes(title_text='Experiments proportion in %')

        return fig

    else:

        # Data segmentation
        plot_data = exp_df[:minutes]

        # Plot definition
        fig = go.Figure(data=[

            go.Bar(name='Exp. 1', x=plot_data['P. Exp 1']*100, y=pd.Series(plot_data.index.values),
                   marker={'color': '#15569B'}, orientation='h'),

            go.Bar(name='Exp. 2', x=plot_data['P. Exp 2']*100, y=pd.Series(plot_data.index.values),
                   marker={'color': '#C22911'}, orientation='h')
        ])

        # Plot configurations
        fig.update_layout(barmode='stack', height=600,
                          font_family='Oswald, sans-serif', title_text='<b>Experiment proportions for APT<b>')
        fig['layout']['title']['font'] = dict(size=19)
        fig.update_yaxes(title_text='Time')
        fig.update_xaxes(title_text='Experiments proportion in %')

        return fig