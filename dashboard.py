"""CEO-facing Streamlit decision brief for the Kashe Meta Ads retrospective.

Run from the repository root with:
    streamlit run dashboard.py

The view is deliberately descriptive. It does not infer revenue, ROAS,
chronological trends or causal creative effects that the surviving export
cannot support.
"""
from __future__ import annotations

from html import escape

import matplotlib.pyplot as plt
import streamlit as st

from scripts.dashboard_data import compact_number, load_dashboard_model

INK = "#16324F"
MUTED = "#64748B"
ACCENT = "#D95D39"
TEAL = "#287271"
PALE = "#E8E1D5"
GRID = "#D7DEE5"
WHITE = "#FFFFFF"


def inject_styles() -> None:
    """Apply a restrained, accessible visual system to the Streamlit shell."""
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 92% 3%, rgba(217, 93, 57, 0.10), transparent 24rem),
                linear-gradient(180deg, #F8F5EF 0%, #F3F6F7 100%);
        }
        [data-testid="stMainBlockContainer"] {
            max-width: 1240px;
            padding-top: 1.35rem;
            padding-bottom: 2.5rem;
        }
        html, body, [class*="st-"] {
            font-family: "Trebuchet MS", "Gill Sans", sans-serif;
            color: #16324F;
        }
        h1, h2, h3 {
            font-family: Georgia, "Times New Roman", serif;
            letter-spacing: -0.025em;
            color: #16324F;
        }
        .hero {
            padding: 1.35rem 1.5rem 1.2rem;
            border: 1px solid rgba(22, 50, 79, 0.14);
            border-left: 6px solid #D95D39;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.88);
            box-shadow: 0 10px 28px rgba(22, 50, 79, 0.07);
            margin-bottom: 0.85rem;
        }
        .eyebrow {
            color: #287271;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }
        .hero h1 {
            font-size: clamp(1.8rem, 4vw, 3rem);
            line-height: 1.04;
            margin: 0;
            max-width: 950px;
        }
        .hero p {
            color: #526779;
            font-size: 1.02rem;
            margin: 0.7rem 0 0;
            max-width: 900px;
        }
        .kpi-card {
            min-height: 108px;
            padding: 0.9rem 1rem;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(22, 50, 79, 0.13);
        }
        .kpi-label {
            color: #64748B;
            font-size: 0.78rem;
            font-weight: 750;
            letter-spacing: 0.045em;
            text-transform: uppercase;
        }
        .kpi-value {
            color: #16324F;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 1.85rem;
            font-weight: 700;
            line-height: 1.15;
            margin-top: 0.28rem;
        }
        .kpi-note { color: #64748B; font-size: 0.76rem; margin-top: 0.2rem; }
        .executive-summary {
            margin: 0.95rem 0 0.35rem;
            padding: 1rem 1.1rem 1.1rem;
            border-radius: 12px;
            border: 1px solid rgba(22, 50, 79, 0.14);
            background: rgba(255, 255, 255, 0.92);
            box-shadow: 0 7px 20px rgba(22, 50, 79, 0.05);
        }
        .summary-heading {
            color: #16324F;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 1.18rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.75rem 1rem;
        }
        .summary-item {
            padding: 0.72rem 0.82rem;
            border-radius: 9px;
            background: #F7F8F8;
            border-left: 3px solid #287271;
        }
        .summary-item.action { border-left-color: #D95D39; }
        .summary-label {
            color: #287271;
            font-size: 0.73rem;
            font-weight: 800;
            letter-spacing: 0.055em;
            text-transform: uppercase;
        }
        .summary-item.action .summary-label { color: #B94729; }
        .summary-item p {
            color: #40566A;
            font-size: 0.87rem;
            line-height: 1.43;
            margin: 0.24rem 0 0;
        }
        .action-card {
            min-height: 150px;
            padding: 1rem 1.05rem;
            border-top: 4px solid #287271;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.92);
            box-shadow: 0 5px 16px rgba(22, 50, 79, 0.05);
        }
        .action-number { color: #D95D39; font-weight: 800; font-size: 0.78rem; }
        .action-card h3 { font-size: 1.04rem; margin: 0.2rem 0 0.35rem; }
        .action-card p { color: #526779; font-size: 0.86rem; margin: 0; line-height: 1.45; }
        div[data-baseweb="tab-list"] { gap: 0.4rem; }
        button[data-baseweb="tab"] { font-weight: 700; }
        div[data-testid="stDataFrame"] { border: 1px solid rgba(22, 50, 79, 0.12); }
        .small-note { color: #64748B; font-size: 0.8rem; }
        @media (max-width: 760px) {
            [data-testid="stMainBlockContainer"] { padding: 0.8rem 0.8rem 2rem; }
            .hero { padding: 1rem; }
            .kpi-card, .action-card { min-height: auto; }
            .summary-grid { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, note: str) -> None:
    """Render a KPI with context but without invented targets or trends."""
    st.markdown(
        f"""
        <div class="kpi-card">
          <div class="kpi-label">{escape(label)}</div>
          <div class="kpi-value">{escape(value)}</div>
          <div class="kpi-note">{escape(note)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def concentration_figure(items: list[dict[str, object]]) -> plt.Figure:
    """Compare the top three link rows with the rest of the link portfolio."""
    labels = [str(item["metric"]) for item in items]
    top = [float(item["top_three_pct"]) for item in items]
    remaining = [float(item["remaining_pct"]) for item in items]

    fig, ax = plt.subplots(figsize=(7.2, 3.1))
    positions = range(len(items))
    ax.barh(positions, top, color=ACCENT, height=0.52, label="Top three rows")
    ax.barh(positions, remaining, left=top, color=PALE, height=0.52, label="Remaining rows")
    ax.set_yticks(list(positions), labels=labels, color=INK, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of link-campaign total", color=MUTED, fontsize=9)
    ax.xaxis.set_major_formatter(lambda value, _: f"{value:.0f}%")
    ax.grid(axis="x", color=GRID, linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)
    for index, value in enumerate(top):
        ax.text(
            max(value / 2, 8),
            index,
            f"{value:.1f}%",
            va="center",
            ha="center",
            color=WHITE,
            fontsize=10,
            fontweight="bold",
        )
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
        ncol=2,
        frameon=False,
        fontsize=9,
    )
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    fig.tight_layout()
    return fig


def sensitivity_figure(items: list[dict[str, object]]) -> plt.Figure:
    """Show how the pooled CPC and CTR depend on exceptional response rows."""
    labels = [str(item["scenario"]) for item in items]
    cpc = [float(item["weighted_cpc_ngn"]) for item in items]
    ctr = [float(item["derived_ctr_pct"]) for item in items]
    positions = list(range(len(items)))

    fig, axes = plt.subplots(1, 2, figsize=(8.1, 3.1))
    specifications = [
        (axes[0], cpc, "Weighted CPC", "NGN", ACCENT),
        (axes[1], ctr, "Derived CTR", "%", TEAL),
    ]
    for ax, values, title, unit, colour in specifications:
        bars = ax.barh(positions, values, color=colour, height=0.48)
        ax.set_yticks(positions, labels=labels if ax is axes[0] else [])
        ax.invert_yaxis()
        ax.set_title(title, loc="left", color=INK, fontsize=10, fontweight="bold")
        ax.grid(axis="x", color=GRID, linewidth=0.7, alpha=0.7)
        ax.set_axisbelow(True)
        ax.margins(x=0.22)
        ax.tick_params(axis="both", colors=MUTED, labelsize=8)
        ax.bar_label(
            bars,
            labels=[f"{value:.2f} {unit}" for value in values],
            padding=4,
            fontsize=8,
            color=INK,
        )
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_facecolor("none")
    fig.patch.set_alpha(0)
    fig.tight_layout(w_pad=2.4)
    return fig


def action_card(number: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="action-card">
          <div class="action-number">{escape(number)}</div>
          <h3>{escape(title)}</h3>
          <p>{escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="Kashe campaign decision brief",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_styles()
model = load_dashboard_model()
headline = model["headline"]

st.markdown(
    f"""
    <section class="hero">
      <div class="eyebrow">Historical Meta Ads decision brief</div>
      <h1>Three rows generated {headline['top_three_click_share_pct']:.1f}% of recorded link clicks.</h1>
      <p>A decision-focused retrospective showing what the surviving export supports, what it cannot answer and what should change in the next live campaign.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

overview_tab, detail_tab, evidence_tab = st.tabs(
    ["Decision brief", "Campaign detail", "Evidence boundary"]
)

with overview_tab:
    kpi_columns = st.columns(4, gap="small")
    with kpi_columns[0]:
        kpi_card("Recorded spend", f"NGN {compact_number(headline['spend_ngn'])}", "All 126 export rows")
    with kpi_columns[1]:
        kpi_card("Recorded impressions", compact_number(headline["impressions"]), "Summed across campaign rows")
    with kpi_columns[2]:
        kpi_card("Recorded link clicks", compact_number(headline["link_clicks"]), "106 comparable link rows")
    with kpi_columns[3]:
        kpi_card("Top-three click share", f"{headline['top_three_click_share_pct']:.1f}%", "From 44.3% of link spend")

    st.markdown(
        f"""
        <section class="executive-summary">
          <div class="summary-heading">Executive summary</div>
          <div class="summary-grid">
            <div class="summary-item">
              <div class="summary-label">Finding</div>
              <p>The export records {compact_number(headline['link_clicks'])} link clicks across 106 comparable rows, but three rows account for {headline['top_three_click_share_pct']:.1f}% of them.</p>
            </div>
            <div class="summary-item">
              <div class="summary-label">Business implication</div>
              <p>The pooled NGN {headline['weighted_cpc_ngn']:.2f} CPC is not a safe planning baseline. Excluding the three leaders raises CPC to NGN {model['sensitivity'][-1]['weighted_cpc_ngn']:.2f} and reduces derived CTR to {model['sensitivity'][-1]['derived_ctr_pct']:.2f}%.</p>
            </div>
            <div class="summary-item action">
              <div class="summary-label">Recommended action</div>
              <p>Investigate whether accumulated learning contributed to the exceptional Bunda and Pressure rows by reconstructing the sequence from Let's Fly Away through Bunda to Pressure, then carry only supported lessons into the next prospectively measured campaign.</p>
            </div>
            <div class="summary-item">
              <div class="summary-label">Evidence limit</div>
              <p>The export can describe concentration and sensitivity, but it lacks row-specific dates and delivery settings. It cannot establish a time trend, creative cause, revenue effect or durable fan value.</p>
            </div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    chart_columns = st.columns([1, 1.12], gap="large")
    with chart_columns[0]:
        st.subheader("Response was concentrated, not evenly distributed")
        concentration = concentration_figure(model["contribution"])
        st.pyplot(concentration, width="stretch")
        plt.close(concentration)
    with chart_columns[1]:
        st.subheader("The aggregate efficiency depends on exceptional rows")
        sensitivity = sensitivity_figure(model["sensitivity"])
        st.pyplot(sensitivity, width="stretch")
        plt.close(sensitivity)

    st.subheader("Future campaign measurement plan")
    action_columns = st.columns(3, gap="small")
    with action_columns[0]:
        action_card(
            "01 / PLAN",
            "Define the decision",
            "Choose one primary outcome, map the journey from exposure to value, and set the budget, observation window and decision rule before launch.",
        )
    with action_columns[1]:
        action_card(
            "02 / INSTRUMENT",
            "Capture the missing evidence",
            "Preserve stable IDs, creative and delivery labels, tagged links, costs and consented downstream events; test the tracking before spend begins.",
        )
    with action_columns[2]:
        action_card(
            "03 / RUN & LEARN",
            "Keep a complete record",
            "Export at fixed checkpoints, log changes and compare platform response with later fan or commercial outcomes. Add a controlled test only when the design and budget support it.",
        )

    st.markdown(
        '<p class="small-note">Reporting period: not reliably recoverable from the surviving export. No target or prior-period comparison is available, so the dashboard does not invent trend arrows or RAG status.</p>',
        unsafe_allow_html=True,
    )

with detail_tab:
    st.subheader("Link-campaign rows, ranked by recorded clicks")
    st.write(
        "Use this table for follow-up questions. It is not a league table of creative quality: "
        "objective, audience, placement, budget, duration and the underlying assets are incomplete."
    )
    st.dataframe(
        model["campaign_detail"],
        width="stretch",
        height=540,
        hide_index=True,
        column_config={
            "Link clicks": st.column_config.NumberColumn(format="localized"),
            "Spend (NGN)": st.column_config.NumberColumn(format="%.2f"),
            "Impressions": st.column_config.NumberColumn(format="localized"),
            "CPC (NGN)": st.column_config.NumberColumn(format="%.2f"),
            "CTR (%)": st.column_config.NumberColumn(format="%.2f%%"),
        },
    )

with evidence_tab:
    supported, limited = st.columns(2, gap="large")
    with supported:
        st.subheader("What the export supports")
        st.markdown(
            """
            - Recorded spend, impressions and platform-reported results.
            - Descriptive comparisons within the link-click result type.
            - Concentration and sensitivity calculations.
            - A lower-bound view of rows explicitly named Bunda.
            """
        )
    with limited:
        st.subheader("What it cannot establish")
        st.markdown(
            """
            - Revenue, profit, ROAS or total campaign return.
            - Which hook, format, creator or audience caused the response.
            - Unique reach across rows or a reliable campaign timeline.
            - Whether inexpensive clicks produced durable customer value.
            """
        )

    st.subheader("Historical context kept separate from platform evidence")
    st.write(
        "The Facebook page grew from launch to around 5,000 followers in just over a month "
        "during the paid-growth phase; click-to-WhatsApp activity supported a direct audience "
        "contact list; and the Bunda video reached 230,000+ YouTube views. These are "
        "author-reported outcomes. The surviving Meta export partly corroborates the Facebook "
        "and messaging activity but does not independently preserve the full timeline, later "
        "contact use or YouTube total."
    )
    st.caption(
        "Source: data/meta_campaign_export_sanitized.csv and analysis/summary.json. "
        "See METHODOLOGY.md and PROVENANCE.md for the full evidence trail."
    )
