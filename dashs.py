import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import numpy as np

# ===== CHARGEMENT DES DONNÉES =====
try:
    df = pd.read_excel('data_dashboard_large.xlsx')
    df.columns = df.columns.str.strip()
    
    # Conversion de la date
    if 'Date_Transaction' in df.columns:
        df['Date_Transaction'] = pd.to_datetime(df['Date_Transaction'])
    
except FileNotFoundError:
    print("dataset non trouvé")

df['Montant'] = pd.to_numeric(df['Montant'], errors='coerce').fillna(0)

# ===== CALCULS DES KPI GLOBAUX =====
total_ventes = df['Montant'].sum()
nb_transactions = len(df)
montant_moyen = df['Montant'].mean()
satisfaction_moyenne = df['Satisfaction_Client'].mean()

# Ventes quotidiennes
df['Date'] = df['Date_Transaction'].dt.date
ventes_quotidiennes = df.groupby('Date')['Montant'].sum().reset_index()

# ===== CRÉATION DE L'APPLICATION DASH =====
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    # En-tête
    dbc.Row([
        dbc.Col([
            html.H1("🏪 Dashboard Interactif - Analyse des Ventes", 
                   className="text-center mb-2 mt-4",
                   style={'color': '#2c3e50'}),
            html.P("Vue d'ensemble des performances de la chaîne de magasins", 
                  className="text-center text-muted mb-4")
        ])
    ]),
    
    # Filtres dynamiques
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("🔍 Filtres", className="mb-3"),
                    html.Label("Magasin:", className="fw-bold"),
                    dcc.Dropdown(
                        id='filtre-magasin',
                        options=[{'label': 'Tous', 'value': 'Tous'}] + 
                                [{'label': m, 'value': m} for m in df['Magasin'].unique()],
                        value='Tous',
                        clearable=False,
                        className="mb-3"
                    ),
                    html.Label("Catégorie:", className="fw-bold"),
                    dcc.Dropdown(
                        id='filtre-categorie',
                        options=[{'label': 'Toutes', 'value': 'Toutes'}] + 
                                [{'label': c, 'value': c} for c in df['Categorie_Produit'].unique()],
                        value='Toutes',
                        clearable=False,
                        className="mb-3"
                    ),
                    html.Label("Mode de paiement:", className="fw-bold"),
                    dcc.Dropdown(
                        id='filtre-paiement',
                        options=[{'label': 'Tous', 'value': 'Tous'}] + 
                                [{'label': p, 'value': p} for p in df['Mode_Paiement'].unique()],
                        value='Tous',
                        clearable=False
                    )
                ])
            ], className="shadow-sm")
        ], width=12, md=3),
        
        # KPI Cards
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("💰 Total des Ventes", className="card-subtitle mb-2 text-muted"),
                            html.H3(id='kpi-total', className="card-title text-success mb-0")
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, lg=3),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("🛒 Transactions", className="card-subtitle mb-2 text-muted"),
                            html.H3(id='kpi-transactions', className="card-title text-primary mb-0")
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, lg=3),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("📊 Montant Moyen", className="card-subtitle mb-2 text-muted"),
                            html.H3(id='kpi-moyen', className="card-title text-info mb-0")
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, lg=3),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("⭐ Satisfaction", className="card-subtitle mb-2 text-muted"),
                            html.H3(id='kpi-satisfaction', className="card-title text-warning mb-0")
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, lg=3)
            ])
        ], width=12, md=9)
    ], className="mb-4"),
    
    # Section 1: Ventes quotidiennes
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📈 Évolution des Ventes Quotidiennes", className="mb-3"),
                    dcc.Graph(id='graph-quotidien')
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),
    
    # Section 2: Analyse par magasin
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🏬 Répartition par Magasin", className="mb-3"),
                    dcc.Graph(id='graph-magasin-pie')
                ])
            ], className="shadow-sm")
        ], width=12, md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📊 Montant Moyen par Magasin", className="mb-3"),
                    dcc.Graph(id='graph-magasin-bar')
                ])
            ], className="shadow-sm")
        ], width=12, md=6)
    ], className="mb-4"),
    
    # Section 3: Analyse des catégories
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📦 Quantités Vendues par Catégorie", className="mb-3"),
                    dcc.Graph(id='graph-quantite-categorie')
                ])
            ], className="shadow-sm")
        ], width=12, md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("💵 Ventes par Catégorie et Magasin", className="mb-3"),
                    dcc.Graph(id='graph-categorie-magasin')
                ])
            ], className="shadow-sm")
        ], width=12, md=6)
    ], className="mb-4"),
    
    # Section 4 & 5: Paiement et Satisfaction
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("💳 Modes de Paiement", className="mb-3"),
                    dcc.Graph(id='graph-paiement'),
                    html.Hr(),
                    html.H6("Mode le plus utilisé:", className="text-muted"),
                    html.H4(id='mode-populaire', className="text-primary")
                ])
            ], className="shadow-sm")
        ], width=12, md=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("⭐ Satisfaction par Magasin", className="mb-3"),
                    dcc.Graph(id='graph-satisfaction-magasin')
                ])
            ], className="shadow-sm")
        ], width=12, md=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📊 Distribution Satisfaction", className="mb-3"),
                    dcc.Graph(id='graph-satisfaction-distribution')
                ])
            ], className="shadow-sm")
        ], width=12, md=4)
    ])
    
], fluid=True, style={"backgroundColor": "#f8f9fa", "paddingBottom": "30px"})

# ===== CALLBACKS POUR L'INTERACTIVITÉ =====

