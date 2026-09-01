# 24. GRADIO DASHBOARD — FIXED2 VISUAL + CORRECTED VALIDATION v2.5
# Ganti seluruh cell dashboard Streamlit 24a–24d dengan SATU cell ini.
# Tidak menggunakan Streamlit, ngrok, port 8501, atau Colab proxy.

import importlib
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

print("[1/4] Memeriksa Gradio dan Plotly...", flush=True)

required_packages = {
    "gradio": "gradio",
    "plotly": "plotly",
}

missing_packages = []
for module_name, package_name in required_packages.items():
    try:
        importlib.import_module(module_name)
    except ImportError:
        missing_packages.append(package_name)

if missing_packages:
    print("Menginstal:", missing_packages, flush=True)
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-q",
        *missing_packages,
    ])

import gradio as gr
import plotly.express as px
import plotly.graph_objects as go

print("[2/4] Membaca hasil Corrected Validation v2.5...", flush=True)

try:
    DASHBOARD_RESULTS_DIR = Path(RESULTS_DIR).resolve()
except NameError:
    DASHBOARD_RESULTS_DIR = Path("/content/ercyris_results").resolve()

print("RESULTS_DIR:", DASHBOARD_RESULTS_DIR)

def read_csv(filename):
    path = DASHBOARD_RESULTS_DIR / filename
    if not path.exists():
        print("BELUM ADA:", filename)
        return pd.DataFrame()
    try:
        frame = pd.read_csv(path)
        print("ADA      :", filename, frame.shape)
        return frame
    except Exception as exc:
        print("GAGAL    :", filename, exc)
        return pd.DataFrame()

metrics_df = read_csv("final_test_metrics.csv")
robustness_df = read_csv("noise_robustness.csv")
shap_df = read_csv("shap_feature_importance.csv")
diagnostic_df = read_csv("diagnostic_error_analysis.csv")
triage_df = read_csv("operational_triage_distribution.csv")
risk_df = read_csv("nist_risk_assessment_primary.csv")
benchmark_df = read_csv("near_rt_stagewise_benchmark.csv")
calibration_df = read_csv("calibration_comparison.csv")

if metrics_df.empty:
    raise FileNotFoundError(
        "final_test_metrics.csv belum tersedia. "
        "Jalankan seluruh eksperimen sampai Step 22 sebelum dashboard."
    )

if "model" not in metrics_df.columns:
    raise ValueError(
        "final_test_metrics.csv tidak memiliki kolom 'model'."
    )

models = metrics_df["model"].dropna().astype(str).unique().tolist()
if not models:
    raise ValueError("Daftar model pada final_test_metrics.csv kosong.")

sigma_options = [0.0]
if not robustness_df.empty and "sigma" in robustness_df.columns:
    sigma_options = sorted(
        pd.to_numeric(
            robustness_df["sigma"],
            errors="coerce",
        ).dropna().unique().tolist()
    )
    if not sigma_options:
        sigma_options = [0.0]

try:
    primary_model_name_ui = str(primary_model_name)
except Exception:
    primary_model_name_ui = models[0]

default_model = (
    primary_model_name_ui
    if primary_model_name_ui in models
    else models[0]
)

default_sigma = 0.01 if 0.01 in sigma_options else sigma_options[0]

RISK_COLORS = {
    "Very High": "#C0392B",
    "High": "#E67E22",
    "Moderate": "#F1C40F",
    "Low": "#27AE60",
}

MODEL_COLORS = {
    "XGBoost": "#185FA5",
    "RandomForest": "#0F6E56",
}

TRIAGE_LABELS = {
    "P1_immediate_investigation": "P1 — Immediate Investigation",
    "P2_analyst_review": "P2 — Analyst Review",
    "P3_monitor_or_batch_review": "P3 — Monitor / Batch Review",
}

TRIAGE_COLORS = {
    "P1 — Immediate Investigation": "#A32D2D",
    "P2 — Analyst Review": "#854F0B",
    "P3 — Monitor / Batch Review": "#3B6D11",
}

def empty_figure(title, message="Data belum tersedia"):
    fig = go.Figure()
    fig.update_layout(
        title=title,
        height=340,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[{
            "text": message,
            "xref": "paper",
            "yref": "paper",
            "x": 0.5,
            "y": 0.5,
            "showarrow": False,
            "font": {"size": 17, "color": "#6B7280"},
        }],
    )
    return fig

