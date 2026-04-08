import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.optimize import brentq
import warnings
warnings.filterwarnings("ignore")

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AASHTO 1993 – Rigid Pavement Design",
    page_icon="🛣️",
    layout="wide",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@300;400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans Thai', sans-serif;
}

/* ── Hero Banner ── */
.hero {
    background: linear-gradient(135deg, #0a1628 0%, #112244 50%, #1a3a6b 100%);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    border: 1px solid #2a4a8a;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(52,152,219,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero h1 {
    color: #e8f4fd;
    font-size: 2.0rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.5px;
}
.hero p {
    color: #7fb3d3;
    font-size: 1.05rem;
    margin: 0;
}
.hero .badge {
    display: inline-block;
    background: rgba(52,152,219,0.25);
    color: #5dade2;
    border: 1px solid #2e86c1;
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 1rem;
}

/* ── Section Headers ── */
.section-header {
    background: linear-gradient(90deg, #1a3a6b, transparent);
    border-left: 4px solid #3498db;
    padding: 0.6rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 1.5rem 0 1rem 0;
    color: #d6eaf8;
    font-size: 1.05rem;
    font-weight: 600;
}

/* ── Result Cards ── */
.result-card {
    background: linear-gradient(135deg, #0d2137, #112a45);
    border: 1px solid #1f4e79;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 0.5rem;
    position: relative;
    overflow: hidden;
}
.result-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #2e86c1, #52be80);
}
.result-card .label {
    color: #7fb3d3;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.result-card .value {
    color: #85c1e9;
    font-size: 2.4rem;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1;
}
.result-card .unit {
    color: #5d8aa8;
    font-size: 0.9rem;
    margin-top: 0.3rem;
}

.result-main {
    background: linear-gradient(135deg, #0b3d2e, #145a38);
    border: 1px solid #1e8449;
    border-radius: 14px;
    padding: 1.8rem;
    text-align: center;
    margin-bottom: 0.5rem;
}
.result-main::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #27ae60, #82e0aa);
}
.result-main .label {
    color: #82e0aa;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.result-main .value {
    color: #a9dfbf;
    font-size: 3.2rem;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1;
}
.result-main .unit {
    color: #52be80;
    font-size: 1rem;
    margin-top: 0.4rem;
}

/* ── Info Boxes ── */
.info-box {
    background: rgba(52,152,219,0.08);
    border: 1px solid rgba(52,152,219,0.3);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-top: 1rem;
    font-size: 0.88rem;
    color: #85c1e9;
    line-height: 1.7;
}
.warn-box {
    background: rgba(243,156,18,0.08);
    border: 1px solid rgba(243,156,18,0.3);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-top: 1rem;
    font-size: 0.88rem;
    color: #f8c471;
    line-height: 1.7;
}

/* ── Formula Box ── */
.formula-box {
    background: #0a1628;
    border: 1px solid #2a4a8a;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: #85c1e9;
    line-height: 1.8;
    margin: 1rem 0;
}

/* ── Stmetric override ── */
[data-testid="stMetric"] {
    background: #0d2137;
    border: 1px solid #1f4e79;
    border-radius: 10px;
    padding: 0.8rem 1rem;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Helper Functions – AASHTO 1993 Rigid Pavement
# ═══════════════════════════════════════════════════════════════════════════════

def calc_D_rigid(W18, ZR, S0, delta_PSI, pt, k, Ec, Sc, Cd, J):
    """
    คำนวณความหนาแผ่นคอนกรีต D (นิ้ว) สำหรับผิวทางแข็งแกร่ง (Rigid Pavement)
    โดยใช้สมการ AASHTO 1993:

    log10(W18) = ZR·S0 + 7.35·log10(D+1) - 0.06
                 + [log10(ΔPSI/(4.5-1.5))] / [1 + 1.624e7/(D+1)^8.46]
                 + (4.22 - 0.32·pt)·log10[Sc·Cd·(D^0.75 - 1.132) /
                   (215.63·J·(D^0.75 - 18.42/(Ec/k)^0.25))]
    """
    log_W18 = np.log10(W18)

    def equation(D):
        if D <= 0:
            return -1e9
        term1 = ZR * S0
        term2 = 7.35 * np.log10(D + 1) - 0.06
        term3_num = np.log10(delta_PSI / (4.5 - 1.5))
        term3_den = 1 + 1.624e7 / (D + 1) ** 8.46
        term3 = term3_num / term3_den

        inner_num = Sc * Cd * (D ** 0.75 - 1.132)
        inner_den = 215.63 * J * (D ** 0.75 - 18.42 / (Ec / k) ** 0.25)
        if inner_den <= 0 or inner_num <= 0:
            return -1e9
        term4 = (4.22 - 0.32 * pt) * np.log10(inner_num / inner_den)

        return term1 + term2 + term3 + term4 - log_W18

    try:
        D_sol = brentq(equation, 2, 40, xtol=1e-6)
    except Exception:
        D_sol = None
    return D_sol


def calc_structural_number_rigid(D, Ec):
    """
    Structural Number เทียบเท่าสำหรับผิวแข็งแกร่ง
    SN_eq = a1 * D  โดยที่ a1 ≈ 0.44 (ค่ามาตรฐาน AASHTO สำหรับ PCC)
    """
    a1 = 0.44  # structural layer coefficient ของ PCC
    SN_eq = a1 * D
    return SN_eq


def calc_esal(ADT, T, TF, GF, Y, D_factor=1.0):
    """คำนวณ W18 (ESALs) ตลอดอายุการออกแบบ"""
    # Accumulated ESALs
    W18 = ADT * (T / 100) * TF * D_factor * 365 * ((1 + GF) ** Y - 1) / GF
    return W18


def reliability_ZR(R):
    """แปลงค่า Reliability (%) → ZR โดยใช้ตาราง AASHTO 1993"""
    table = {
        50: 0.000, 60: -0.253, 70: -0.524, 75: -0.674,
        80: -0.842, 85: -1.037, 90: -1.282, 91: -1.340,
        92: -1.405, 93: -1.476, 94: -1.555, 95: -1.645,
        96: -1.751, 97: -1.881, 98: -2.054, 99: -2.327,
        99.9: -3.090, 99.99: -3.750
    }
    keys = sorted(table.keys())
    if R <= keys[0]:
        return table[keys[0]]
    if R >= keys[-1]:
        return table[keys[-1]]
    for i in range(len(keys) - 1):
        if keys[i] <= R <= keys[i + 1]:
            r = (R - keys[i]) / (keys[i + 1] - keys[i])
            return table[keys[i]] + r * (table[keys[i + 1]] - table[keys[i]])
    return -1.282


# ═══════════════════════════════════════════════════════════════════════════════
# UI Layout
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
  <div class="badge">AASHTO 1993 · RIGID PAVEMENT</div>
  <h1>🛣️ ออกแบบผิวทางแข็งแกร่ง (Rigid Pavement)</h1>
  <p>คำนวณความหนาแผ่นคอนกรีต (D) และ Structural Number เทียบเท่า ตามมาตรฐาน AASHTO 1993</p>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📐 คำนวณออกแบบ", "📊 กราฟวิเคราะห์", "📖 ทฤษฎีและสูตร"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – Main Calculator
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns([1.2, 1], gap="large")

    # ── LEFT: Inputs ──────────────────────────────────────────────────────────
    with col_left:

        # ── 1. Traffic ────────────────────────────────────────────────────────
        st.markdown('<div class="section-header">🚛 ข้อมูลปริมาณจราจร (Traffic)</div>', unsafe_allow_html=True)

        mode = st.radio("วิธีกำหนด W18", ["คำนวณจากข้อมูลจราจร", "กำหนด W18 โดยตรง"], horizontal=True)

        if mode == "กำหนด W18 โดยตรง":
            W18 = st.number_input("W18 – จำนวน ESALs ตลอดอายุออกแบบ", min_value=1e4, max_value=5e8,
                                  value=5_000_000.0, step=1e5, format="%.0f")
        else:
            c1, c2 = st.columns(2)
            with c1:
                ADT = st.number_input("ADT (คัน/วัน)", min_value=100, max_value=200000, value=10000, step=500)
                T = st.number_input("สัดส่วนรถบรรทุก (%)", min_value=1.0, max_value=100.0, value=15.0, step=0.5)
                Y = st.number_input("อายุออกแบบ (ปี)", min_value=5, max_value=50, value=20, step=1)
            with c2:
                TF = st.number_input("Truck Factor (ESAL/คัน)", min_value=0.01, max_value=10.0, value=1.2, step=0.05,
                                     help="ค่าเฉลี่ยจำนวน ESAL ต่อรถบรรทุก 1 คัน")
                GF = st.number_input("Growth Factor (ทศนิยม)", min_value=0.00, max_value=0.15, value=0.03, step=0.005,
                                     format="%.3f", help="อัตราการเติบโตของปริมาณจราจร เช่น 0.03 = 3%")
                DD = st.number_input("Directional Distribution (ทศนิยม)", min_value=0.3, max_value=0.7, value=0.5, step=0.05)
            W18 = calc_esal(ADT, T, TF, GF, Y, DD)
            st.info(f"📦 W18 ที่คำนวณได้ = **{W18:,.0f}** ESALs")

        # ── 2. Reliability ────────────────────────────────────────────────────
        st.markdown('<div class="section-header">🎯 Reliability & Overall Std. Deviation</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            R = st.select_slider("Reliability R (%)",
                                 options=[50, 60, 70, 75, 80, 85, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99],
                                 value=95)
            ZR = reliability_ZR(R)
            st.caption(f"ZR = {ZR:.3f}")
        with c2:
            S0 = st.slider("Overall Std. Deviation (S₀)", 0.25, 0.55, 0.35, 0.01,
                           help="ค่าเบี่ยงเบนมาตรฐาน ปกติ 0.30–0.40 สำหรับ Rigid")

        # ── 3. Serviceability ─────────────────────────────────────────────────
        st.markdown('<div class="section-header">📉 Serviceability Loss (ΔPSI)</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            p0 = st.number_input("Initial PSI (p₀)", 3.0, 5.0, 4.5, 0.1)
        with c2:
            pt = st.number_input("Terminal PSI (pt)", 1.5, 3.0, 2.5, 0.1)
        with c3:
            delta_PSI = round(p0 - pt, 2)
            st.metric("ΔPSI", f"{delta_PSI:.2f}")

        # ── 4. Pavement & Subgrade ────────────────────────────────────────────
        st.markdown('<div class="section-header">🧱 วัสดุและโครงสร้างชั้นทาง</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            Ec = st.number_input("Ec – Modulus of Elasticity คอนกรีต (psi)",
                                 min_value=1_000_000, max_value=8_000_000,
                                 value=4_000_000, step=100_000, format="%d")
            Sc = st.number_input("Sc – Modulus of Rupture คอนกรีต (psi)",
                                 min_value=400, max_value=1000, value=650, step=10)
            Cd = st.slider("Cd – Drainage Coefficient", 0.70, 1.25, 1.00, 0.05,
                           help="1.00 = ระบายน้ำปกติ (Good, drains within 1 week)")
        with c2:
            k = st.number_input("k – Modulus of Subgrade Reaction (pci)",
                                min_value=50, max_value=1000, value=200, step=10,
                                help="ค่า k ของชั้นรองพื้นทาง (psi/in)")
            J = st.select_slider("J – Load Transfer Coefficient",
                                 options=[2.2, 2.5, 2.7, 3.0, 3.2, 3.5, 3.8, 4.0, 4.2, 4.5],
                                 value=3.2,
                                 help="2.5–3.1: มีอุปกรณ์ถ่ายแรง | 3.6–4.2: ไม่มีอุปกรณ์")

        run = st.button("🔢 คำนวณ", type="primary", use_container_width=True)

    # ── RIGHT: Results ────────────────────────────────────────────────────────
    with col_right:
        st.markdown('<div class="section-header">📋 ผลการคำนวณ</div>', unsafe_allow_html=True)

        if run or True:  # show results always (update on re-run)
            D = calc_D_rigid(W18, ZR, S0, delta_PSI, pt, k, Ec, Sc, Cd, J)

            if D is None:
                st.error("❌ ไม่สามารถคำนวณได้ กรุณาตรวจสอบค่าที่ป้อน")
            else:
                D_round = np.ceil(D * 2) / 2  # ปัดขึ้นทีละ 0.5 นิ้ว
                D_mm = D_round * 25.4
                SN_eq = calc_structural_number_rigid(D_round, Ec)

                st.markdown(f"""
                <div class="result-main" style="position:relative;">
                  <div class="label">ความหนาแผ่นคอนกรีต D (ออกแบบ)</div>
                  <div class="value">{D:.2f}<span style="font-size:1.5rem"> in</span></div>
                  <div class="unit">ปัดขึ้น → <b>{D_round:.1f} in</b> ({D_mm:.0f} mm)</div>
                </div>
                """, unsafe_allow_html=True)

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                    <div class="result-card">
                      <div class="label">Structural Number (SN_eq)</div>
                      <div class="value">{SN_eq:.2f}</div>
                      <div class="unit">equivalent SN</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
                    <div class="result-card">
                      <div class="label">W18 (ESALs)</div>
                      <div class="value" style="font-size:1.6rem">{W18:,.0f}</div>
                      <div class="unit">18-kip ESAL</div>
                    </div>""", unsafe_allow_html=True)

                # Summary table
                st.markdown("---")
                st.markdown("**📊 สรุปพารามิเตอร์ที่ใช้คำนวณ**")
                params = {
                    "W18 (ESALs)": f"{W18:,.0f}",
                    "Reliability R (%)": f"{R}",
                    "ZR": f"{ZR:.3f}",
                    "S₀": f"{S0:.2f}",
                    "ΔPSI": f"{delta_PSI:.2f}",
                    "pt": f"{pt:.1f}",
                    "k (pci)": f"{k}",
                    "Ec (psi)": f"{Ec:,}",
                    "Sc (psi)": f"{Sc}",
                    "Cd": f"{Cd:.2f}",
                    "J": f"{J}",
                    "D คำนวณ (in)": f"{D:.3f}",
                    "D ออกแบบ (in)": f"{D_round:.1f}",
                    "D ออกแบบ (mm)": f"{D_mm:.0f}",
                    "SN_equivalent": f"{SN_eq:.2f}",
                }
                for k_p, v_p in params.items():
                    cols = st.columns([2, 1])
                    cols[0].markdown(f"<span style='color:#7fb3d3;font-size:0.87rem'>{k_p}</span>", unsafe_allow_html=True)
                    cols[1].markdown(f"<span style='color:#e8f4fd;font-weight:600;font-size:0.87rem'>{v_p}</span>", unsafe_allow_html=True)

                # Drainage tip
                if Cd < 0.90:
                    st.markdown('<div class="warn-box">⚠️ ค่า Cd < 0.90 แสดงว่าระบบระบายน้ำไม่ดี ควรปรับปรุงก่อนออกแบบ</div>', unsafe_allow_html=True)
                elif Cd > 1.10:
                    st.markdown('<div class="info-box">✅ ค่า Cd > 1.10 ระบายน้ำดีมาก อาจลดความหนาลงได้เล็กน้อย</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – Charts
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">📊 กราฟวิเคราะห์ความไวของตัวแปร</div>', unsafe_allow_html=True)

    # Re-compute D for current inputs (always available)
    try:
        D_base = calc_D_rigid(W18, ZR, S0, delta_PSI, pt, k, Ec, Sc, Cd, J)
    except Exception:
        D_base = 10.0

    plt.style.use("dark_background")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.patch.set_facecolor("#0a1628")
    for ax in axes.flat:
        ax.set_facecolor("#0d1f3c")
        for spine in ax.spines.values():
            spine.set_edgecolor("#2a4a8a")
        ax.tick_params(colors="#7fb3d3", labelsize=8)
        ax.xaxis.label.set_color("#85c1e9")
        ax.yaxis.label.set_color("#85c1e9")
        ax.title.set_color("#d6eaf8")

    color_main = "#3498db"
    color_accent = "#52be80"

    # 1. D vs W18
    ax = axes[0, 0]
    w_range = np.logspace(5, 8, 80)
    d_vals = [calc_D_rigid(w, ZR, S0, delta_PSI, pt, k, Ec, Sc, Cd, J) or 0 for w in w_range]
    ax.semilogx(w_range, d_vals, color=color_main, lw=2)
    if D_base:
        ax.axhline(D_base, color=color_accent, ls="--", lw=1, alpha=0.7)
        ax.axvline(W18, color=color_accent, ls="--", lw=1, alpha=0.7)
    ax.set_xlabel("W18 (ESALs)")
    ax.set_ylabel("D (in)")
    ax.set_title("D vs W18 (log scale)")
    ax.grid(alpha=0.2, color="#2a4a8a")

    # 2. D vs k
    ax = axes[0, 1]
    k_range = np.linspace(50, 600, 60)
    d_vals = [calc_D_rigid(W18, ZR, S0, delta_PSI, pt, kk, Ec, Sc, Cd, J) or 0 for kk in k_range]
    ax.plot(k_range, d_vals, color=color_main, lw=2)
    if D_base:
        ax.axhline(D_base, color=color_accent, ls="--", lw=1, alpha=0.7)
        ax.axvline(k, color=color_accent, ls="--", lw=1, alpha=0.7)
    ax.set_xlabel("k (pci)")
    ax.set_ylabel("D (in)")
    ax.set_title("D vs Modulus of Subgrade Reaction (k)")
    ax.grid(alpha=0.2, color="#2a4a8a")

    # 3. D vs Sc
    ax = axes[1, 0]
    sc_range = np.linspace(400, 900, 60)
    d_vals = [calc_D_rigid(W18, ZR, S0, delta_PSI, pt, k, Ec, sc, Cd, J) or 0 for sc in sc_range]
    ax.plot(sc_range, d_vals, color="#e67e22", lw=2)
    if D_base:
        ax.axhline(D_base, color=color_accent, ls="--", lw=1, alpha=0.7)
        ax.axvline(Sc, color=color_accent, ls="--", lw=1, alpha=0.7)
    ax.set_xlabel("Sc – Modulus of Rupture (psi)")
    ax.set_ylabel("D (in)")
    ax.set_title("D vs Sc (Modulus of Rupture)")
    ax.grid(alpha=0.2, color="#2a4a8a")

    # 4. D vs Reliability
    ax = axes[1, 1]
    r_list = [50, 60, 70, 75, 80, 85, 90, 95, 99]
    d_r = [calc_D_rigid(W18, reliability_ZR(r), S0, delta_PSI, pt, k, Ec, Sc, Cd, J) or 0 for r in r_list]
    bars = ax.bar(r_list, d_r, width=4, color=color_main, alpha=0.8, edgecolor="#2a4a8a")
    # Highlight current
    for i, r_val in enumerate(r_list):
        if r_val == R:
            bars[i].set_color(color_accent)
    ax.set_xlabel("Reliability R (%)")
    ax.set_ylabel("D (in)")
    ax.set_title("D vs Reliability Level")
    ax.grid(axis="y", alpha=0.2, color="#2a4a8a")

    plt.tight_layout(pad=2)
    st.pyplot(fig)
    plt.close()

    # ── Cross-section diagram ─────────────────────────────────────────────────
    if D_base:
        D_design = np.ceil(D_base * 2) / 2
        st.markdown('<div class="section-header">🏗️ ภาพตัดขวางโครงสร้างผิวทาง</div>', unsafe_allow_html=True)

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        fig2.patch.set_facecolor("#0a1628")
        ax2.set_facecolor("#0a1628")
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 5.5)
        ax2.axis("off")

        layers = [
            {"label": f"Concrete Slab  D = {D_design:.1f} in ({D_design*25.4:.0f} mm)", "color": "#85929e", "h": 1.6, "y": 3.0},
            {"label": "Base / Subbase", "color": "#a9cce3", "h": 0.9, "y": 2.1},
            {"label": "Subgrade (k = {k} pci)".format(k=k), "color": "#a9dfbf", "h": 1.0, "y": 1.1},
        ]

        for layer in layers:
            rect = mpatches.FancyBboxPatch((1, layer["y"]), 8, layer["h"],
                                           boxstyle="round,pad=0.05",
                                           facecolor=layer["color"], edgecolor="#2a4a8a",
                                           alpha=0.85, linewidth=1.5)
            ax2.add_patch(rect)
            ax2.text(5, layer["y"] + layer["h"] / 2, layer["label"],
                     ha="center", va="center", fontsize=9, color="#0a1628", fontweight="bold")

        # Road surface lines
        for xi in np.linspace(1.2, 8.8, 30):
            ax2.plot([xi, xi + 0.3], [4.62, 4.62], color="#5d6d7e", lw=0.8, alpha=0.5)

        ax2.text(5, 5.1, "AASHTO 1993 – Rigid Pavement Cross-Section", ha="center",
                 fontsize=11, color="#d6eaf8", fontweight="bold")
        ax2.text(5, 0.5, f"SN equivalent = {calc_structural_number_rigid(D_design, Ec):.2f}",
                 ha="center", fontsize=10, color="#82e0aa")

        st.pyplot(fig2)
        plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 – Theory
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">📖 สมการการออกแบบ AASHTO 1993 – Rigid Pavement</div>', unsafe_allow_html=True)

    st.markdown("""
    ### สมการหลัก (Design Equation)

    AASHTO 1993 ใช้สมการต่อไปนี้สำหรับการออกแบบผิวทางแข็งแกร่ง (Jointed Plain Concrete Pavement – JPCP):
    """)

    st.markdown("""
    <div class="formula-box">
    log₁₀(W₁₈) = Z_R · S₀ + 7.35·log₁₀(D+1) − 0.06<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    + log₁₀[ΔPSI / (4.5−1.5)] / [1 + 1.624×10⁷ / (D+1)^8.46]<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    + (4.22 − 0.32·p_t) · log₁₀[S_c·C_d·(D^0.75 − 1.132) / (215.63·J·(D^0.75 − 18.42/(E_c/k)^0.25))]
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ---
    ### คำอธิบายตัวแปร

    | สัญลักษณ์ | รายละเอียด | หน่วย | ค่าแนะนำ |
    |-----------|------------|-------|----------|
    | **W₁₈** | จำนวนแกนเดี่ยว 18-kip สะสมตลอดอายุ | ESALs | — |
    | **Z_R** | Normal deviate สำหรับ Reliability R | — | −1.282 (R=90%) |
    | **S₀** | Overall standard deviation | — | 0.30–0.40 |
    | **D** | ความหนาแผ่นคอนกรีต | นิ้ว | **คำนวณ** |
    | **ΔPSI** | การสูญเสีย Serviceability (p₀ − pt) | — | — |
    | **pt** | Terminal serviceability index | — | 2.0–2.5 |
    | **E_c** | Elastic modulus ของคอนกรีต | psi | 3.6–4.5 × 10⁶ |
    | **S_c** | Modulus of rupture ของคอนกรีต | psi | 550–750 |
    | **C_d** | Drainage coefficient | — | 0.70–1.25 |
    | **J** | Load transfer coefficient | — | 2.2–4.2 |
    | **k** | Modulus of subgrade reaction | pci | 50–500 |

    ---
    ### Structural Number เทียบเท่า (SN_equivalent)

    สำหรับผิวทางแข็งแกร่ง AASHTO กำหนดค่า Layer coefficient ของ PCC ที่ **a₁ = 0.44**
    """)

    st.markdown("""
    <div class="formula-box">
    SN_eq = a₁ × D = 0.44 × D
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ---
    ### ค่า Load Transfer Coefficient (J)

    | สภาพรอยต่อ | J |
    |------------|---|
    | มีอุปกรณ์ถ่ายแรง + ไหล่ทาง Tied PCC | 2.2–2.7 |
    | มีอุปกรณ์ถ่ายแรง + ไม่มีไหล่ทาง Tied | 2.7–3.2 |
    | ไม่มีอุปกรณ์ถ่ายแรง + ไหล่ทาง Tied PCC | 3.2–3.8 |
    | ไม่มีอุปกรณ์ถ่ายแรง + ไม่มีไหล่ทาง | 3.8–4.5 |

    ---
    ### ค่า Drainage Coefficient (C_d)

    | คุณภาพการระบายน้ำ | เวลาที่น้ำขัง | C_d (1–5% อิ่มตัว) |
    |-------------------|--------------|---------------------|
    | Excellent | < 2 ชั่วโมง | 1.15–1.25 |
    | Good | < 1 วัน | 1.05–1.15 |
    | Fair | < 1 สัปดาห์ | 0.95–1.05 |
    | Poor | < 1 เดือน | 0.75–0.95 |
    | Very Poor | ไม่ระบาย | 0.40–0.75 |

    ---
    ### อ้างอิง
    > AASHTO (1993). *Guide for Design of Pavement Structures*. American Association of State Highway and Transportation Officials, Washington, D.C.
    """)

    st.markdown('<div class="info-box">ℹ️ แอปพลิเคชันนี้ใช้เพื่อการศึกษาและเป็นแนวทางเบื้องต้น การออกแบบจริงควรตรวจสอบโดยวิศวกรโยธาที่มีใบอนุญาต</div>', unsafe_allow_html=True)
