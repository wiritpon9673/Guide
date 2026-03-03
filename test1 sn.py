import streamlit as st
import math

st.set_page_config(page_title="AASHTO 1993 Pavement Design", layout="wide")

st.title("🛣️ AASHTO 1993 Flexible Pavement Design Calculator")
st.markdown("---")

# Sidebar for inputs
st.sidebar.header("Input Parameters")

# Design inputs
W18 = st.sidebar.number_input(
    "Predicted 18-kip ESAL (W₁₈)", 
    min_value=1000.0, 
    value=1000000.0,
    format="%.0f",
    help="Total equivalent 18-kip single axle loads over design period"
)

R = st.sidebar.slider(
    "Reliability (R) %", 
    min_value=50, 
    max_value=99, 
    value=95,
    help="Probability that pavement will perform satisfactorily"
)

# Standard normal deviate based on reliability
ZR_values = {
    50: 0.000, 60: -0.253, 70: -0.524, 75: -0.674, 80: -0.841,
    85: -1.037, 90: -1.282, 95: -1.645, 99: -2.327
}
ZR = ZR_values.get(R, -1.645)

S0 = st.sidebar.number_input(
    "Overall Standard Deviation (S₀)", 
    min_value=0.30, 
    max_value=0.50, 
    value=0.45,
    step=0.01,
    help="Typical range: 0.40-0.50"
)

delta_PSI = st.sidebar.number_input(
    "ΔPSI (Design Serviceability Loss)", 
    min_value=1.0, 
    max_value=3.0, 
    value=2.0,
    step=0.1,
    help="Difference between initial and terminal serviceability"
)

MR = st.sidebar.number_input(
    "Subgrade Resilient Modulus (MR) psi", 
    min_value=1000, 
    max_value=20000, 
    value=5000,
    step=100,
    help="Effective roadbed soil resilient modulus"
)

st.sidebar.markdown("---")
st.sidebar.header("Layer Coefficients & Drainage")

st.sidebar.subheader("🔸 Surface Layer (ชั้นผิวทาง)")
a1 = st.sidebar.number_input(
    "Layer coefficient (a₁)", 
    min_value=0.20, 
    max_value=0.50, 
    value=0.44,
    step=0.01,
    help="Typical for asphalt concrete: 0.40-0.44",
    key="coef_a1"
)

m1 = st.sidebar.number_input(
    "Drainage coefficient (m₁)", 
    min_value=0.5, 
    max_value=1.4, 
    value=1.0,
    step=0.1,
    help="Excellent: 1.2-1.4, Good: 1.0-1.2, Fair: 0.8-1.0",
    key="drain_m1"
)

st.sidebar.subheader("🔸 Base Layer (ชั้นฐาน)")
a2 = st.sidebar.number_input(
    "Layer coefficient (a₂)", 
    min_value=0.05, 
    max_value=0.20, 
    value=0.14,
    step=0.01,
    help="Typical for granular base: 0.10-0.14",
    key="coef_a2"
)

m2 = st.sidebar.number_input(
    "Drainage coefficient (m₂)", 
    min_value=0.5, 
    max_value=1.4, 
    value=1.0,
    step=0.1,
    help="Excellent: 1.2-1.4, Good: 1.0-1.2, Fair: 0.8-1.0",
    key="drain_m2"
)

st.sidebar.subheader("🔸 Subbase Layer (ชั้นรองฐาน)")
a3 = st.sidebar.number_input(
    "Layer coefficient (a₃)", 
    min_value=0.05, 
    max_value=0.15, 
    value=0.11,
    step=0.01,
    help="Typical for granular subbase: 0.08-0.11",
    key="coef_a3"
)