def as_number(row, column, default=0.0):
    try:
        value = row.get(column, default)
        return float(value) if pd.notna(value) else float(default)
    except Exception:
        return float(default)

def metric_card(label, value, subtitle, accent):
    return f"""
    <div class="metric-card" style="border-left-color:{accent}">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{accent}">{value}</div>
        <div class="metric-sub">{subtitle}</div>
    </div>
    """

def build_kpis(model):
    selected = metrics_df[
        metrics_df["model"].astype(str) == str(model)
    ].iloc[0]

    f1 = as_number(selected, "F1")
    prauc = as_number(selected, "PR_AUC")
    far = as_number(selected, "FAR")

    model_shap = (
        shap_df[shap_df["model"].astype(str) == str(model)].copy()
        if not shap_df.empty and "model" in shap_df.columns
        else pd.DataFrame()
    )

    fss = 0.0
    if (
        not model_shap.empty
        and "FSS_clean_vs_noise" in model_shap.columns
    ):
        values = pd.to_numeric(
            model_shap["FSS_clean_vs_noise"],
            errors="coerce",
        ).dropna()
        if len(values):
            fss = float(values.iloc[0])

    total_alerts = int(len(risk_df))

    cards = [
        metric_card(
            "F1 Score",
            f"{f1:.4f}",
            "Final temporal test",
            "#0F6E56" if f1 >= 0.80 else "#A32D2D",
        ),
        metric_card(
            "PR-AUC",
            f"{prauc:.4f}",
            "Final temporal test",
            "#0F6E56" if prauc >= 0.90 else "#854F0B",
        ),
        metric_card(
            "FAR",
            f"{far:.6f}",
            "False alarm rate",
            "#0F6E56" if far < 0.001 else "#A32D2D",
        ),
        metric_card(
            "FSS",
            f"{100*fss:.1f}%",
            "Clean-to-noise stability",
            "#0F6E56" if fss >= 0.80 else "#854F0B",
        ),
        metric_card(
            "Total Alerts",
            f"{total_alerts:,}",
            "Final temporal test",
            "#185FA5",
        ),
    ]

    return (
        '<div class="kpi-grid">'
        + "".join(cards)
        + "</div>"
    )

def build_header(model, sigma):
    threshold = globals().get("primary_threshold", None)
    threshold_text = (
        f"{float(threshold):.3f}"
        if threshold is not None
        else "—"
    )

    return f"""
    <div class="main-header">
        <h1>🛡️ ER-CyRIS Dashboard Prototype</h1>
        <p>
            Corrected Validation v2.5 · Model: {model} ·
            σ={sigma} · Threshold={threshold_text}
        </p>
    </div>
    """

def build_robustness(model):
    if robustness_df.empty:
        return empty_figure(
            "S2 Noise Robustness — F1 vs σ"
        )

    required = {"model", "sigma", "F1"}
    if not required.issubset(robustness_df.columns):
        return empty_figure(
            "S2 Noise Robustness",
            "Kolom model, sigma, atau F1 tidak tersedia",
        )

    plot_df = robustness_df.copy()
    plot_df["sigma"] = pd.to_numeric(
        plot_df["sigma"], errors="coerce"
    )
    plot_df["F1"] = pd.to_numeric(
        plot_df["F1"], errors="coerce"
    )

    fig = go.Figure()

    for model_name in models:
        subset = plot_df[
            plot_df["model"].astype(str) == str(model_name)
        ].sort_values("sigma")

        if subset.empty:
            continue

        fig.add_trace(
            go.Scatter(
                x=subset["sigma"],
                y=subset["F1"],
                mode="lines+markers",
                name=str(model_name),
                line={
                    "color": MODEL_COLORS.get(
                        str(model_name),
                        "#6B7280",
                    ),
                    "width": 3 if str(model_name) == str(model) else 1.5,
                },
                opacity=1.0 if str(model_name) == str(model) else 0.42,
                marker={"size": 8},
            )
        )

    fig.update_layout(
        title="S2 Noise Robustness — F1 vs σ",
        height=350,
        margin={"t": 50, "b": 45, "l": 55, "r": 20},
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Noise σ",
        yaxis_title="F1",
        yaxis_range=[0, 1.05],
        legend={"orientation": "h", "y": 1.12},
    )
    fig.update_xaxes(showgrid=True, gridcolor="#F4F2EB")
    fig.update_yaxes(showgrid=True, gridcolor="#F4F2EB")
    return fig

