
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
def plot_stacked_bar(exp_df,
                     minutes=None):

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