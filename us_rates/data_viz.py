####################################
# DATA VIZ - CREATE CHARTS
####################################
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def line_yield_curve(df):
    '''
    Plot line chart of yield curve with animation, monthly
    '''
    df_rev = df.iloc[:, ::-1]
    tabular_df = pd.melt(df_rev.reset_index(), id_vars='DATE', value_vars=df_rev.columns, var_name='Maturity', value_name='Yield')
    tabular_df['DATE'] = tabular_df['DATE'].dt.strftime('%Y-%m')

    fig = px.line(tabular_df,
              x='Maturity',
              y='Yield',
              animation_frame='DATE',
              animation_group='Maturity',
              range_y=[0,7],
              markers='*',
              text=tabular_df.Yield,

             )
    fig.update_traces(mode='markers+text',
                  textposition='top center',
                  textfont=dict(
                                family='Arial',
                                size=14,
        )
    )
    fig.update_layout(title='Yield Curve Replay',
                  title_font=dict(size = 20),
                  autosize=True,
                  #width=1200,
                  height=500,
                  )
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 100

    #fig.show(animation=dict(fromcurrent=True,mode='immediate'))

    # Auto-play animation
    #plotly.offline.plot(fig, auto_play = True)

    return fig



def surface_3d(df):
    '''
    3d surface plot - History of Yield Curve on a monthly basis from 1m to 30Y rates
    '''

    fig = go.Figure(data=[go.Surface(x=df.columns,
                                    y=df.index,
                                    z=df.values,
                                    opacity=0.9,
                                    connectgaps=True,
                                    colorscale='rdbu',
                                    showscale=True,
                                    reversescale=True,
                                    )
                        ]
                )

    fig.update_layout(title='Historical Yield Curve Evolution',
                        title_font=dict(size = 20),
                        autosize=True,
                        #width=1600,
                        height=600,
                        hovermode='closest',
                        scene = {"aspectratio": {"x": 1, "y": 2.2, "z": 1},
                                'camera': {'eye':{'x': 2, 'y':0.4, 'z': 0.8}},
                                'xaxis_title':'Term',
                              'yaxis_title':'Date',
                              'zaxis_title':'Yield in %'
                                },
                        margin=dict(l=0, r=0, b=60, t=40),

                    )

    return fig


def line_spread(df):
    '''
    10-3MY spread over time
    '''
    data = df.copy()
    data['Spread'] = (df['10Y']-df['3M'])*100

    fig = px.area(data,
              x=df.index,
              y='Spread',
              range_y=[-200,400]

             )
    fig.update_xaxes(title=None)

    fig.update_layout(title='10Y-3M Spread in bps',
                  title_font=dict(size = 20),
                  autosize=True,
                  #width=1200,
                  height=500,

                 )
    return fig