m3 = st.sidebar.number_input(
    "Drainage coefficient (m₃)", 
    min_value=0.5, 
    max_value=1.4, 
    value=1.0,
    step=0.1,
    help="Excellent: 1.2-1.4, Good: 1.0-1.2, Fair: 0.8-1.0",
    key="drain_m3"
)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Calculation Process")
    
    # Calculate required SN using AASHTO equation
    # log10(W18) = ZR*S0 + 9.36*log10(SN+1) - 0.20 + log10(ΔPSI/(4.2-1.5)) / (0.40 + 1094/(SN+1)^5.19) + 2.32*log10(MR) - 8.07
    
    st.subheader("Step 1: AASHTO 1993 Design Equation")
    st.latex(r'''
    \log_{10}(W_{18}) = Z_R \cdot S_0 + 9.36 \cdot \log_{10}(SN+1) - 0.20 + 
    \frac{\log_{10}\left(\frac{\Delta PSI}{4.2-1.5}\right)}{0.40 + \frac{1094}{(SN+1)^{5.19}}} + 2.32 \cdot \log_{10}(M_R) - 8.07
    ''')
    
    # Iterative solution for SN
    def calculate_SN(W18, ZR, S0, delta_PSI, MR):
        SN = 5.0  # Initial guess
        tolerance = 0.001
        max_iterations = 100
        
        for i in range(max_iterations):
            # AASHTO equation
            term1 = ZR * S0
            term2 = 9.36 * math.log10(SN + 1) - 0.20
            term3_num = math.log10(delta_PSI / (4.2 - 1.5))
            term3_den = 0.40 + (1094 / ((SN + 1) ** 5.19))
            term3 = term3_num / term3_den
            term4 = 2.32 * math.log10(MR) - 8.07
            
            W18_calc = 10 ** (term1 + term2 + term3 + term4)
            
            # Check convergence
            error = abs(W18_calc - W18) / W18
            if error < tolerance:
                return SN, i + 1
            
            # Adjust SN (simple bisection-like approach)
            if W18_calc > W18:
                SN = SN * 0.98
            else:
                SN = SN * 1.02
        
        return SN, max_iterations
    
    required_SN, iterations = calculate_SN(W18, ZR, S0, delta_PSI, MR)
    
    st.subheader("Step 2: Required Structural Number")
    st.success(f"**Required SN = {required_SN:.2f}**")
    st.caption(f"Converged in {iterations} iterations")
    
    st.subheader("Step 3: Layer Thickness Design")
    st.markdown("Structural Number equation:")
    st.latex(r'SN = a_1 \cdot D_1 \cdot m_1 + a_2 \cdot D_2 \cdot m_2 + a_3 \cdot D_3 \cdot m_3')
    st.caption("where: D = thickness (inches), a = layer coefficient, m = drainage coefficient")
    
    # User input for layer thicknesses
    st.markdown("### Design Layer Thicknesses (ความหนักชั้นทาง)")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        D1 = st.number_input("Surface D₁ (inches)", min_value=1.0, max_value=12.0, value=4.0, step=0.5)
        st.caption(f"= {D1*2.54:.1f} cm")
    with col_b:
        D2 = st.number_input("Base D₂ (inches)", min_value=0.0, max_value=24.0, value=6.0, step=0.5)
        st.caption(f"= {D2*2.54:.1f} cm")
    with col_c:
        D3 = st.number_input("Subbase D₃ (inches)", min_value=0.0, max_value=24.0, value=6.0, step=0.5)
        st.caption(f"= {D3*2.54:.1f} cm")
    
    # Calculate SN for each layer
    SN1 = a1 * D1 * m1
    SN2 = a2 * D2 * m2
    SN3 = a3 * D3 * m3
    
    st.markdown("### Layer Structural Numbers")
    col_sn1, col_sn2, col_sn3 = st.columns(3)
    
    with col_sn1:
        st.info(f"**SN₁ = {SN1:.2f}**")
        st.caption(f"{a1:.2f} × {D1:.1f} × {m1:.1f}")
    with col_sn2:
        st.info(f"**SN₂ = {SN2:.2f}**")
        st.caption(f"{a2:.2f} × {D2:.1f} × {m2:.1f}")
    with col_sn3:
        st.info(f"**SN₃ = {SN3:.2f}**")
        st.caption(f"{a3:.2f} × {D3:.1f} × {m3:.1f}")
    
    # Calculate provided SN
    provided_SN = SN1 + SN2 + SN3
    
    st.markdown("---")
    col_x, col_y = st.columns(2)
    
    with col_x:
        st.metric("Required SN", f"{required_SN:.2f}")
    with col_y:
        st.metric("Provided SN", f"{provided_SN:.2f}", 
                 delta=f"{provided_SN - required_SN:.2f}",
                 delta_color="normal" if provided_SN >= required_SN else "inverse")
    
    if provided_SN >= required_SN:
        st.success("✅ Design is ADEQUATE - Provided SN meets or exceeds required SN")
    else:
        st.error("❌ Design is INADEQUATE - Increase layer thicknesses")
        st.warning(f"⚠️ Need to add SN = {abs(provided_SN - required_SN):.2f}")

