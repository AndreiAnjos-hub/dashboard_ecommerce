# Dashboard - Ecommerce

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard de Ecommerce", layout="wide")
st.title("📊 Análise de Dados Comportamentais do Consumidor")
st.markdown("Este painel analisa dados de comportamento de consumidores em um ecommerce, abordando público, vendas e tendências.")
st.markdown("---")

df = pd.read_csv('Ecommerce_Consumer_Behavior_Analysis_Data.csv')

df['Valor'] = df.apply(lambda x: float(x["Purchase_Amount"][1:]), axis=1)

# Qual é o público alvo?

st.header("🎯 Público Alvo")
st.markdown("Informações gerais sobre o perfil do consumidor.")

col1, col2, col3 = st.columns(3)

with col1:
    gender_popular = df['Gender'].value_counts().idxmax()
    st.metric("Gênero com maior quantidade", gender_popular)

with col2:
    # Qual é a idade média dos clientes?
    
    idade_media = df["Age"].mean()
    st.metric("Idade Média dos Clientes", f"{int(idade_media)} anos")

with col3:
    classe_social = df['Social_Media_Influence'].value_counts().idxmax()
    st.metric("Classe Social mais comum", classe_social)

st.markdown("---")

st.header("⚖️ Distribuição por Gênero")
tab1, tab2, tab3 = st.tabs(["Quantidade", "Porcentagem", "Idade Média"])

genero_qnt = df['Gender'].value_counts().reset_index()
genero_qnt.columns = ['Gênero', 'Quantidade']

with tab1:
    # quantidade de cada gênero
    
    fig = px.bar(genero_qnt, x='Gênero', y='Quantidade', title="Quantidade por Gênero", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # porcentagem de cada gênero
    
    fig = px.pie(genero_qnt, values='Quantidade', names='Gênero', title="Porcentagem por Gênero")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Qual é a idade média por gênero?
    
    idade_media_genero = df.groupby('Gender')['Age'].mean().reset_index()
    fig = px.bar(
        idade_media_genero,
        x='Gender',
        y='Age',
        title="Idade Média por Gênero",
        labels={"Gender": "Gênero", "Age": "Idade Média"},
        text_auto='.0f'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.header("📅 Análise por Estado Civil e Nível de Renda")
st.markdown("Entendimento da relação entre o nível de renda e estado civil dos consumidores.")

# Quantos solteiros tem?

marital_status_qnt = df['Marital_Status'].value_counts().reset_index()
marital_status_qnt.columns = ['Estado Civil', 'Quantidade']

fig = px.bar(
    marital_status_qnt,
    x='Estado Civil',
    y='Quantidade',
    title="Quantidade por Estado Civil",
    text_auto=True
)
st.plotly_chart(fig, use_container_width=True)

# Qual é a idade média por nível de renda?

df_idade_media = df.groupby("Income_Level")["Age"].mean().reset_index()

fig = px.bar(
    df_idade_media,
    x="Income_Level",
    y="Age",
    title="Idade Média por Nível de Renda",
    labels={"Income_Level": "Nível de Renda", "Age": "Idade Média"},
    color="Income_Level",
    text_auto='.0f'
)
fig.update_layout(
    xaxis={'categoryorder':'total ascending'},
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

# Qual é a proporção de clientes por nível de renda (Baixa, Média, Alta)?

nivel_renda = df['Social_Media_Influence'].value_counts().reset_index()
nivel_renda.columns = ['Nível de Renda', 'Cliente']

fig = px.treemap(
    nivel_renda,
    path=['Nível de Renda'],
    values='Cliente',
    title='Proporção de Clientes por Nível de Influência Social',
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.header("🛒 Comportamento de Compra")
st.markdown("Análise dos métodos de pagamento, categorias de compra e valores médios.")

col1, col2, col3 = st.columns(3)

with col1:
    # Qual é o método de pagamento mais usado?
    
    metodo_pagamento_max = df["Payment_Method"].value_counts().idxmax()
    st.metric("Método de Pagamento mais usado", metodo_pagamento_max)
    
    # Forma de pagamento menos utilizado? 
    
    metodo_pagamento_min = df["Payment_Method"].value_counts().idxmin()
    st.metric("Método de Pagamento menos usado", metodo_pagamento_min)

with col2:
    # Qual é a categoria de produto mais comprada?
    
    categoria_produto = df['Purchase_Category'].value_counts().idxmax()
    st.metric("Categoria de Produto mais Comprada", categoria_produto)
    
    # O valor médio de compra pelo marital status
    
    df_valor_medio_cliente_marital_status = df.groupby("Marital_Status")["Valor"].mean()
    marital_status_maior_valor = df_valor_medio_cliente_marital_status.idxmax()
    valor_medio_marital_status = df_valor_medio_cliente_marital_status.max()
    st.metric(label="Estado Civil com maior Valor Médio de Compra", value=marital_status_maior_valor, delta=f"R${valor_medio_marital_status:.2f}")

with col3:
    # O valor médio de compra é maior para clientes do gênero feminino ou masculino?
    
    df_valor_medio_cliente_genero = df.groupby("Gender")["Valor"].mean()
    genero_maior_valor = df_valor_medio_cliente_genero.idxmax()
    valor_medio_genero = df_valor_medio_cliente_genero.max()
    st.metric(label="Gênero com maior Valor Médio de Compra", value=genero_maior_valor, delta=f"R$ {valor_medio_genero:.2f}")
    
    # Qual é a avaliação média dos produtos?
    
    avaliacao_media = df["Product_Rating"].mean()
    st.metric("Avaliação Média dos Produtos", f"{avaliacao_media:.1f}")

st.markdown("---")

st.header("📦 Frequência e Canais de Compra")
st.markdown("Entendimento dos padrões de frequência e preferência de canais.")

# Qual é o valor médio gasto por compra?

valor_medio_compra = df.groupby('Frequency_of_Purchase')['Valor'].mean().reset_index()

fig = px.bar(
    valor_medio_compra,
    x='Frequency_of_Purchase',
    y='Valor',
    title="Valor Médio Gasto por Frequência de Compra",
    labels={"Frequency_of_Purchase": "Frequência de Compra", "Valor": "Valor Médio (R$)"},
    text_auto='.2f'
)
st.plotly_chart(fig, use_container_width=True)

# Quantas compras foram feitas online vs em loja física?

df_canal_filtrado = df[df["Purchase_Channel"].isin(["Online", "In-Store"])]
df_canal_compra = df_canal_filtrado["Purchase_Channel"].value_counts().reset_index()
df_canal_compra.columns = ['Canal de Compra', 'Quantidade']

fig = px.bar(
    df_canal_compra,
    x="Quantidade",
    y="Canal de Compra",
    orientation='h',
    title="Distribuição de Compras: Online vs Loja Física",
    labels={'Quantidade': 'Número de Compras', 'Canal de Compra': 'Canal'},
    text_auto='.0f'
)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Desenvolvido por Andrei Conrado. 🚀")
