from dash import Dash, dcc, html, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def make_fig(n=21):
    x = np.linspace(-2, 2, n)
    y = np.linspace(-2, 2, n)
    X, Y = np.meshgrid(x, y)

    turbo = px.colors.sequential.Turbo
    ncolor = len(turbo)
    ic = int((ncolor -1 ) / 2)
    colorscale = [
        [0.0, turbo[0]],     # blue
        [0.30, turbo[ic-4]],
        [0.40, turbo[ic-3]],
        [0.45, turbo[ic-2]],
        [0.49, turbo[ic-1]],
        [0.50, turbo[ic]],   # center of color (green)
        [0.51, turbo[ic+1]],
        [0.55, turbo[ic+2]],
        [0.60, turbo[ic+3]],
        [0.70, turbo[ic+4]],
        [1.0, turbo[-1]]     # red
    ]    

    # プロット
    def f(x):
        return x**2

    Z = f(X + Y * 1j)
    opacity = 0.5
#    real_surface = go.Surface(x=X, y=Y, z=Z.real, opacity=opacity, colorscale='gray', colorbar=dict(x=1.0, title="Real"))
#    imag_surface = go.Surface(x=X, y=Y, z=Z.imag, opacity=opacity, colorscale='turbo', colorbar=dict(x=1.1, title="Imag"))
    surface = go.Surface(x=X, y=Y, z=Z.real, opacity=1, colorscale=colorscale, colorbar=dict(x=1.1, title="y.imag"),
                              surfacecolor=Z.imag, cmin=Z.imag.min(), cmax=Z.imag.max(),
                              customdata=Z.imag,   # ← C を渡す
                              hovertemplate=
                                  "x.real: %{x:.5g}<br>" +
                                  "x.imag: %{y:.5g}<br>" +
                                  "y.real: %{z:.5g}<br>" +
                                  "y.imag: %{customdata:.5g}<br>" +   # ← C を表示
                                  "<extra></extra>",
                        )
#    fig = go.Figure(data=[real_surface, imag_surface])
    fig = go.Figure(data=[surface])

    fig.update_layout(
        title="y = x², x = x.real + i * x.imag",
        width=800, height=600,
        autosize=False,
        scene = dict(
            camera_eye=dict(x=0, y=-1, z=0.5),
            aspectratio=dict(x=1, y=1, z=1),
            xaxis_title='x.real',
            yaxis_title='x.imag',
            zaxis_title='y.real',
        )
    )
    return fig

npoints = [10, 20, 50, 100, 200]

npoint_slider = dcc.Slider(
    id="npoint-slider",
    min=0,
    max=len(npoints)-1,
    step=1,
    marks={i: f'{v} X {v}' for i, v in enumerate(npoints)},
    value=3,
)

app = Dash(__name__)
server = app.server

fig = make_fig()
plot = dcc.Graph(id='surface-plot', figure=fig)
app.layout = html.Div([
    html.Div([
        html.Div('変数Xの分割数'),
        npoint_slider,
    ], style={"width": "50%"}),
    plot,
])

@callback(
    Output('surface-plot', 'figure'),
    Input('npoint-slider', 'value')
)
def update_npoint_slider(value):
    npoint = npoints[value]
    fig = make_fig(npoint + 1)
    return fig

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8888)  # don't use app.run(...) start jupyterlab and build somthing 
