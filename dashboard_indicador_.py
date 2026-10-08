import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Indicador 7", layout="wide")
st.title(" Dashboard – Indicador 7")

arquivo = st.sidebar.file_uploader("Carregar CSV (data, categoria, valor)", type="csv")

@st.cache_data
def dados_exemplo():
    rng = np.random.default_rng(7)
    datas = pd.date_range("2025-01-01", periods=12, freq="MS")
    linhas = []
    for cat in ["A", "B", "C"]:
        base = rng.uniform(60, 90)
        for d in datas:
            linhas.append({"data": d, "categoria": cat,
                           "valor": base + rng.normal(0, 5)})
    return pd.DataFrame(linhas)

if arquivo:
    df = pd.read_csv(arquivo, parse_dates=["data"])
else:
    df = dados_exemplo()

cats = st.sidebar.multiselect("Categoria", sorted(df["categoria"].unique()),
                              default=sorted(df["categoria"].unique()))
meta = st.sidebar.number_input("Meta", value=75.0)
df = df[df["categoria"].isin(cats)]

if df.empty:
    st.warning("Nenhum dado para os filtros selecionados.")
    st.stop()

serie = df.groupby("data")["valor"].mean()
atual, anterior = serie.iloc[-1], serie.iloc[-2] if len(serie) > 1 else serie.iloc[-1]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Valor atual", f"{atual:.1f}", f"{atual - anterior:+.1f}")
c2.metric("Média do período", f"{serie.mean():.1f}")
c3.metric("Máximo", f"{serie.max():.1f}")
c4.metric("% da meta", f"{atual / meta * 100:.0f}%")

col_a, col_b = st.columns((2, 1))

with col_a:
    fig, ax = plt.subplots(figsize=(8, 4))
    for cat, g in df.groupby("categoria"):
        ax.plot(g["data"], g["valor"], marker="o", label=cat)
    ax.axhline(meta, color="red", linestyle="--", label="Meta")
    ax.set_title("Evolução do Indicador 7")
    ax.set_xlabel("Data")
    ax.set_ylabel("Valor")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.autofmt_xdate()
    st.pyplot(fig)

with col_b:
    fig, ax = plt.subplots(figsize=(4, 4))
    media_cat = df.groupby("categoria")["valor"].mean()
    cores = ["tab:green" if v >= meta else "tab:orange" for v in media_cat]
    ax.bar(media_cat.index, media_cat.values, color=cores)
    ax.axhline(meta, color="red", linestyle="--")
    ax.set_title("Média por categoria")
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)

with st.expander("Ver dados"):
    st.dataframe(df, use_container_width=True)
