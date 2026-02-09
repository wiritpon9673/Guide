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
    help="Typical range: 0.40-0.50"
)

delta_PSI = st.sidebar.number_input(
    "ΔPSI (Design Serviceability Loss)", 
    min_value=1.0, 
    max_value=3.0, 
    value=2.0,
    help="Difference between initial and terminal serviceability"
)

MR = st.sidebar.number_input(
    "Subgrade Resilient Modulus (MR) psi", 
    min_value=1000, 
    max_value=20000, 
    value=5000,
    help="Effective roadbed soil resilient modulus"
)

st.sidebar.markdown("---")
st.sidebar.header("Layer Coefficients")

a1 = st.sidebar.number_input(
    "Surface layer coefficient (a₁)", 
    min_value=0.20, 
    max_value=0.50, 
    value=0.44,
    help="Typical for asphalt concrete: 0.40-0.44"
)

a2 = st.sidebar.number_input(
    "Base layer coefficient (a₂)", 
    min_value=0.05, 
    max_value=0.20, 
    value=0.14,
    help="Typical for granular base: 0.10-0.14"
)

a3 = st.sidebar.number_input(
    "Subbase layer coefficient (a₃)", 
    min_value=0.05, 
    max_value=0.15, 
    value=0.11,
    help="Typical for granular subbase: 0.08-0.11"
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
        tolerance = 0.01
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
                SN = SN * 0.95
            else:
                SN = SN * 1.05
        
        return SN, max_iterations
    
    required_SN, iterations = calculate_SN(W18, ZR, S0, delta_PSI, MR)
    
    st.subheader("Step 2: Required Structural Number")
    st.success(f"**Required SN = {required_SN:.2f}**")
    st.caption(f"Converged in {iterations} iterations")
    
    st.subheader("Step 3: Layer Thickness Design")
    st.markdown("Structural Number equation:")
    st.latex(r'SN = a_1 \cdot D_1 + a_2 \cdot D_2 \cdot m_2 + a_3 \cdot D_3 \cdot m_3')
    st.caption("where: D = thickness (inches), m = drainage coefficient (assumed = 1.0)")
    
    # Simple layer distribution (can be customized)
    # Assume m2 = m3 = 1.0 for simplicity
    m2 = 1.0
    m3 = 1.0
    
    # User input for layer thicknesses
    st.markdown("### Design Layer Thicknesses")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        D1 = st.number_input("Surface thickness D₁ (inches)", min_value=1.0, max_value=12.0, value=4.0, step=0.5)
    with col_b:
        D2 = st.number_input("Base thickness D₂ (inches)", min_value=0.0, max_value=24.0, value=6.0, step=0.5)
    with col_c:
        D3 = st.number_input("Subbase thickness D₃ (inches)", min_value=0.0, max_value=24.0, value=6.0, step=0.5)
    
    # Calculate provided SN
    provided_SN = a1 * D1 + a2 * D2 * m2 + a3 * D3 * m3
    
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
    
    **Layer Coefficients:**
    - a₁: {a1:.2f}
    - a₂: {a2:.2f}
    - a₃: {a3:.2f}
    
    **Layer Thicknesses:**
    - Surface: {D1:.1f} in ({D1*2.54:.1f} cm)
    - Base: {D2:.1f} in ({D2*2.54:.1f} cm)
    - Subbase: {D3:.1f} in ({D3*2.54:.1f} cm)
    - **Total: {D1+D2+D3:.1f} in ({(D1+D2+D3)*2.54:.1f} cm)**
    
    **Structural Numbers:**
    - Required: {required_SN:.2f}
    - Provided: {provided_SN:.2f}
    - Difference: {provided_SN - required_SN:+.2f}
    """)
    
    # Pavement structure visualization
    st.markdown("### Pavement Structure")
    st.markdown(f"""
```
    ┌─────────────────────────┐
    │   Surface Course        │ {D1:.1f}"
    │   (Asphalt Concrete)    │
    ├─────────────────────────┤
    │   Base Course           │ {D2:.1f}"
    │   (Granular Base)       │
    ├─────────────────────────┤
    │   Subbase Course        │ {D3:.1f}"
    │   (Granular Subbase)    │
    ├─────────────────────────┤
    │   Subgrade              │
    │   (MR = {MR:,} psi)    │
    └─────────────────────────┘
```
    """)

st.markdown("---")
st.caption("📚 Reference: AASHTO Guide for Design of Pavement Structures, 1993")
st.caption("⚠️ This calculator is for educational purposes. Consult with a licensed engineer for actual pavement design.")