with col2:
    st.header("📋 Design Summary")
    
    st.markdown(f"""
    **Design Inputs:**
    - ESAL (W₁₈): {W18:,.0f}
    - Reliability: {R}%
    - ZR: {ZR:.3f}
    - S₀: {S0:.2f}
    - ΔPSI: {delta_PSI:.1f}
    - MR: {MR:,} psi
    
    **Layer Properties:**
    
    *Surface Layer:*
    - Thickness (D₁): {D1:.1f} in ({D1*2.54:.1f} cm)
    - Coefficient (a₁): {a1:.2f}
    - Drainage (m₁): {m1:.1f}
    - SN₁: {SN1:.2f}
    
    *Base Layer:*
    - Thickness (D₂): {D2:.1f} in ({D2*2.54:.1f} cm)
    - Coefficient (a₂): {a2:.2f}
    - Drainage (m₂): {m2:.1f}
    - SN₂: {SN2:.2f}
    
    *Subbase Layer:*
    - Thickness (D₃): {D3:.1f} in ({D3*2.54:.1f} cm)
    - Coefficient (a₃): {a3:.2f}
    - Drainage (m₃): {m3:.1f}
    - SN₃: {SN3:.2f}
    
    **Total Thickness:** {D1+D2+D3:.1f} in ({(D1+D2+D3)*2.54:.1f} cm)
    
    **Structural Numbers:**
    - Required: {required_SN:.2f}
    - Provided: {provided_SN:.2f}
    - Difference: {provided_SN - required_SN:+.2f}
    """)
    
    # Pavement structure visualization
    st.markdown("---")
    st.markdown("### Pavement Structure")
    st.markdown(f"""
```
┌────────────────────────────┐
│  Surface Course (AC)       │ {D1:.1f}" ({D1*2.54:.1f} cm)
│  a₁={a1:.2f}, m₁={m1:.1f}       │ SN₁={SN1:.2f}
├────────────────────────────┤
│  Base Course               │ {D2:.1f}" ({D2*2.54:.1f} cm)
│  a₂={a2:.2f}, m₂={m2:.1f}       │ SN₂={SN2:.2f}
├────────────────────────────┤
│  Subbase Course            │ {D3:.1f}" ({D3*2.54:.1f} cm)
│  a₃={a3:.2f}, m₃={m3:.1f}       │ SN₃={SN3:.2f}
├────────────────────────────┤
│  Subgrade                  │
│  MR = {MR:,} psi          │
└────────────────────────────┘

Total SN = {provided_SN:.2f}
Required SN = {required_SN:.2f}
```
    """)

# Additional information section
st.markdown("---")
with st.expander("📚 คำแนะนำค่าสัมประสิทธิ์ (Coefficient Guidelines)"):
    col_guide1, col_guide2 = st.columns(2)
    
    with col_guide1:
        st.markdown("""
        **Layer Coefficient (a):**
        
        *Surface (Asphalt Concrete):*
        - High quality: 0.44
        - Good quality: 0.40-0.42
        - Fair quality: 0.35-0.38
        
        *Base Course:*
        - Crushed stone: 0.14
        - Dense graded: 0.12-0.13
        - Sandy gravel: 0.10-0.11
        
        *Subbase Course:*
        - High quality: 0.11
        - Good quality: 0.08-0.10
        - Fair quality: 0.06-0.08
        """)
    
    with col_guide2:
        st.markdown("""
        **Drainage Coefficient (m):**
        
        *Quality of Drainage:*
        - Excellent: 1.2-1.4
        - Good: 1.0-1.2
        - Fair: 0.8-1.0
        - Poor: 0.6-0.8
        - Very poor: 0.4-0.6
        
        *Note:*
        - Surface layer typically uses m₁ = 1.0
        - Base and subbase affected by drainage
        - Consider local rainfall patterns
        """)

st.markdown("---")
st.caption("📚 Reference: AASHTO Guide for Design of Pavement Structures, 1993")
st.caption("⚠️ This calculator is for educational purposes. Consult with a licensed engineer for actual pavement design.")