def build_risk_figure():
    if risk_df.empty or "risk_level" not in risk_df.columns:
        return empty_figure("NIST Risk Distribution")

    counts = (
        risk_df["risk_level"]
        .value_counts()
        .rename_axis("Risk Level")
        .reset_index(name="Count")
    )

    fig = px.pie(
        counts,
        names="Risk Level",
        values="Count",
        hole=0.55,
        color="Risk Level",
        color_discrete_map=RISK_COLORS,
        title="NIST Risk Distribution",
    )
    fig.update_layout(
        height=350,
        margin={"t": 50, "b": 20, "l": 20, "r": 20},
        paper_bgcolor="white",
        legend={"orientation": "h", "y": -0.05},
    )
    return fig

def build_shap(model):
    if (
        shap_df.empty
        or "model" not in shap_df.columns
        or "feature" not in shap_df.columns
        or "mean_abs_shap" not in shap_df.columns
    ):
        return empty_figure("SHAP Explainability")

    subset = shap_df[
        shap_df["model"].astype(str) == str(model)
    ].copy()

    if subset.empty:
        return empty_figure(
            f"SHAP Explainability — {model}",
            "Tidak ada baris untuk model terpilih",
        )

    subset["mean_abs_shap"] = pd.to_numeric(
        subset["mean_abs_shap"],
        errors="coerce",
    )

    subset = (
        subset.sort_values(
            "mean_abs_shap",
            ascending=True,
        )
        .tail(15)
    )

    fig = px.bar(
        subset,
        x="mean_abs_shap",
        y="feature",
        orientation="h",
        color="mean_abs_shap",
        color_continuous_scale="Blues",
        title=f"SHAP Explainability — {model}",
    )
    fig.update_layout(
        height=500,
        margin={"t": 50, "b": 40, "l": 165, "r": 20},
        coloraxis_showscale=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    return fig

def build_detection(model):
    selected = metrics_df[
        metrics_df["model"].astype(str) == str(model)
    ].iloc[0]

    tn = int(as_number(selected, "TN"))
    fp = int(as_number(selected, "FP"))
    fn = int(as_number(selected, "FN"))
    tp = int(as_number(selected, "TP"))

    matrix = np.array([[tn, fp], [fn, tp]])

    fig = px.imshow(
        matrix,
        text_auto=True,
        x=["Predicted Normal", "Predicted Anomaly"],
        y=["Actual Normal", "Actual Anomaly"],
        color_continuous_scale="Blues",
        aspect="auto",
        title=f"Confusion Matrix — {model}",
    )
    fig.update_layout(height=390, paper_bgcolor="white")
    return fig

def build_triage():
    if (
        triage_df.empty
        or not {"triage", "count"}.issubset(triage_df.columns)
    ):
        return empty_figure("Operational Triage")

    plot_df = triage_df.copy()
    plot_df["Priority"] = (
        plot_df["triage"]
        .map(TRIAGE_LABELS)
        .fillna(plot_df["triage"])
    )

    fig = px.bar(
        plot_df,
        x="Priority",
        y="count",
        color="Priority",
        color_discrete_map=TRIAGE_COLORS,
        text="count",
        title="Operational Triage Distribution",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        showlegend=False,
        height=390,
        margin={"t": 50, "b": 100, "l": 50, "r": 20},
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    return fig

def build_benchmark():
    if benchmark_df.empty:
        return empty_figure("Near Real-Time Performance")

    required = {
        "batch_size",
        "p50_ms",
        "p95_ms",
        "p99_ms",
    }
    if not required.issubset(benchmark_df.columns):
        return empty_figure(
            "Near Real-Time Performance",
            "Kolom benchmark belum lengkap",
        )

    plot_df = benchmark_df.copy()

    if "stage" in plot_df.columns:
        total_rows = plot_df[
            plot_df["stage"]
            .astype(str)
            .str.contains(
                "total",
                case=False,
                na=False,
            )
        ]
        if not total_rows.empty:
            plot_df = total_rows

    long_df = plot_df.melt(
        id_vars=["batch_size"],
        value_vars=["p50_ms", "p95_ms", "p99_ms"],
        var_name="Percentile",
        value_name="Latency (ms)",
    )

    fig = px.line(
        long_df,
        x="batch_size",
        y="Latency (ms)",
        color="Percentile",
        markers=True,
        title="Near Real-Time Latency",
    )
    fig.update_layout(
        height=390,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Batch Size",
    )
    return fig

def get_model_table(model):
    return metrics_df[
        metrics_df["model"].astype(str) == str(model)
    ].reset_index(drop=True)

def get_calibration_table(model):
    if calibration_df.empty or "model" not in calibration_df.columns:
        return pd.DataFrame({
            "status": ["Calibration data belum tersedia"]
        })
    return calibration_df[
        calibration_df["model"].astype(str) == str(model)
    ].reset_index(drop=True)

def get_shap_table(model):
    if shap_df.empty or "model" not in shap_df.columns:
        return pd.DataFrame({
            "status": ["SHAP data belum tersedia"]
        })
    return shap_df[
        shap_df["model"].astype(str) == str(model)
    ].head(100).reset_index(drop=True)

def get_risk_preview():
    if risk_df.empty:
        return pd.DataFrame({
            "status": ["Risk data belum tersedia"]
        })

    preferred = [
        "risk_level",
        "threat_event",
        "calibrated_probability",
        "likelihood",
        "impact_overall",
        "risk_score",
        "operational_triage",
        "top3_features",
    ]
    columns = [
        column
        for column in preferred
        if column in risk_df.columns
    ]

    return (
        risk_df[columns].head(100).reset_index(drop=True)
        if columns
        else risk_df.head(100).reset_index(drop=True)
    )

def refresh_model(model, sigma):
    return (
        build_header(model, sigma),
        build_kpis(model),
        build_robustness(model),
        build_detection(model),
        build_shap(model),
        get_model_table(model),
        get_calibration_table(model),
        get_shap_table(model),
    )

print("[3/4] Membuat dashboard dengan tampilan Fixed2...", flush=True)

FIXED2_CSS = """
.gradio-container {
    max-width: 100% !important;
    background: #F6F8FB;
    font-family: Arial, Helvetica, sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #042C53 0%, #0C4480 100%);
    padding: 25px 30px;
    border-radius: 14px;
    color: white;
    margin-bottom: 16px;
    box-shadow: 0 8px 24px rgba(4, 44, 83, 0.20);
}

.main-header h1 {
    color: white !important;
    font-size: 29px;
    margin: 0 0 6px 0;
}

.main-header p {
    color: #DCEBFA !important;
    margin: 0;
    font-size: 14px;
}

.sidebar-card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E3E9F0;
    box-shadow: 0 4px 14px rgba(15, 35, 55, 0.06);
}

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(150px, 1fr));
    gap: 12px;
    margin: 12px 0 18px 0;
}

.metric-card {
    background: white;
    padding: 15px 16px;
    border-radius: 10px;
    border: 1px solid #E5EAF0;
    border-left: 5px solid #185FA5;
    box-shadow: 0 4px 12px rgba(15, 35, 55, 0.06);
}

.metric-label {
    color: #667085;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.metric-value {
    font-size: 25px;
    font-weight: 700;
    margin: 5px 0 2px 0;
}

.metric-sub {
    color: #8A94A3;
    font-size: 11px;
}

.section-label {
    color: #042C53;
    font-size: 17px;
    font-weight: 700;
    border-bottom: 2px solid #DCE7F2;
    padding-bottom: 7px;
    margin: 8px 0 12px 0;
}

@media (max-width: 1050px) {
    .kpi-grid {
        grid-template-columns: repeat(2, minmax(150px, 1fr));
    }
}
"""

with gr.Blocks(
    title="ER-CyRIS Dashboard",
    css=FIXED2_CSS,
) as demo:

    header_html = gr.HTML(
        value=build_header(
            default_model,
            default_sigma,
        )
    )

    with gr.Row():
        with gr.Column(scale=1, min_width=245):
            with gr.Group(elem_classes=["sidebar-card"]):
                gr.Markdown("### 🛡️ ER-CyRIS")
                gr.Markdown("Siklus 3 — SIUTER SIAKAD UNSAP")

                model_dropdown = gr.Dropdown(
                    choices=models,
                    value=default_model,
                    label="Select Model",
                )

                sigma_dropdown = gr.Dropdown(
                    choices=sigma_options,
                    value=default_sigma,
                    label="S2 Noise Level (σ)",
                )

                gr.Markdown(
                    f"""
                    **Dataset Results Directory**

                    `{DASHBOARD_RESULTS_DIR}`
                    """
                )

        with gr.Column(scale=5):
            kpi_html = gr.HTML(
                value=build_kpis(default_model)
            )

            with gr.Tabs():
                with gr.Tab("📊 Overview"):
                    with gr.Row():
                        overview_robustness = gr.Plot(
                            value=build_robustness(default_model)
                        )
                        overview_risk = gr.Plot(
                            value=build_risk_figure()
                        )

                    with gr.Row():
                        overview_triage = gr.Plot(
                            value=build_triage()
                        )
                        overview_benchmark = gr.Plot(
                            value=build_benchmark()
                        )

                with gr.Tab("🔍 Detection Metrics"):
                    detection_plot = gr.Plot(
                        value=build_detection(default_model)
                    )
                    detection_table = gr.Dataframe(
                        value=get_model_table(default_model),
                        label="Final Temporal-Test Metrics",
                        interactive=False,
                    )
                    calibration_table = gr.Dataframe(
                        value=get_calibration_table(default_model),
                        label="Calibration Comparison",
                        interactive=False,
                    )

                with gr.Tab("🧠 SHAP Explainability"):
                    shap_plot = gr.Plot(
                        value=build_shap(default_model)
                    )
                    shap_table = gr.Dataframe(
                        value=get_shap_table(default_model),
                        label="SHAP Feature Importance",
                        interactive=False,
                    )

                with gr.Tab("⚠️ Triage Rationale"):
                    gr.Plot(value=build_triage())
                    gr.Dataframe(
                        value=triage_df
                        if not triage_df.empty
                        else pd.DataFrame({
                            "status": [
                                "Operational triage belum tersedia"
                            ]
                        }),
                        label="Operational Triage Distribution",
                        interactive=False,
                    )
                    gr.Dataframe(
                        value=diagnostic_df.head(100)
                        if not diagnostic_df.empty
                        else pd.DataFrame({
                            "status": [
                                "Diagnostic analysis belum tersedia"
                            ]
                        }),
                        label="Diagnostic Error Analysis — Research Only",
                        interactive=False,
                    )

                with gr.Tab("📋 NIST Risk Mapping"):
                    gr.Plot(value=build_risk_figure())
                    gr.Dataframe(
                        value=get_risk_preview(),
                        label="Alert-to-Risk Preview",
                        interactive=False,
                    )

                with gr.Tab("⚡ Near-RT Performance"):
                    gr.Plot(value=build_benchmark())
                    gr.Dataframe(
                        value=benchmark_df
                        if not benchmark_df.empty
                        else pd.DataFrame({
                            "status": [
                                "Benchmark belum tersedia"
                            ]
                        }),
                        label="Stage-Wise Benchmark",
                        interactive=False,
                    )

    model_dropdown.change(
        fn=refresh_model,
        inputs=[model_dropdown, sigma_dropdown],
        outputs=[
            header_html,
            kpi_html,
            overview_robustness,
            detection_plot,
            shap_plot,
            detection_table,
            calibration_table,
            shap_table,
        ],
    )

    sigma_dropdown.change(
        fn=refresh_model,
        inputs=[model_dropdown, sigma_dropdown],
        outputs=[
            header_html,
            kpi_html,
            overview_robustness,
            detection_plot,
            shap_plot,
            detection_table,
            calibration_table,
            shap_table,
        ],
    )

print("[4/4] Menjalankan dashboard Gradio...", flush=True)
print(
    "Tunggu sampai muncul URL publik berakhiran .gradio.live",
    flush=True,
)

demo.launch(
    share=True,
    inline=True,
    show_error=True,
    debug=False,
)
