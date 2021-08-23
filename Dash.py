# Librerías

import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# Base de usuarios
users = pd.read_csv (r'C:\Users\Juliana Forero\Desktop\Prueba Coink, Dash plotly\users.csv')

# Base de transacciones
transactions = pd.read_csv (r'C:\Users\Juliana Forero\Desktop\Prueba Coink, Dash plotly\transactions.csv')

# inner join (merge) de las 2 tablas
users_trans = pd.merge(users,transactions,on='user_id')

users_trans.info()

# Faltantes
def missings(x):
            a = x.isna().sum()
            b = 100*x.isna().mean()
            c = pd.Series({"Missings": a,"%Missings": b})
            return(c)

users_trans.apply(missings)

# Summary de las variables numéricas
users_trans.describe()

# Para ver si hay duplicados
pd.merge(users,transactions.drop_duplicates(),how='inner',on='user_id')

# Se grafica la distribucion conjunta de las 2 variables numéricas del dataset
sns.pairplot(users_trans[["money_user_balance_value", "balance_historic_transaction_value"]], diag_kind="kde")



# Se toma solo la parte de la fecha de creación y se omite la hora 
users_trans['fecha_creación'] = pd.to_datetime(users_trans['user_createddate']).dt.date

# Se vuelven de tipo fecha

users_trans['user_createddate'] = pd.to_datetime(users_trans['user_createddate'], format="%Y-%m-%d %H:%M:%S")
users_trans['balance_historic_transaction_date'] = pd.to_datetime(users_trans['balance_historic_transaction_date'], 
                                                                  format="%Y-%m-%d %H:%M:%S")

# Se crean nuevas variables de fecha
users_trans['year_new']= users_trans['user_createddate'].dt.year
users_trans['month_new']= users_trans['user_createddate'].dt.month
users_trans['day_new']= users_trans['user_createddate'].dt.day
users_trans['year_transaction']= users_trans['balance_historic_transaction_date'].dt.year
users_trans['month_transaction']= users_trans['balance_historic_transaction_date'].dt.month
users_trans['day_transaction']= users_trans['balance_historic_transaction_date'].dt.day

# Se muestran los niveles de la variable categórica 'year_new' para saber el rango de años que toma
list(users_trans['year_new'].value_counts().index)

# Gráficos

# Punto 1