@app.callback(
    [Output('kpi-total', 'children'),
     Output('kpi-transactions', 'children'),
     Output('kpi-moyen', 'children'),
     Output('kpi-satisfaction', 'children'),
     Output('graph-quotidien', 'figure'),
     Output('graph-magasin-pie', 'figure'),
     Output('graph-magasin-bar', 'figure'),
     Output('graph-quantite-categorie', 'figure'),
     Output('graph-categorie-magasin', 'figure'),
     Output('graph-paiement', 'figure'),
     Output('mode-populaire', 'children'),
     Output('graph-satisfaction-magasin', 'figure'),
     Output('graph-satisfaction-distribution', 'figure')],
    [Input('filtre-magasin', 'value'),
     Input('filtre-categorie', 'value'),
     Input('filtre-paiement', 'value')]
)
def update_dashboard(magasin, categorie, paiement):
    # Filtrage des données
    dff = df.copy()
    if magasin != 'Tous':
        dff = dff[dff['Magasin'] == magasin]
    if categorie != 'Toutes':
        dff = dff[dff['Categorie_Produit'] == categorie]
    if paiement != 'Tous':
        dff = dff[dff['Mode_Paiement'] == paiement]
    
    # KPI
    total = f"{dff['Montant'].sum():,.0f} €"
    nb_trans = f"{len(dff):,}"
    moyen = f"{dff['Montant'].mean():.2f} €"
    satisf = f"{dff['Satisfaction_Client'].mean():.2f} / 5"
    
    # Graph 1: Ventes quotidiennes
    ventes_jour = dff.groupby('Date')['Montant'].sum().reset_index()
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=ventes_jour['Date'], 
        y=ventes_jour['Montant'],
        mode='lines+markers',
        line=dict(color='#3498db', width=3),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.2)'
    ))
    fig1.update_layout(
        xaxis_title="Date",
        yaxis_title="Ventes (€)",
        hovermode='x unified',
        height=300
    )
    
    # Graph 2: Pie Chart Magasins
    ventes_magasin = dff.groupby('Magasin')['Montant'].sum()
    fig2 = go.Figure(data=[go.Pie(
        labels=ventes_magasin.index,
        values=ventes_magasin.values,
        hole=0.4,
        marker_colors=px.colors.qualitative.Set3
    )])
    fig2.update_layout(height=300)
    
    # Graph 3: Bar Chart Montant moyen par magasin
    moyen_magasin = dff.groupby('Magasin')['Montant'].mean().sort_values(ascending=True)
    fig3 = go.Figure(data=[go.Bar(
        x=moyen_magasin.values,
        y=moyen_magasin.index,
        orientation='h',
        marker_color='#9b59b6',
        text=moyen_magasin.values.round(2),
        textposition='auto'
    )])
    fig3.update_layout(
        xaxis_title="Montant Moyen (€)",
        yaxis_title="Magasin",
        height=300
    )
    
    # Graph 4: Quantités par catégorie
    quantite_cat = dff.groupby('Categorie_Produit')['Quantite'].sum().sort_values(ascending=False)
    fig4 = go.Figure(data=[go.Bar(
        x=quantite_cat.index,
        y=quantite_cat.values,
        marker_color=['#e74c3c', '#f39c12', '#2ecc71'],
        text=quantite_cat.values,
        textposition='auto'
    )])
    fig4.update_layout(
        xaxis_title="Catégorie",
        yaxis_title="Quantité Totale",
        height=300
    )
    
    # Graph 5: Ventes empilées par catégorie et magasin
    ventes_cat_mag = dff.groupby(['Magasin', 'Categorie_Produit'])['Montant'].sum().reset_index()
    fig5 = px.bar(
        ventes_cat_mag,
        x='Magasin',
        y='Montant',
        color='Categorie_Produit',
        title='',
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig5.update_layout(
        xaxis_title="Magasin",
        yaxis_title="Montant (€)",
        height=300,
        legend_title_text='Catégorie'
    )
    
    # Graph 6: Modes de paiement
    paiement_count = dff['Mode_Paiement'].value_counts()
    fig6 = go.Figure(data=[go.Pie(
        labels=paiement_count.index,
        values=paiement_count.values,
        hole=0.3,
        marker_colors=px.colors.qualitative.Safe
    )])
    fig6.update_layout(height=250, showlegend=True)
    
    mode_pop = paiement_count.index[0] if len(paiement_count) > 0 else "N/A"
    
    # Graph 7: Satisfaction par magasin
    satisf_magasin = dff.groupby('Magasin')['Satisfaction_Client'].mean().sort_values(ascending=True)
    fig7 = go.Figure(data=[go.Bar(
        x=satisf_magasin.values,
        y=satisf_magasin.index,
        orientation='h',
        marker_color='#f39c12',
        text=satisf_magasin.values.round(2),
        textposition='auto'
    )])
    fig7.update_layout(
        xaxis_title="Score Moyen",
        yaxis_title="Magasin",
        height=250,
        xaxis=dict(range=[0, 5])
    )
    
    # Graph 8: Distribution satisfaction
    satisf_dist = dff['Satisfaction_Client'].value_counts().sort_index()
    fig8 = go.Figure(data=[go.Bar(
        x=satisf_dist.index,
        y=satisf_dist.values,
        marker_color='#16a085',
        text=satisf_dist.values,
        textposition='auto'
    )])
    fig8.update_layout(
        xaxis_title="Score de Satisfaction",
        yaxis_title="Nombre de Clients",
        height=250,
        xaxis=dict(tickmode='linear', tick0=1, dtick=1)
    )
    
    return (total, nb_trans, moyen, satisf, 
            fig1, fig2, fig3, fig4, fig5, fig6, mode_pop, fig7, fig8)

if __name__ == '__main__':
    app.run(debug=True, port=8050)