from io import BytesIO

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =============================================================================
# CONFIGURACION Y ESTILO
# =============================================================================

st.set_page_config(
    page_title="Politicas publicas | Economia cerrada",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#17283D"
BLUE = "#315F92"
TEAL = "#177B76"
AMBER = "#C28A32"
RED = "#B5525E"
SLATE = "#5E6D78"
PAPER = "#F4F2EC"
WHITE = "#FFFEFB"

st.markdown(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap');

        .stApp {{
            background:
                radial-gradient(circle at 88% 3%, rgba(23,123,118,.095), transparent 28rem),
                radial-gradient(circle at 6% 32%, rgba(194,138,50,.055), transparent 25rem),
                linear-gradient(180deg, #FBFAF6 0%, {PAPER} 100%);
            color: {NAVY};
            font-family: "Manrope", "Segoe UI", sans-serif;
        }}
        [data-testid="stHeader"] {{
            background: rgba(251,250,246,.88);
            border-bottom: 1px solid rgba(23,40,61,.055);
            backdrop-filter: blur(14px);
        }}
        [data-testid="stSidebar"] {{
            background:
                radial-gradient(circle at 20% 5%, rgba(255,255,255,.07), transparent 16rem),
                linear-gradient(165deg, #132439 0%, #19394A 58%, #17504F 100%);
            border-right: 1px solid rgba(255,255,255,.10);
            box-shadow: 12px 0 34px rgba(23,40,61,.08);
        }}
        [data-testid="stSidebar"] * {{ color: #F6F4ED; }}
        [data-testid="stSidebar"] h2 {{
            font-family: "Source Serif 4", Georgia, serif;
            font-size: 1.55rem;
            letter-spacing: -.02em;
        }}
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
            color: rgba(246,244,237,.70) !important;
        }}
        [data-testid="stSidebar"] [data-baseweb="input"],
        [data-testid="stSidebar"] [data-baseweb="input"] > div {{
            background: rgba(255,254,251,.97) !important;
            border-color: rgba(255,255,255,.38) !important;
            border-radius: 11px !important;
        }}
        [data-testid="stSidebar"] [data-baseweb="input"] input {{
            color: {NAVY} !important;
            -webkit-text-fill-color: {NAVY} !important;
            font-weight: 700 !important;
        }}
        [data-testid="stSidebar"] [data-baseweb="input"] button,
        [data-testid="stSidebar"] [data-baseweb="input"] button * {{
            color: {NAVY} !important;
            fill: {NAVY} !important;
        }}
        [data-testid="stSidebar"] details {{
            border: 1px solid rgba(255,255,255,.18);
            border-radius: 15px;
            background: rgba(255,255,255,.055);
            box-shadow: inset 0 1px 0 rgba(255,255,255,.055);
        }}
        [data-testid="stSidebar"] details:hover {{
            background: rgba(255,255,255,.075);
            border-color: rgba(255,255,255,.26);
        }}
        [data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,.14); }}
        h1, h2, h3 {{
            color: {NAVY};
            font-family: "Source Serif 4", Georgia, serif;
            letter-spacing: -.035em;
        }}
        h2 {{ line-height: 1.16; }}
        h3 {{ line-height: 1.22; }}
        p, li, label, button, input {{ font-family: "Manrope", "Segoe UI", sans-serif; }}
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {{
            line-height: 1.68;
        }}
        [data-testid="stCaptionContainer"] {{
            color: #71808B;
            font-size: .89rem;
        }}
        .block-container {{
            max-width: 1480px;
            padding-top: 1.6rem;
            padding-bottom: 4rem;
        }}
        .hero {{
            position: relative;
            overflow: hidden;
            padding: 2.4rem 2.7rem;
            border-radius: 24px;
            background:
                linear-gradient(125deg, rgba(255,255,255,.02), rgba(255,255,255,0)),
                linear-gradient(125deg, #14263C 0%, #21445A 58%, #17645F 100%);
            border: 1px solid rgba(255,255,255,.12);
            box-shadow: 0 24px 65px rgba(23,40,61,.20);
            margin-bottom: 1.25rem;
        }}
        .hero:after {{
            content: "";
            position: absolute;
            width: 330px;
            height: 330px;
            border-radius: 50%;
            right: -95px;
            top: -170px;
            border: 52px solid rgba(255,255,255,.065);
        }}
        .eyebrow {{
            color: #D6B46C;
            font-size: .78rem;
            font-weight: 800;
            letter-spacing: .18em;
            text-transform: uppercase;
            margin-bottom: .7rem;
        }}
        .hero h1 {{
            color: #FFFEFB;
            max-width: 920px;
            font-size: clamp(2rem, 4vw, 3.55rem);
            line-height: 1.08;
            margin: 0 0 .85rem 0;
            text-wrap: balance;
        }}
        .hero p {{
            color: rgba(255,254,251,.78);
            max-width: 850px;
            font-size: 1.04rem;
            line-height: 1.65;
            margin: 0;
        }}
        .section-kicker {{
            color: {TEAL};
            font-size: .77rem;
            font-weight: 800;
            letter-spacing: .17em;
            text-transform: uppercase;
            margin-bottom: -.35rem;
        }}
        .simulation-title {{
            color: {NAVY};
            font-size: clamp(1.35rem, 2.2vw, 1.9rem);
            font-family: "Source Serif 4", Georgia, serif;
            font-weight: 700;
            letter-spacing: -.025em;
            line-height: 1.25;
            margin: 1.8rem 0 1rem 0;
        }}
        .simulation-title span {{
            color: {TEAL};
            font-weight: 700;
        }}
        .info-card, .formula-card, .interpretation-card {{
            background: rgba(255,254,251,.90);
            border: 1px solid #DEDCD4;
            border-radius: 16px;
            padding: 1.15rem 1.25rem;
            box-shadow: 0 11px 30px rgba(23,40,61,.055);
            height: 100%;
        }}
        .formula-card {{
            background: linear-gradient(135deg, #EDF6F3 0%, #FFFEFB 100%);
            border-left: 4px solid {TEAL};
        }}
        .interpretation-card {{
            border-top: 4px solid {AMBER};
            background: linear-gradient(180deg, rgba(255,252,245,.96), rgba(255,254,251,.92));
        }}
        .card-label {{
            color: {SLATE};
            font-size: .72rem;
            font-weight: 800;
            letter-spacing: .12em;
            text-transform: uppercase;
            margin-bottom: .35rem;
        }}
        .card-title {{
            color: {NAVY};
            font-family: "Source Serif 4", Georgia, serif;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: .3rem;
        }}
        .card-copy {{ color: {SLATE}; line-height: 1.55; font-size: .92rem; }}
        [data-testid="stMetric"] {{
            background: rgba(255,254,251,.93);
            border: 1px solid #DEDDD6;
            border-radius: 15px;
            padding: 1rem 1.1rem;
            box-shadow: 0 9px 25px rgba(23,40,61,.052);
            min-height: 126px;
            overflow: visible;
            margin-bottom: .45rem;
            transition: border-color .18s ease, box-shadow .18s ease, transform .18s ease;
        }}
        [data-testid="stMetric"]:hover {{
            border-color: rgba(23,123,118,.30);
            box-shadow: 0 13px 32px rgba(23,40,61,.075);
            transform: translateY(-1px);
        }}
        [data-testid="stMetricLabel"] {{
            color: {SLATE};
            font-weight: 600;
            min-height: 2.6rem;
        }}
        [data-testid="stMetricLabel"] p {{
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
            line-height: 1.25 !important;
            font-size: .88rem !important;
        }}
        [data-testid="stMetricValue"] {{
            color: {NAVY};
            font-weight: 700;
            overflow: visible !important;
        }}
        [data-testid="stMetricValue"] > div {{
            font-size: clamp(1.45rem, 2.25vw, 2.15rem) !important;
            line-height: 1.1 !important;
            white-space: nowrap !important;
            overflow: visible !important;
            text-overflow: clip !important;
            letter-spacing: -.03em;
        }}
        [data-testid="stMetricDelta"] {{
            font-size: .82rem !important;
            white-space: nowrap !important;
        }}
        [data-testid="stHorizontalBlock"] {{
            gap: 1.15rem;
        }}
        [data-baseweb="tab-list"] {{
            gap: .38rem;
            background: rgba(255,254,251,.82);
            border: 1px solid #DEDDD6;
            border-radius: 14px;
            padding: .38rem;
            box-shadow: 0 8px 24px rgba(23,40,61,.045);
        }}
        [data-baseweb="tab"] {{
            border-radius: 10px;
            padding-left: 1rem;
            padding-right: 1rem;
            font-weight: 700;
            color: {SLATE};
            transition: background-color .16s ease, color .16s ease;
        }}
        [aria-selected="true"] {{
            background: #E5F0ED !important;
            color: #125F5C !important;
            box-shadow: inset 0 0 0 1px rgba(23,123,118,.10);
        }}
        [data-baseweb="tab-highlight"] {{
            background-color: {TEAL} !important;
            height: 2px !important;
        }}
        [data-baseweb="tab-border"] {{
            background-color: #DEDDD6 !important;
        }}
        [data-testid="stNumberInput"] input:focus {{
            border-color: {TEAL} !important;
            box-shadow: 0 0 0 2px rgba(23,123,118,.12) !important;
        }}
        .stButton > button, .stDownloadButton > button {{
            border: 0;
            border-radius: 10px;
            background: linear-gradient(135deg, {NAVY}, #1D6662);
            color: #FFFEFB;
            font-weight: 700;
            min-height: 2.8rem;
            box-shadow: 0 9px 20px rgba(23,40,61,.17);
            transition: transform .16s ease, box-shadow .16s ease;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            color: #FFFEFB;
            border: 0;
            transform: translateY(-1px);
            box-shadow: 0 13px 26px rgba(23,40,61,.22);
        }}
        .stDataFrame {{
            border: 1px solid #DEDDD6;
            border-radius: 13px;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(23,40,61,.045);
        }}
        [data-testid="stExpander"] details {{
            background: rgba(255,254,251,.72);
            border-color: #DEDDD6;
            border-radius: 12px;
        }}
        [data-testid="stExpander"] details:hover {{
            border-color: rgba(23,123,118,.26);
        }}
        [data-testid="stPlotlyChart"] {{
            background: rgba(255,254,251,.70);
            border: 1px solid #E2E0D9;
            border-radius: 16px;
            padding: .35rem;
            box-shadow: 0 10px 30px rgba(23,40,61,.045);
        }}
        [data-testid="stAlert"] {{
            border-radius: 12px;
            border-width: 1px;
        }}
        .soft-rule {{ border: 0; border-top: 1px solid #DDDCD5; margin: 1.5rem 0; }}
        .source-note {{
            color: {SLATE};
            font-size: .79rem;
            line-height: 1.5;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# MODELO ECONOMICO
# =============================================================================

def equilibrio(a: float, b: float, c: float, d: float) -> tuple[float, float]:
    """Equilibrio competitivo para Qd = a - bP y Qo = c + dP."""
    precio = (a - c) / (b + d)
    cantidad = a - b * precio
    return precio, cantidad


def excedente_consumidor(a: float, b: float, precio: float, cantidad: float) -> float:
    """Area bajo la demanda y sobre el precio para las primeras `cantidad` unidades."""
    precio_reserva = a / b
    return (precio_reserva - precio) * cantidad - cantidad**2 / (2 * b)


def excedente_productor(c: float, d: float, precio: float, cantidad: float) -> float:
    """Area sobre la oferta y bajo el precio para las primeras `cantidad` unidades."""
    precio_inicio_oferta = -c / d
    return (precio - precio_inicio_oferta) * cantidad - cantidad**2 / (2 * d)


def resultado_subsidio(a: float, b: float, c: float, d: float, subsidio: float) -> dict:
    p0, q0 = equilibrio(a, b, c, d)
    pu = (a - c - d * subsidio) / (b + d)
    po = pu + subsidio
    q1 = a - b * pu

    ec0 = excedente_consumidor(a, b, p0, q0)
    ep0 = excedente_productor(c, d, p0, q0)
    ec1 = excedente_consumidor(a, b, pu, q1)
    ep1 = excedente_productor(c, d, po, q1)
    gasto = subsidio * q1
    bt0 = ec0 + ep0
    bt1 = ec1 + ep1 - gasto

    return {
        "p0": p0,
        "q0": q0,
        "pu": pu,
        "po": po,
        "q1": q1,
        "ec0": ec0,
        "ep0": ep0,
        "ec1": ec1,
        "ep1": ep1,
        "gasto": gasto,
        "resultado_fiscal": -gasto,
        "bt0": bt0,
        "bt1": bt1,
        "delta_bt": bt1 - bt0,
        "delta_q": q1 - q0,
        "beneficio_unitario_usuarios": p0 - pu,
        "beneficio_unitario_empresas": po - p0,
    }


def resultado_precio_maximo(a: float, b: float, c: float, d: float, pmax: float) -> dict:
    p0, q0 = equilibrio(a, b, c, d)
    qd_techo = max(a - b * pmax, 0.0)
    qo_techo = max(c + d * pmax, 0.0)
    vinculante = pmax < p0
    escasez = max(qd_techo - qo_techo, 0.0) if vinculante else 0.0

    if vinculante:
        precio_efectivo = pmax
        q1 = min(qd_techo, qo_techo)
        # Se supone asignacion eficiente: acceden quienes mas valoran la vivienda.
        ec1 = excedente_consumidor(a, b, precio_efectivo, q1)
        ep1 = excedente_productor(c, d, precio_efectivo, q1)
    else:
        precio_efectivo = p0
        q1 = q0
        ec1 = excedente_consumidor(a, b, p0, q0)
        ep1 = excedente_productor(c, d, p0, q0)

    ec0 = excedente_consumidor(a, b, p0, q0)
    ep0 = excedente_productor(c, d, p0, q0)
    bt0 = ec0 + ep0
    bt1 = ec1 + ep1

    return {
        "p0": p0,
        "q0": q0,
        "pmax": pmax,
        "precio_efectivo": precio_efectivo,
        "qd_techo": qd_techo,
        "qo_techo": qo_techo,
        "escasez": escasez,
        "q1": q1,
        "vinculante": vinculante,
        "ec0": ec0,
        "ep0": ep0,
        "ec1": ec1,
        "ep1": ep1,
        "bt0": bt0,
        "bt1": bt1,
        "delta_bt": bt1 - bt0,
        "resultado_fiscal": 0.0,
    }


def numero(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def moneda(valor: float) -> str:
    signo = "-" if valor < 0 else ""
    return f"{signo}$\u00a0{numero(abs(valor))}"


def delta_numero(valor: float) -> str:
    return f"{'+' if valor > 0 else ''}{numero(valor)}"


def delta_moneda(valor: float) -> str:
    return f"{'+' if valor > 0 else ''}{moneda(valor)}"


def cambio_moneda(valor: float) -> str:
    if valor > 1e-8:
        return f"aumenta en {moneda(valor)}"
    if valor < -1e-8:
        return f"disminuye en {moneda(abs(valor))}"
    return "no cambia"


def validar_mercado(a: float, b: float, c: float, d: float) -> tuple[bool, str]:
    if a <= 0 or b <= 0 or d <= 0:
        return False, "Los parametros a, b y d deben ser positivos."
    p, q = equilibrio(a, b, c, d)
    if p < 0 or q < 0:
        return False, "Los parametros elegidos generan un equilibrio negativo. Ajustalos para continuar."
    return True, ""


def dataframe_estilizado(df: pd.DataFrame, formatos: dict | None = None):
    formatos = formatos or {}
    return df.style.format(formatos).set_properties(
        **{"color": NAVY, "font-family": "Manrope, Segoe UI, sans-serif"}
    )


def libro_excel(hojas: dict[str, pd.DataFrame]) -> bytes:
    salida = BytesIO()
    with pd.ExcelWriter(salida, engine="openpyxl") as writer:
        for nombre, df in hojas.items():
            df.to_excel(writer, sheet_name=nombre[:31], index=False)
            hoja = writer.sheets[nombre[:31]]
            hoja.freeze_panes = "A2"
            hoja.auto_filter.ref = hoja.dimensions
            for columna in hoja.columns:
                ancho = max(len(str(celda.value or "")) for celda in columna) + 3
                hoja.column_dimensions[columna[0].column_letter].width = min(ancho, 38)
    return salida.getvalue()


# =============================================================================
# VISUALIZACIONES
# =============================================================================

def estilo_figura(fig: go.Figure, titulo: str, subtitulo: str = "") -> go.Figure:
    fig.update_layout(
        title=dict(
            text=f"<b>{titulo}</b><br><span style='font-size:12px;color:{SLATE}'>{subtitulo}</span>",
            x=0.02,
            y=0.97,
            xanchor="left",
            yanchor="top",
        ),
        font=dict(family="Manrope, Segoe UI, sans-serif", color=NAVY),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=WHITE,
        hoverlabel=dict(bgcolor=WHITE, font_color=NAVY),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.16,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,254,251,.92)",
            bordercolor="#DEDDD6",
            borderwidth=1,
            font=dict(size=11),
        ),
        separators=",.",
        margin=dict(l=45, r=30, t=100, b=115),
        height=600,
    )
    fig.update_xaxes(
        title="Cantidad",
        gridcolor="#E8E6DF",
        zerolinecolor="#C9C7BE",
        rangemode="tozero",
        tickformat=",.0f",
        automargin=True,
    )
    fig.update_yaxes(
        title="Precio",
        gridcolor="#E8E6DF",
        zerolinecolor="#C9C7BE",
        tickformat=",.0f",
        automargin=True,
    )
    return fig


def grafico_subsidio(a: float, b: float, c: float, d: float, r: dict) -> go.Figure:
    q_max = max(a, r["q1"] * 1.18)
    q = np.linspace(0, q_max, 350)
    pdem = (a - q) / b
    pof = (q - c) / d
    pof_sub = pof - (r["po"] - r["pu"])

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=q,
            y=pdem,
            name="Demanda",
            line=dict(color=BLUE, width=3),
            hovertemplate="Cantidad: %{x:,.2f}<br>Precio: %{y:,.2f}<extra>Demanda</extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=q,
            y=pof,
            name="Oferta inicial",
            line=dict(color=TEAL, width=3),
            hovertemplate="Cantidad: %{x:,.2f}<br>Precio: %{y:,.2f}<extra>Oferta inicial</extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=q,
            y=pof_sub,
            name="Oferta percibida con subsidio",
            line=dict(color=AMBER, width=3, dash="dash"),
            hovertemplate="Cantidad: %{x:,.2f}<br>Precio usuarios: %{y:,.2f}<extra>Oferta con subsidio</extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[r["q0"]],
            y=[r["p0"]],
            name="Equilibrio inicial",
            mode="markers",
            marker=dict(color=NAVY, size=12, line=dict(color=WHITE, width=2)),
            hovertemplate="Cantidad: %{x:,.2f}<br>Precio: %{y:,.2f}<extra>Equilibrio inicial</extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[r["q1"], r["q1"]],
            y=[r["pu"], r["po"]],
            name="Equilibrio con subsidio",
            mode="markers+lines",
            line=dict(color=AMBER, width=5),
            marker=dict(color=[BLUE, TEAL], size=12, line=dict(color=WHITE, width=2)),
            hovertemplate="Cantidad: %{x:,.2f}<br>Precio: %{y:,.2f}<extra>Equilibrio con subsidio</extra>",
        )
    )

    fig.add_shape(
        type="rect",
        x0=0,
        x1=r["q1"],
        y0=r["pu"],
        y1=r["po"],
        fillcolor="rgba(194,138,50,.12)",
        line=dict(width=0),
        layer="below",
    )
    fig.add_annotation(
        x=r["q1"] * 0.48,
        y=(r["pu"] + r["po"]) / 2,
        text="Gasto fiscal",
        showarrow=False,
        font=dict(color="#866022", size=12),
    )
    fig.add_annotation(
        x=r["q1"],
        y=r["pu"],
        text=f"Usuarios: {moneda(r['pu'])}",
        showarrow=False,
        xanchor="left",
        xshift=14,
        yshift=-16,
        bgcolor="rgba(255,254,251,.94)",
        bordercolor="#DEDDD6",
        borderpad=4,
        font=dict(color=BLUE, size=11),
    )
    fig.add_annotation(
        x=r["q1"],
        y=r["po"],
        text=f"Empresas: {moneda(r['po'])}",
        showarrow=False,
        xanchor="left",
        xshift=14,
        yshift=16,
        bgcolor="rgba(255,254,251,.94)",
        bordercolor="#DEDDD6",
        borderpad=4,
        font=dict(color=TEAL, size=11),
    )

    y_min = min(0, float(np.min(pof_sub))) * 1.08
    y_max = max(a / b, r["po"]) * 1.08
    fig.update_yaxes(range=[y_min, y_max])
    return estilo_figura(
        fig,
        "Mercado de transporte con subsidio",
        "La brecha vertical representa el subsidio por viaje y el rectangulo, el gasto publico.",
    )


def grafico_precio_maximo(a: float, b: float, c: float, d: float, r: dict) -> go.Figure:
    q_max = max(a, r["qd_techo"], r["q0"]) * 1.05
    q = np.linspace(0, q_max, 350)
    pdem = (a - q) / b
    pof = (q - c) / d

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=q,
            y=pdem,
            name="Demanda",
            line=dict(color=BLUE, width=3),
            hovertemplate="Cantidad: %{x:,.2f}<br>Precio: %{y:,.2f}<extra>Demanda</extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=q,
            y=pof,
            name="Oferta",
            line=dict(color=TEAL, width=3),
            hovertemplate="Cantidad: %{x:,.2f}<br>Precio: %{y:,.2f}<extra>Oferta</extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[r["q0"]],
            y=[r["p0"]],
            name="Equilibrio inicial",
            mode="markers",
            marker=dict(color=NAVY, size=12, line=dict(color=WHITE, width=2)),
            hovertemplate="Cantidad: %{x:,.2f}<br>Precio: %{y:,.2f}<extra>Equilibrio inicial</extra>",
        )
    )
    fig.add_hline(
        y=r["pmax"],
        line_color=RED,
        line_width=2.5,
        line_dash="dash",
        annotation_text=f"Precio maximo: {moneda(r['pmax'])}",
        annotation_position="top left",
    )

    if r["vinculante"]:
        fig.add_trace(
            go.Scatter(
                x=[r["qo_techo"], r["qd_techo"]],
                y=[r["pmax"], r["pmax"]],
                name="Escasez",
                mode="markers+lines",
                line=dict(color=RED, width=6),
                marker=dict(color=RED, size=10, line=dict(color=WHITE, width=2)),
                hovertemplate="Cantidad: %{x:,.2f}<br>Precio maximo: %{y:,.2f}<extra>Escasez</extra>",
            )
        )
        q_dwl = np.linspace(r["q1"], r["q0"], 80)
        fig.add_trace(
            go.Scatter(
                x=np.concatenate([q_dwl, q_dwl[::-1]]),
                y=np.concatenate([(a - q_dwl) / b, ((q_dwl - c) / d)[::-1]]),
                fill="toself",
                fillcolor="rgba(181,82,94,.16)",
                line=dict(color="rgba(0,0,0,0)"),
                name="Perdida de bienestar",
                hoverinfo="skip",
            )
        )
    else:
        fig.add_annotation(
            x=r["q0"],
            y=r["pmax"],
            text="Techo no vinculante: el mercado permanece en el equilibrio inicial",
            showarrow=True,
            arrowcolor=RED,
            bgcolor=WHITE,
            bordercolor="#DEDDD6",
            font=dict(color=NAVY, size=11),
        )

    y_min = min(0, float(np.min(pof))) * 1.05
    y_max = max(a / b, r["pmax"]) * 1.08
    fig.update_yaxes(range=[y_min, y_max])
    return estilo_figura(
        fig,
        "Mercado de alquileres con precio maximo",
        "Cuando el techo es vinculante, la distancia roja muestra la escasez.",
    )


def grafico_bienestar(etiquetas: list[str], inicial: list[float], final: list[float], titulo: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=etiquetas,
            y=inicial,
            name="Antes",
            marker_color="#A9B4B6",
            text=[moneda(x) for x in inicial],
            textposition="outside",
        )
    )
    fig.add_trace(
        go.Bar(
            x=etiquetas,
            y=final,
            name="Despues",
            marker_color=[BLUE, TEAL, AMBER][: len(final)],
            text=[moneda(x) for x in final],
            textposition="outside",
        )
    )
    fig.update_layout(
        barmode="group",
        yaxis_title="Pesos",
        xaxis_title="",
        height=430,
        margin=dict(l=20, r=20, t=90, b=25),
    )
    fig.update_yaxes(gridcolor="#E8E6DF")
    return estilo_figura(fig, titulo, "Comparacion de excedentes y bienestar neto.")


def grafico_simulacion_subsidios(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["Subsidio"],
            y=df["Cantidad de equilibrio"],
            name="Cantidad",
            mode="lines+markers",
            line=dict(color=TEAL, width=3),
            marker=dict(size=9),
            yaxis="y",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["Subsidio"],
            y=df["Gasto publico"],
            name="Gasto publico",
            mode="lines+markers",
            line=dict(color=AMBER, width=3),
            marker=dict(size=9),
            yaxis="y2",
        )
    )
    fig.update_layout(
        yaxis=dict(title="Cantidad", gridcolor="#E8E6DF"),
        yaxis2=dict(title="Gasto publico", overlaying="y", side="right", showgrid=False),
        xaxis=dict(title="Subsidio por viaje", gridcolor="#E8E6DF"),
        height=455,
    )
    return estilo_figura(
        fig,
        "Respuesta a distintos subsidios",
        "Un subsidio mayor eleva la cantidad, pero tambien incrementa el costo fiscal.",
    )


def grafico_simulacion_precios(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["Precio maximo"],
            y=df["Cantidad demandada al techo"],
            name="Cantidad demandada",
            mode="lines+markers",
            line=dict(color=BLUE, width=3),
            marker=dict(size=9),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["Precio maximo"],
            y=df["Cantidad ofrecida al techo"],
            name="Cantidad ofrecida",
            mode="lines+markers",
            line=dict(color=TEAL, width=3),
            marker=dict(size=9),
        )
    )
    fig.add_trace(
        go.Bar(
            x=df["Precio maximo"],
            y=df["Escasez"],
            name="Escasez",
            marker_color="rgba(181,82,94,.34)",
        )
    )
    fig.update_layout(
        xaxis=dict(title="Precio maximo", autorange="reversed", gridcolor="#E8E6DF"),
        yaxis=dict(title="Cantidad", gridcolor="#E8E6DF"),
        height=455,
    )
    return estilo_figura(
        fig,
        "Escasez ante distintos precios maximos",
        "El eje se ordena de mayor a menor para mostrar el efecto de reducir el techo.",
    )


# =============================================================================
# COMPONENTES DE INTERFAZ
# =============================================================================

def titulo_seccion(kicker: str, titulo: str, texto: str):
    st.markdown(f"<div class='section-kicker'>{kicker}</div>", unsafe_allow_html=True)
    st.subheader(titulo)
    st.caption(texto)


def tarjeta(etiqueta: str, titulo: str, texto: str, clase: str = "info-card"):
    st.markdown(
        f"""
        <div class="{clase}">
            <div class="card-label">{etiqueta}</div>
            <div class="card-title">{titulo}</div>
            <div class="card-copy">{texto}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def parametros_sidebar():
    st.sidebar.markdown("## Panel de simulacion")
    st.sidebar.caption(
        "Cada cambio recalcula inmediatamente precios, cantidades, excedentes, graficos, tablas y exportacion."
    )
    st.sidebar.markdown("---")

    with st.sidebar.expander("Ejercicio 1 · Transporte subsidiado", expanded=True):
        st.caption("Edita el mercado y el subsidio del Ejercicio 1.")
        sub_a = st.number_input(
            "a · Intercepto de demanda",
            min_value=1.0,
            value=1500.0,
            step=50.0,
            key="sub_a",
        )
        sub_b = st.number_input(
            "b · Pendiente de demanda",
            min_value=0.01,
            value=25.0,
            step=1.0,
            key="sub_b",
        )
        sub_c = st.number_input(
            "c · Intercepto de oferta",
            value=0.0,
            step=10.0,
            key="sub_c",
        )
        sub_d = st.number_input(
            "d · Pendiente de oferta",
            min_value=0.01,
            value=15.0,
            step=1.0,
            key="sub_d",
        )
        sub_politica = st.number_input(
            "Subsidio por viaje",
            min_value=0.0,
            value=8.0,
            step=1.0,
            key="sub_politica",
        )

    with st.sidebar.expander("Ejercicio 2 · Alquileres", expanded=False):
        st.caption("Edita el mercado y el precio maximo del Ejercicio 2.")
        pm_a = st.number_input(
            "a · Intercepto de demanda",
            min_value=1.0,
            value=1800.0,
            step=50.0,
            key="pm_a",
        )
        pm_b = st.number_input(
            "b · Pendiente de demanda",
            min_value=0.01,
            value=20.0,
            step=1.0,
            key="pm_b",
        )
        pm_c = st.number_input(
            "c · Intercepto de oferta",
            value=0.0,
            step=10.0,
            key="pm_c",
        )
        pm_d = st.number_input(
            "d · Pendiente de oferta",
            min_value=0.01,
            value=12.0,
            step=1.0,
            key="pm_d",
        )
        pm_politica = st.number_input(
            "Precio maximo",
            min_value=0.0,
            value=40.0,
            step=1.0,
            key="pm_politica",
        )

    st.sidebar.markdown("---")
    st.sidebar.caption(
        "Valores predeterminados: consignas del TP. Todos los campos son editables y recalculan la aplicacion."
    )
    return (
        {"a": sub_a, "b": sub_b, "c": sub_c, "d": sub_d, "politica": sub_politica},
        {"a": pm_a, "b": pm_b, "c": pm_c, "d": pm_d, "politica": pm_politica},
    )


# =============================================================================
# PORTADA Y DATOS
# =============================================================================

sub_params, pm_params = parametros_sidebar()

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">UNSTA · Economia para Ingenieros · Trabajo Practico N.° 2</div>
        <h1>Politicas publicas bajo economia cerrada</h1>
        <p>Una herramienta interactiva para medir como los subsidios y los controles de precios
        transforman el equilibrio, distribuyen beneficios y costos, y modifican el bienestar social.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_a, col_b, col_c = st.columns([1.3, 1, 1])
with col_a:
    tarjeta(
        "Equipo",
        "Amparo Ruiz · Candelaria Lopez Avila · Luz Maria Ponce de Leon",
        "Analisis economico, simulacion computacional e interpretacion de resultados.",
    )
with col_b:
    tarjeta(
        "Modelo",
        "Economia cerrada",
        "Mercados competitivos con funciones lineales de oferta y demanda.",
    )
with col_c:
    tarjeta(
        "Intervenciones",
        "Subsidio y precio maximo",
        "Dos politicas publicas evaluadas desde la eficiencia y la distribucion.",
    )

st.markdown("<hr class='soft-rule'>", unsafe_allow_html=True)

tab_inicio, tab_subsidio, tab_precio, tab_simulacion = st.tabs(
    [
        "Panorama",
        "Subsidios",
        "Precios Maximos",
        "Simulaciones",
    ]
)

sub_ok, sub_error = validar_mercado(sub_params["a"], sub_params["b"], sub_params["c"], sub_params["d"])
pm_ok, pm_error = validar_mercado(pm_params["a"], pm_params["b"], pm_params["c"], pm_params["d"])

sub_r = (
    resultado_subsidio(
        sub_params["a"], sub_params["b"], sub_params["c"], sub_params["d"], sub_params["politica"]
    )
    if sub_ok
    else None
)
pm_r = (
    resultado_precio_maximo(
        pm_params["a"], pm_params["b"], pm_params["c"], pm_params["d"], pm_params["politica"]
    )
    if pm_ok
    else None
)


# =============================================================================
# PANORAMA
# =============================================================================

with tab_inicio:
    titulo_seccion(
        "Lectura general",
        "El Estado cambia resultados y tambien incentivos",
        "La aplicacion permite identificar ganadores, perdedores, costo fiscal y eficiencia.",
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        tarjeta(
            "Pregunta 01",
            "¿Quien recibe el beneficio?",
            "Una politica puede favorecer a mas de un grupo. La incidencia depende de las pendientes de oferta y demanda.",
            "interpretation-card",
        )
    with c2:
        tarjeta(
            "Pregunta 02",
            "¿Quien financia el costo?",
            "En un subsidio aparece un gasto fiscal explicito. En un precio maximo, el costo surge como menor oferta y escasez.",
            "interpretation-card",
        )
    with c3:
        tarjeta(
            "Pregunta 03",
            "¿Cambia el bienestar total?",
            "Sin externalidades ni fallas adicionales, ambas intervenciones pueden generar intercambios ineficientes.",
            "interpretation-card",
        )

    st.markdown("<hr class='soft-rule'>", unsafe_allow_html=True)
    titulo_seccion(
        "Objetivo del proyecto",
        "Del modelo teorico a una herramienta de decision",
        "El TP combina economia e informatica para simular intervenciones publicas en mercados cerrados.",
    )
    l, rcol = st.columns([1.05, 1])
    with l:
        st.markdown(
            """
            La aplicacion automatiza el recorrido completo solicitado:

            - ingreso de los parametros `a`, `b`, `c` y `d`;
            - calculo de equilibrio, excedentes y bienestar inicial;
            - evaluacion posterior a la politica publica;
            - resultado fiscal, escasez y variacion de bienestar;
            - visualizacion de curvas, situaciones y areas relevantes;
            - simulaciones obligatorias, interpretacion y exportacion.
            """
        )
    with rcol:
        tarjeta(
            "Criterio economico",
            "Bienestar social",
            "Se define como excedente del consumidor + excedente del productor - gasto publico. "
            "En el precio maximo no existe gasto fiscal directo. Los resultados suponen asignacion eficiente "
            "de las unidades disponibles.",
            "formula-card",
        )


# =============================================================================
# EJERCICIO 1: SUBSIDIO
# =============================================================================

with tab_subsidio:
    titulo_seccion(
        "Ejercicio 01",
        "Subsidio al transporte publico",
        "El Gobierno busca reducir el precio que pagan los usuarios mediante un subsidio por viaje.",
    )

    st.markdown(
        f"""
        <div class="formula-card">
            <div class="card-label">Mercado configurado</div>
            <div class="card-title">Qd = {numero(sub_params['a'])} - {numero(sub_params['b'])} Pd &nbsp;&nbsp;·&nbsp;&nbsp;
            Qo = {numero(sub_params['c'])} + {numero(sub_params['d'])} Po</div>
            <div class="card-copy">Subsidio por unidad: <b>{moneda(sub_params['politica'])}</b>. La diferencia entre
            el precio recibido por la empresa y el pagado por el usuario es exactamente el subsidio.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not sub_ok:
        st.error(sub_error)
    else:
        st.markdown("### Situacion inicial")
        i1, i2, i3 = st.columns(3)
        i1.metric("Precio de equilibrio", moneda(sub_r["p0"]))
        i2.metric("Cantidad de equilibrio", numero(sub_r["q0"]))
        i3.metric("Excedente consumidor", moneda(sub_r["ec0"]))
        i4, i5 = st.columns(2)
        i4.metric("Excedente productor", moneda(sub_r["ep0"]))
        i5.metric("Bienestar total", moneda(sub_r["bt0"]))

        st.markdown("### Situacion posterior a la intervencion")
        k1, k2, k3 = st.columns(3)
        k1.metric("Precio usuarios", moneda(sub_r["pu"]), delta=delta_moneda(sub_r["pu"] - sub_r["p0"]))
        k2.metric("Precio empresas", moneda(sub_r["po"]), delta=delta_moneda(sub_r["po"] - sub_r["p0"]))
        k3.metric("Nueva cantidad", numero(sub_r["q1"]), delta=delta_numero(sub_r["delta_q"]))
        k4, k5, k6 = st.columns(3)
        k4.metric("Gasto publico", moneda(sub_r["gasto"]))
        k5.metric("Resultado fiscal", moneda(sub_r["resultado_fiscal"]))
        k6.metric("Variacion bienestar", moneda(sub_r["delta_bt"]), delta=delta_moneda(sub_r["delta_bt"]))

        st.plotly_chart(
            grafico_subsidio(sub_params["a"], sub_params["b"], sub_params["c"], sub_params["d"], sub_r),
            width="stretch",
            config={"displayModeBar": False},
        )

        titulo_seccion(
            "Impacto por actor",
            "Quienes ganan, quienes financian y que ocurre con la sociedad",
            "La incidencia se actualiza automaticamente con cada parametro ingresado.",
        )
        actor_1, actor_2 = st.columns(2)
        with actor_1:
            tarjeta(
                "Consumidores",
                f"Su excedente {cambio_moneda(sub_r['ec1'] - sub_r['ec0'])}",
                f"Pagan {moneda(sub_r['beneficio_unitario_usuarios'])} menos por viaje y demandan una cantidad mayor.",
            )
        with actor_2:
            tarjeta(
                "Productores",
                f"Su excedente {cambio_moneda(sub_r['ep1'] - sub_r['ep0'])}",
                f"Reciben {moneda(sub_r['beneficio_unitario_empresas'])} mas por viaje y ofrecen una cantidad mayor.",
            )
        actor_3, actor_4 = st.columns(2)
        with actor_3:
            tarjeta(
                "Gobierno y contribuyentes",
                f"Resultado fiscal: {moneda(sub_r['resultado_fiscal'])}",
                f"El subsidio exige financiar un gasto publico total de {moneda(sub_r['gasto'])}.",
            )
        with actor_4:
            tarjeta(
                "Sociedad en su conjunto",
                f"El bienestar {cambio_moneda(sub_r['delta_bt'])}",
                "El analisis neto suma los excedentes de consumidores y productores y descuenta el gasto publico.",
            )

        titulo_seccion(
            "Distribucion",
            "Excedentes y bienestar social",
            "El bienestar final descuenta el gasto que debe financiar el Gobierno.",
        )
        m1, m2 = st.columns(2)
        m1.metric("Excedente consumidor · antes", moneda(sub_r["ec0"]))
        m2.metric(
            "Excedente consumidor · despues",
            moneda(sub_r["ec1"]),
            delta=delta_moneda(sub_r["ec1"] - sub_r["ec0"]),
        )
        m3, m4 = st.columns(2)
        m3.metric("Excedente productor · antes", moneda(sub_r["ep0"]))
        m4.metric(
            "Excedente productor · despues",
            moneda(sub_r["ep1"]),
            delta=delta_moneda(sub_r["ep1"] - sub_r["ep0"]),
        )

        b1, b2, b3 = st.columns(3)
        b1.metric("Bienestar inicial", moneda(sub_r["bt0"]))
        b2.metric("Bienestar final neto", moneda(sub_r["bt1"]))
        b3.metric(
            "Variacion del bienestar",
            moneda(sub_r["delta_bt"]),
            delta=delta_moneda(sub_r["delta_bt"]),
            delta_color="normal",
        )

        izq, der = st.columns([1.25, 1])
        with izq:
            st.plotly_chart(
                grafico_bienestar(
                    ["Consumidor", "Productor", "Bienestar neto"],
                    [sub_r["ec0"], sub_r["ep0"], sub_r["bt0"]],
                    [sub_r["ec1"], sub_r["ep1"], sub_r["bt1"]],
                    "Como se distribuye el efecto",
                ),
                width="stretch",
                config={"displayModeBar": False},
            )
        with der:
            if sub_r["delta_bt"] < -1e-8:
                st.warning(
                    f"La politica reduce el bienestar total en {moneda(abs(sub_r['delta_bt']))}. "
                    "La perdida surge porque se realizan viajes cuyo costo marginal supera su beneficio marginal."
                )
            elif sub_r["delta_bt"] > 1e-8:
                st.success(f"La politica aumenta el bienestar total en {moneda(sub_r['delta_bt'])}.")
            else:
                st.info("Sin subsidio, el bienestar no cambia.")

            st.markdown(
                f"""
                <div class="interpretation-card">
                    <div class="card-label">Interpretacion solicitada</div>
                    <div class="card-title">¿El subsidio ayuda a la gente?</div>
                    <div class="card-copy">
                    <b>Beneficiados:</b> los usuarios pagan {moneda(sub_r['beneficio_unitario_usuarios'])} menos
                    por viaje y las empresas reciben {moneda(sub_r['beneficio_unitario_empresas'])} mas por viaje
                    respecto del equilibrio inicial.<br><br>
                    <b>Quienes pagan:</b> el Gobierno desembolsa {moneda(sub_r['gasto'])}; en ultima instancia,
                    ese gasto se financia con impuestos presentes o futuros de los contribuyentes.<br><br>
                    <b>Conclusion:</b> la politica redistribuye recursos y aumenta el uso del transporte, pero
                    bajo este modelo sin externalidades positivas reduce el bienestar social neto.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        resumen_sub = pd.DataFrame(
            {
                "Indicador": [
                    "Precio de equilibrio inicial",
                    "Cantidad de equilibrio inicial",
                    "Precio pagado por usuarios",
                    "Precio recibido por empresas",
                    "Cantidad luego del subsidio",
                    "Excedente consumidor inicial",
                    "Excedente consumidor final",
                    "Excedente productor inicial",
                    "Excedente productor final",
                    "Gasto total del Gobierno",
                    "Resultado fiscal",
                    "Bienestar inicial",
                    "Bienestar final neto",
                    "Variacion del bienestar social",
                ],
                "Valor": [
                    sub_r["p0"],
                    sub_r["q0"],
                    sub_r["pu"],
                    sub_r["po"],
                    sub_r["q1"],
                    sub_r["ec0"],
                    sub_r["ec1"],
                    sub_r["ep0"],
                    sub_r["ep1"],
                    sub_r["gasto"],
                    sub_r["resultado_fiscal"],
                    sub_r["bt0"],
                    sub_r["bt1"],
                    sub_r["delta_bt"],
                ],
            }
        )
        with st.expander("Ver tabla completa del ejercicio"):
            st.dataframe(
                dataframe_estilizado(resumen_sub, {"Valor": numero}),
                width="stretch",
                hide_index=True,
            )


# =============================================================================
# EJERCICIO 2: PRECIO MAXIMO
# =============================================================================

with tab_precio:
    titulo_seccion(
        "Ejercicio 02",
        "Precio maximo a los alquileres",
        "El Gobierno busca facilitar el acceso a la vivienda fijando un techo al precio.",
    )

    st.markdown(
        f"""
        <div class="formula-card">
            <div class="card-label">Mercado configurado</div>
            <div class="card-title">Qd = {numero(pm_params['a'])} - {numero(pm_params['b'])} P &nbsp;&nbsp;·&nbsp;&nbsp;
            Qo = {numero(pm_params['c'])} + {numero(pm_params['d'])} P</div>
            <div class="card-copy">Precio maximo: <b>{moneda(pm_params['politica'])}</b>.
            Un techo solo modifica el mercado cuando queda por debajo del precio de equilibrio.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not pm_ok:
        st.error(pm_error)
    else:
        st.markdown("### Situacion inicial")
        i1, i2, i3 = st.columns(3)
        i1.metric("Precio de equilibrio", moneda(pm_r["p0"]))
        i2.metric("Cantidad de equilibrio", numero(pm_r["q0"]))
        i3.metric("Excedente consumidor", moneda(pm_r["ec0"]))
        i4, i5 = st.columns(2)
        i4.metric("Excedente productor", moneda(pm_r["ep0"]))
        i5.metric("Bienestar total", moneda(pm_r["bt0"]))

        st.markdown("### Situacion posterior a la intervencion")
        k1, k2, k3 = st.columns(3)
        k1.metric("Precio efectivo", moneda(pm_r["precio_efectivo"]))
        k2.metric("Cantidad transada", numero(pm_r["q1"]))
        k3.metric("Cantidad demandada al techo", numero(pm_r["qd_techo"]))
        k4, k5, k6 = st.columns(3)
        k4.metric("Cantidad ofrecida al techo", numero(pm_r["qo_techo"]))
        k5.metric("Escasez", numero(pm_r["escasez"]))
        k6.metric("Resultado fiscal directo", moneda(pm_r["resultado_fiscal"]))

        if pm_r["vinculante"]:
            st.warning(
                f"El precio maximo es vinculante: queda {moneda(pm_r['p0'] - pm_r['pmax'])} "
                "por debajo del precio de equilibrio."
            )
        else:
            st.info(
                "El precio maximo no es vinculante. Aunque se muestran oferta y demanda evaluadas al techo, "
                "el mercado sigue operando en el equilibrio inicial."
            )

        st.plotly_chart(
            grafico_precio_maximo(pm_params["a"], pm_params["b"], pm_params["c"], pm_params["d"], pm_r),
            width="stretch",
            config={"displayModeBar": False},
        )

        titulo_seccion(
            "Impacto por actor",
            "Quienes ganan, quienes pierden y que ocurre con la sociedad",
            "El resultado distingue entre los inquilinos que acceden y quienes quedan excluidos por la escasez.",
        )
        actor_1, actor_2 = st.columns(2)
        with actor_1:
            tarjeta(
                "Consumidores",
                f"Su excedente {cambio_moneda(pm_r['ec1'] - pm_r['ec0'])}",
                "Quienes consiguen una vivienda pagan menos; cuando el techo es vinculante, otros demandantes quedan excluidos.",
            )
        with actor_2:
            tarjeta(
                "Productores",
                f"Su excedente {cambio_moneda(pm_r['ep1'] - pm_r['ep0'])}",
                f"Al precio efectivo ofrecen {numero(pm_r['q1'])} unidades, frente a {numero(pm_r['q0'])} en el equilibrio inicial.",
            )
        actor_3, actor_4 = st.columns(2)
        with actor_3:
            tarjeta(
                "Gobierno",
                f"Resultado fiscal directo: {moneda(pm_r['resultado_fiscal'])}",
                "El control no exige un pago fiscal directo, aunque su administracion y fiscalizacion pueden tener costos no modelados.",
            )
        with actor_4:
            tarjeta(
                "Sociedad en su conjunto",
                f"El bienestar {cambio_moneda(pm_r['delta_bt'])}",
                f"La politica genera una escasez de {numero(pm_r['escasez'])} unidades cuando el techo es vinculante.",
            )

        titulo_seccion(
            "Distribucion",
            "Excedentes y bienestar social",
            "Con un techo vinculante se transa la cantidad ofrecida; se supone que las unidades van a quienes mas las valoran.",
        )
        m1, m2 = st.columns(2)
        m1.metric("Excedente consumidor · antes", moneda(pm_r["ec0"]))
        m2.metric(
            "Excedente consumidor · despues",
            moneda(pm_r["ec1"]),
            delta=delta_moneda(pm_r["ec1"] - pm_r["ec0"]),
        )
        m3, m4 = st.columns(2)
        m3.metric("Excedente productor · antes", moneda(pm_r["ep0"]))
        m4.metric(
            "Excedente productor · despues",
            moneda(pm_r["ep1"]),
            delta=delta_moneda(pm_r["ep1"] - pm_r["ep0"]),
        )

        b1, b2, b3 = st.columns(3)
        b1.metric("Bienestar inicial", moneda(pm_r["bt0"]))
        b2.metric("Bienestar final", moneda(pm_r["bt1"]))
        b3.metric(
            "Variacion del bienestar",
            moneda(pm_r["delta_bt"]),
            delta=delta_moneda(pm_r["delta_bt"]),
            delta_color="normal",
        )

        izq, der = st.columns([1.25, 1])
        with izq:
            st.plotly_chart(
                grafico_bienestar(
                    ["Consumidor", "Productor", "Bienestar total"],
                    [pm_r["ec0"], pm_r["ep0"], pm_r["bt0"]],
                    [pm_r["ec1"], pm_r["ep1"], pm_r["bt1"]],
                    "Como se distribuye el efecto",
                ),
                width="stretch",
                config={"displayModeBar": False},
            )
        with der:
            if pm_r["vinculante"]:
                st.error(
                    f"Se genera una escasez de {numero(pm_r['escasez'])} unidades y una perdida de bienestar "
                    f"de {moneda(abs(pm_r['delta_bt']))}."
                )
            else:
                st.success("El techo no altera el precio, la cantidad ni el bienestar.")

            st.markdown(
                f"""
                <div class="interpretation-card">
                    <div class="card-label">Interpretacion solicitada</div>
                    <div class="card-title">¿La politica resuelve el problema habitacional?</div>
                    <div class="card-copy">
                    <b>Quienes ganan:</b> si el techo es vinculante, los inquilinos que consiguen una vivienda
                    pagan un precio menor.<br><br>
                    <b>Quienes pierden:</b> los propietarios reciben menos y ofrecen menos viviendas; tambien
                    pierden quienes demandan una unidad pero quedan excluidos por la escasez.<br><br>
                    <b>Conclusion:</b> el control mejora la accesibilidad para un grupo, pero no aumenta la
                    cantidad disponible. En este modelo, genera escasez y no resuelve por si solo el problema
                    habitacional.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        resumen_pm = pd.DataFrame(
            {
                "Indicador": [
                    "Precio de equilibrio",
                    "Cantidad de equilibrio",
                    "Precio maximo",
                    "Cantidad demandada al precio maximo",
                    "Cantidad ofrecida al precio maximo",
                    "Escasez generada",
                    "Cantidad efectivamente transada",
                    "Resultado fiscal directo",
                    "Excedente consumidor antes",
                    "Excedente consumidor despues",
                    "Excedente productor antes",
                    "Excedente productor despues",
                    "Bienestar inicial",
                    "Bienestar final",
                    "Variacion del bienestar social",
                ],
                "Valor": [
                    pm_r["p0"],
                    pm_r["q0"],
                    pm_r["pmax"],
                    pm_r["qd_techo"],
                    pm_r["qo_techo"],
                    pm_r["escasez"],
                    pm_r["q1"],
                    pm_r["resultado_fiscal"],
                    pm_r["ec0"],
                    pm_r["ec1"],
                    pm_r["ep0"],
                    pm_r["ep1"],
                    pm_r["bt0"],
                    pm_r["bt1"],
                    pm_r["delta_bt"],
                ],
            }
        )
        with st.expander("Ver tabla completa del ejercicio"):
            st.dataframe(
                dataframe_estilizado(resumen_pm, {"Valor": numero}),
                width="stretch",
                hide_index=True,
            )


# =============================================================================
# SIMULACIONES OBLIGATORIAS Y EXPORTACION
# =============================================================================

filas_sub = []
if sub_ok:
    for s in [0, 5, 10, 15, 20]:
        r = resultado_subsidio(sub_params["a"], sub_params["b"], sub_params["c"], sub_params["d"], s)
        filas_sub.append(
            {
                "Subsidio": s,
                "Precio usuarios": r["pu"],
                "Precio empresas": r["po"],
                "Cantidad de equilibrio": r["q1"],
                "Gasto publico": r["gasto"],
                "Bienestar total": r["bt1"],
                "Variacion de bienestar": r["delta_bt"],
            }
        )
df_sim_sub = pd.DataFrame(filas_sub)

filas_pm = []
if pm_ok:
    for pmax in [70, 60, 50, 40, 30]:
        r = resultado_precio_maximo(pm_params["a"], pm_params["b"], pm_params["c"], pm_params["d"], pmax)
        filas_pm.append(
            {
                "Precio maximo": pmax,
                "Cantidad demandada al techo": r["qd_techo"],
                "Cantidad ofrecida al techo": r["qo_techo"],
                "Escasez": r["escasez"],
                "Cantidad transada": r["q1"],
                "Techo vinculante": "Si" if r["vinculante"] else "No",
                "Bienestar total": r["bt1"],
                "Variacion de bienestar": r["delta_bt"],
            }
        )
df_sim_pm = pd.DataFrame(filas_pm)

with tab_simulacion:
    titulo_seccion(
        "Escenarios obligatorios",
        "Comparar para entender",
        "Las tablas reproducen exactamente los niveles de politica solicitados por el TP y usan los parametros configurados.",
    )

    st.markdown(
        """
        <div class="simulation-title">
            Subsidios simulados: <span>$ 0 · $ 5 · $ 10 · $ 15 · $ 20</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if sub_ok:
        st.dataframe(
            dataframe_estilizado(
                df_sim_sub,
                {
                    "Subsidio": moneda,
                    "Precio usuarios": moneda,
                    "Precio empresas": moneda,
                    "Cantidad de equilibrio": numero,
                    "Gasto publico": moneda,
                    "Bienestar total": moneda,
                    "Variacion de bienestar": moneda,
                },
            ),
            width="stretch",
            hide_index=True,
        )
        st.plotly_chart(grafico_simulacion_subsidios(df_sim_sub), width="stretch", config={"displayModeBar": False})
        primer_sub = df_sim_sub.iloc[0]
        ultimo_sub = df_sim_sub.iloc[-1]
        st.markdown(
            f"""
            <div class="interpretation-card">
                <div class="card-label">Lectura de la simulacion</div>
                <div class="card-title">Mas subsidio implica mas viajes y un costo fiscal creciente</div>
                <div class="card-copy">Al pasar de un subsidio de {moneda(primer_sub['Subsidio'])} a
                {moneda(ultimo_sub['Subsidio'])}, la cantidad aumenta de
                <b>{numero(primer_sub['Cantidad de equilibrio'])}</b> a
                <b>{numero(ultimo_sub['Cantidad de equilibrio'])}</b>. El gasto publico alcanza
                <b>{moneda(ultimo_sub['Gasto publico'])}</b> y el bienestar neto cambia en
                <b>{moneda(ultimo_sub['Variacion de bienestar'])}</b>.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error(sub_error)

    st.markdown("<hr class='soft-rule'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="simulation-title">
            Precios maximos simulados: <span>$ 70 · $ 60 · $ 50 · $ 40 · $ 30</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if pm_ok:
        st.dataframe(
            dataframe_estilizado(
                df_sim_pm,
                {
                    "Precio maximo": moneda,
                    "Cantidad demandada al techo": numero,
                    "Cantidad ofrecida al techo": numero,
                    "Escasez": numero,
                    "Cantidad transada": numero,
                    "Bienestar total": moneda,
                    "Variacion de bienestar": moneda,
                },
            ),
            width="stretch",
            hide_index=True,
        )
        st.plotly_chart(grafico_simulacion_precios(df_sim_pm), width="stretch", config={"displayModeBar": False})
        esc_70 = float(df_sim_pm.loc[df_sim_pm["Precio maximo"] == 70, "Escasez"].iloc[0])
        esc_30 = float(df_sim_pm.loc[df_sim_pm["Precio maximo"] == 30, "Escasez"].iloc[0])
        st.markdown(
            f"""
            <div class="interpretation-card">
                <div class="card-label">Lectura de la simulacion</div>
                <div class="card-title">La escasez crece cuando el precio maximo disminuye</div>
                <div class="card-copy">Con un techo de {moneda(70)}, la escasez es
                <b>{numero(esc_70)}</b>; al reducirlo a {moneda(30)}, asciende a
                <b>{numero(esc_30)}</b>. El precio menor eleva la cantidad demandada y, al mismo tiempo,
                reduce la cantidad que los propietarios desean ofrecer.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error(pm_error)

    if sub_ok and pm_ok:
        hojas = {
            "Resumen subsidio": resumen_sub,
            "Simulacion subsidios": df_sim_sub,
            "Resumen precio maximo": resumen_pm,
            "Simulacion precios": df_sim_pm,
        }
        st.download_button(
            "Descargar resultados completos en Excel",
            data=libro_excel(hojas),
            file_name="TP2_politicas_publicas_resultados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch",
        )


st.markdown("<hr class='soft-rule'>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="source-note">
        Modelo desarrollado para el Trabajo Practico N.° 2 · Economia para Ingenieros · UNSTA.<br>
        Los resultados representan un modelo simplificado y deben interpretarse junto con sus supuestos.
    </div>
    """,
    unsafe_allow_html=True,
)