users_trans_1 = users_trans.query("year_new=='2019'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["fecha_creación"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("fecha_creación")["user_id"].agg(sum),
    text=users_trans_1.groupby("fecha_creación")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["fecha_creación"].sort_values().unique(),
    y=users_trans_2.groupby("fecha_creación")["user_id"].agg(sum),
    text=users_trans_2.groupby("fecha_creación")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["fecha_creación"].sort_values().unique(),
    y=users_trans_3.groupby("fecha_creación")["user_id"].agg(sum),
    text=users_trans_3.groupby("fecha_creación")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios años 2019-2021") #define how to display the columns
fig1 = go.Figure(data=data, layout=layout)
fig1.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Fecha",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig1.update_traces(texttemplate="%{text:.2s}") #text formart

# Enero
users_trans_1 = users_trans.query("year_new=='2019'" and "month_new =='1'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["day_new"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'" and "month_new =='1'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["day_new"].sort_values().unique(),
    y=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'" and "month_new =='1'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["day_new"].sort_values().unique(),
    y=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios por día del mes de Enero, años 2019-2021") #define how to display the columns
fig2 = go.Figure(data=data, layout=layout)
fig2.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Día del mes",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig2.update_traces(texttemplate="%{text:.2s}") #text formart

# Febrero
users_trans_1 = users_trans.query("year_new=='2019'" and "month_new =='2'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["day_new"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'" and "month_new =='2'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["day_new"].sort_values().unique(),
    y=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'" and "month_new =='2'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["day_new"].sort_values().unique(),
    y=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios por día del mes de Febrero, años 2019-2021") #define how to display the columns
fig3 = go.Figure(data=data, layout=layout)
fig3.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Día del mes",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig3.update_traces(texttemplate="%{text:.2s}") #text formart

# Marzo
users_trans_1 = users_trans.query("year_new=='2019'" and "month_new =='3'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["day_new"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'" and "month_new =='3'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["day_new"].sort_values().unique(),
    y=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'" and "month_new =='3'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["day_new"].sort_values().unique(),
    y=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios por día del mes de Marzo, años 2019-2021") #define how to display the columns
fig4 = go.Figure(data=data, layout=layout)
fig4.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Día del mes",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig4.update_traces(texttemplate="%{text:.2s}") #text formart

# Abril
users_trans_1 = users_trans.query("year_new=='2019'" and "month_new =='4'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["day_new"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'" and "month_new =='4'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["day_new"].sort_values().unique(),
    y=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'" and "month_new =='4'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["day_new"].sort_values().unique(),
    y=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios por día del mes de Abril, años 2019-2021") #define how to display the columns
fig5 = go.Figure(data=data, layout=layout)
fig5.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Día del mes",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig5.update_traces(texttemplate="%{text:.2s}") #text formart

# Mayo
users_trans_1 = users_trans.query("year_new=='2019'" and "month_new =='5'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["day_new"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'" and "month_new =='5'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["day_new"].sort_values().unique(),
    y=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'" and "month_new =='5'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["day_new"].sort_values().unique(),
    y=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios por día del mes de Mayo, años 2019-2021") #define how to display the columns
fig6 = go.Figure(data=data, layout=layout)
fig6.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Día del mes",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig6.update_traces(texttemplate="%{text:.2s}") #text formart

# Junio
users_trans_1 = users_trans.query("year_new=='2019'" and "month_new =='6'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["day_new"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'" and "month_new =='6'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["day_new"].sort_values().unique(),
    y=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'" and "month_new =='6'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["day_new"].sort_values().unique(),
    y=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios por día del mes de Junio, años 2019-2021") #define how to display the columns
fig7 = go.Figure(data=data, layout=layout)
fig7.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Día del mes",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig7.update_traces(texttemplate="%{text:.2s}") #text formart

# Julio
users_trans_1 = users_trans.query("year_new=='2019'" and "month_new =='7'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["day_new"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'" and "month_new =='7'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["day_new"].sort_values().unique(),
    y=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'" and "month_new =='7'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["day_new"].sort_values().unique(),
    y=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios por día del mes de Julio, años 2019-2021") #define how to display the columns
fig8 = go.Figure(data=data, layout=layout)
fig8.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Día del mes",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig8.update_traces(texttemplate="%{text:.2s}") #text formart

# Agosto
users_trans_1 = users_trans.query("year_new=='2019'" and "month_new =='8'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["day_new"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'" and "month_new =='8'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["day_new"].sort_values().unique(),
    y=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'" and "month_new =='8'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["day_new"].sort_values().unique(),
    y=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios por día del mes de Agosto, años 2019-2021") #define how to display the columns
fig9 = go.Figure(data=data, layout=layout)
fig9.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Día del mes",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig9.update_traces(texttemplate="%{text:.2s}") #text formart

# Septiembre
users_trans_1 = users_trans.query("year_new=='2019'" and "month_new =='9'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["day_new"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'" and "month_new =='9'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["day_new"].sort_values().unique(),
    y=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'" and "month_new =='9'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["day_new"].sort_values().unique(),
    y=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios por día del mes de Septiembre, años 2019-2021") #define how to display the columns
fig10 = go.Figure(data=data, layout=layout)
fig10.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Día del mes",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig10.update_traces(texttemplate="%{text:.2s}") #text formart

# Octubre
users_trans_1 = users_trans.query("year_new=='2019'" and "month_new =='10'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["day_new"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'" and "month_new =='10'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["day_new"].sort_values().unique(),
    y=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'" and "month_new =='10'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["day_new"].sort_values().unique(),
    y=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios por día del mes de Octubre, años 2019-2021") #define how to display the columns
fig11 = go.Figure(data=data, layout=layout)
fig11.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Día del mes",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig11.update_traces(texttemplate="%{text:.2s}") #text formart

# Noviembre
users_trans_1 = users_trans.query("year_new=='2019'" and "month_new =='11'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["day_new"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'" and "month_new =='11'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["day_new"].sort_values().unique(),
    y=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'" and "month_new =='11'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["day_new"].sort_values().unique(),
    y=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios por día del mes de Noviembre, años 2019-2021") #define how to display the columns
fig12 = go.Figure(data=data, layout=layout)
fig12.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Día del mes",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig12.update_traces(texttemplate="%{text:.2s}") #text formart

# Diciembre
users_trans_1 = users_trans.query("year_new=='2019'" and "month_new =='12'")

trace1 = go.Bar(   #usuarios diarios
    x=users_trans_1["day_new"].sort_values(ascending=True).unique(),
    y=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_1.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Año 2019",
)

users_trans_2 = users_trans.query("year_new=='2020'" and "month_new =='12'")

trace2 = go.Bar(   #usuarios diarios
    x=users_trans_2["day_new"].sort_values().unique(),
    y=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_2.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Año 2020",
)

users_trans_3 = users_trans.query("year_new=='2021'" and "month_new =='12'")

trace3 = go.Bar(   #usuarios diarios
    x=users_trans_3["day_new"].sort_values().unique(),
    y=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    text=users_trans_3.groupby("day_new")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[2],
    textposition="outside",
    name="Año 2021",
)


data = [trace1,trace2,trace3] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de nuevos usuarios por día del mes de Diciembre, años 2019-2021") #define how to display the columns
fig13 = go.Figure(data=data, layout=layout)
fig13.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Día del mes",#setup the x-axis title
    yaxis_title="Total de nuevos usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig13.update_traces(texttemplate="%{text:.2s}") #text formart

# Se muestran los niveles de la variables dirección y canal de la transacción para saber los valores que toman

list(users_trans['money_transaction_type_direction'].value_counts().index)
list(users_trans['money_transaction_type_description'].value_counts().index)

## Punto 2

users_trans_1 = users_trans.query("money_transaction_type_direction=='cash_in'")
                                  
trace1 = go.Bar(   
    x=users_trans_1["money_transaction_type_description"].unique(),
    y=users_trans_1.groupby("money_transaction_type_description")["balance_historic_transaction_value"].agg(sum),
    text=users_trans_1.groupby("money_transaction_type_description")["balance_historic_transaction_value"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Cash in"
)

users_trans_2 = users_trans.query("money_transaction_type_direction=='cash_out'")

trace2 = go.Bar(   
    x=users_trans_2["money_transaction_type_description"].unique(),
    y=users_trans_2.groupby("money_transaction_type_description")["balance_historic_transaction_value"].agg(sum),
    text=users_trans_2.groupby("money_transaction_type_description")["balance_historic_transaction_value"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[1],
    textposition="outside",
    name="Cash out"
)



data = [trace1,trace2] #combine two charts/columns
layout = go.Layout(barmode="group", title="Monto transado por cada canal según la dirección") #define how to display the columns
fig14 = go.Figure(data=data, layout=layout)
fig14.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Dirección de la transacción",#setup the x-axis title
    yaxis_title="Total monto transacción", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig14.update_traces(texttemplate="%{text:.2s}") #text formart


## Punto 3

users_trans_var = users_trans.groupby(["fecha_creación","user_id", "money_transaction_type_direction"])["money_user_balance_value"].agg("sum").unstack().reset_index()
users_trans_var_1= pd.DataFrame(users_trans_var)
users_trans_var_1

users_trans_var_1['cash_out'] = users_trans_var_1['cash_out'].replace(np.nan, 0)
users_trans_var_1['Ahorro'] = users_trans_var_1['cash_in'] - users_trans_var_1['cash_out']
users_trans_var_1

trace1 = go.Bar(   
    x=users_trans_var_1["fecha_creación"].unique(),
    y=users_trans_var_1.groupby("fecha_creación")["Ahorro"].agg("mean"),
    text=users_trans_var_1.groupby("fecha_creación")["Ahorro"].agg("mean"),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Date"
)



data = [trace1] #combine two charts/columns
layout = go.Layout(barmode="group", title="Variación temporal (diaria) del promedio del monto ahorrado ") #define how to display the columns
fig15 = go.Figure(data=data, layout=layout)
fig15.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Fecha de creación",#setup the x-axis title
    yaxis_title="Promedio del monto ahorrado", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig15.update_traces(texttemplate="%{text:.2s}") #text formart

### Punto 4

# Se muestran los niveles de la variable ecosistema

list(users_trans['ecosystem_name'].value_counts().index)

trace1 = go.Bar(   
    x=users_trans["ecosystem_name"].sort_values(ascending=True).unique(),
    y=users_trans.groupby("ecosystem_name")["user_id"].agg(sum),
    text=users_trans.groupby("ecosystem_name")["user_id"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Ecosistema"
)


data = [trace1] #combine two charts/columns
layout = go.Layout(barmode="group", title="Cantidad de usuarios por ecosistema") #define how to display the columns
fig16 = go.Figure(data=data, layout=layout)
fig16.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Nombre del ecosistema",#setup the x-axis title
    yaxis_title="Cantidad de usuarios", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig16.update_traces(texttemplate="%{text:.2s}") #text formart


### Punto 5

trace1 = go.Bar(   
    x=users_trans["ecosystem_name"].sort_values(ascending=True).unique(),
    y=users_trans.groupby("ecosystem_name")["money_user_balance_value"].agg(sum),
    text=users_trans.groupby("ecosystem_name")["money_user_balance_value"].agg(sum),
    marker_color=px.colors.qualitative.Dark24[0],
    textposition="outside",
    name="Ecosistema"
)


data = [trace1] #combine two charts/columns
layout = go.Layout(barmode="group", title="Total ahorrado por ecosistema") #define how to display the columns
fig17 = go.Figure(data=data, layout=layout)
fig17.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Nombre del ecosistema",#setup the x-axis title
    yaxis_title="Total ahorrado por ecosistema", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig17.update_traces(texttemplate="%{text:.2s}") #text formart


######################## Código para construir el dashboard:

from flask import Flask

app = Flask(__name__)


    

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ]

app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets
) 

#app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("Prueba Data Scientist Coink"),
    html.Div(children='''Report Coink'''),
    dcc.Graph(
        id='example-graph',
        figure={fig1
        })
])

if __name__ == '__main__':
    app.run_server(debug=True)

