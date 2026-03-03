import streamlit as st
import math

st.set_page_config(page_title="AASHTO 1993 Pavement Design", layout="wide")

st.title("🛣️ AASHTO 1993 Flexible Pavement Design Calculator")
st.markdown("คำนวณ Structural Number สำหรับผิวทางลาดยาง")
st.markdown("---")

# Sidebar for design inputs
st.sidebar.header("🔧 ข้อมูลการออกแบบ (Design Parameters)")

# Design inputs
W18 = st.sidebar.number_input(
    "Predicted 18-kip ESAL (W₁₈)", 
    min_value=1000.0, 
    value=1000000.0,
    format="%.0f",
    help="จำนวนรถบรรทุกมาตรฐาน 18-kip ตลอดอายุการใช้งาน"
)

R = st.sidebar.slider(
    "Reliability (R) %", 
    min_value=50, 
    max_value=99, 
    value=95,
    help="ความน่าเชื่อถือของการออกแบบ"
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
    help="ค่าเบี่ยงเบนมาตรฐาน (ทั่วไป: 0.40-0.50)"
)

delta_PSI = st.sidebar.number_input(
    "ΔPSI (Design Serviceability Loss)", 
    min_value=1.0, 
    max_value=3.0, 
    value=2.0,
    step=0.1,
    help="ค่าการสูญเสียความสามารถในการให้บริการ"
)

MR = st.sidebar.number_input(
    "Subgrade Resilient Modulus (MR) psi", 
    min_value=1000, 
    max_value=20000, 
    value=5000,
    step=100,
    help="โมดูลัสความยืดหยุ่นของดินเดิม"
)

# Main content - Two columns
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.header("📊 ข้อมูลชั้นทาง (Layer Information)")
    
    # Create tabs for different layers
    tab1, tab2, tab3 = st.tabs(["ชั้นผิวทาง (Surface)", "ชั้นฐาน (Base)", "ชั้นรองฐาน (Subbase)"])
    
    with tab1:
        st.subheader("ชั้นผิวทาง - Surface Course (Asphalt Concrete)")
        col1a, col1b, col1c = st.columns(3)
        
        with col1a:
            D1 = st.number_input(
                "ความหนัก D₁ (นิ้ว/inches)", 
                min_value=0.0, 
                max_value=12.0, 
                value=4.0, 
                step=0.5,
                key="D1"
            )
            st.caption(f"= {D1*2.54:.1f} เซนติเมตร")
        
        with col1b:
            a1 = st.number_input(
                "สัมประสิทธิ์ชั้น a₁", 
                min_value=0.20, 
                max_value=0.50, 
                value=0.44,
                step=0.01,
                key="a1",
                help="AC: 0.40-0.44"
            )
        
        with col1c:
            m1 = st.number_input(
                "สัมประสิทธิ์การระบาย m₁", 
                min_value=0.5, 
                max_value=1.4, 
                value=1.0,
                step=0.1,
                key="m1",
                help="ดี: 1.0-1.2, พอใช้: 0.8-1.0"
            )
        
        SN1 = a1 * D1 * m1
        st.info(f"**SN₁ = a₁ × D₁ × m₁ = {a1:.2f} × {D1:.1f} × {m1:.1f} = {SN1:.2f}**")
    
    with tab2:
        st.subheader("ชั้นฐาน - Base Course (Granular Base)")
        col2a, col2b, col2c = st.columns(3)
        
        with col2a:
            D2 = st.number_input(
                "ความหนัก D₂ (นิ้ว/inches)", 
                min_value=0.0, 
                max_value=24.0, 
                value=6.0, 
                step=0.5,
                key="D2"
            )
            st.caption(f"= {D2*2.54:.1f} เซนติเมตร")
        
        with col2b:
            a2 = st.number_input(
                "สัมประสิทธิ์ชั้น a₂", 
                min_value=0.05, 
                max_value=0.20, 
                value=0.14,
                step=0.01,
                key="a2",
                help="Granular Base: 0.10-0.14"
            )
        
        with col2c:
            m2 = st.number_input(
                "สัมประสิทธิ์การระบาย m₂", 
                min_value=0.5, 
                max_value=1.4, 
                value=1.0,
                step=0.1,
                key="m2",
                help="ดี: 1.0-1.2, พอใช้: 0.8-1.0"
            )
        
        SN2 = a2 * D2 * m2
        st.info(f"**SN₂ = a₂ × D₂ × m₂ = {a2:.2f} × {D2:.1f} × {m2:.1f} = {SN2:.2f}**")
    
    with tab3:
        st.subheader("ชั้นรองฐาน - Subbase Course (Granular Subbase)")
        col3a, col3b, col3c = st.columns(3)
        
        with col3a:
            D3 = st.number_input(
                "ความหนัก D₃ (นิ้ว/inches)", 
                min_value=0.0, 
                max_value=24.0, 
                value=6.0, 
                step=0.5,
                key="D3"
            )
            st.caption(f"= {D3*2.54:.1f} เซนติเมตร")
        
        with col3b:
            a3 = st.number_input(
                "สัมประสิทธิ์ชั้น a₃", 
                min_value=0.05, 
                max_value=0.15, 
                value=0.11,
                step=0.01,
                key="a3",
                help="Granular Subbase: 0.08-0.11"
            )
        
        with col3c:
            m3 = st.number_input(
                "สัมประสิทธิ์การระบาย m₃", 
                min_value=0.5, 
                max_value=1.4, 
                value=1.0,
                step=0.1,
                key="m3",
                help="ดี: 1.0-1.2, พอใช้: 0.8-1.0"
            )
        
        SN3 = a3 * D3 * m3
        st.info(f"**SN₃ = a₃ × D₃ × m₃ = {a3:.2f} × {D3:.1f} × {m3:.1f} = {SN3:.2f}**")

with col_right:
    st.header("📈 ผลการคำนวณ (Results)")
    
    # Calculate required SN using AASHTO equation
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
            
            # Adjust SN
            if W18_calc > W18:
                SN = SN * 0.98
            else:
                SN = SN * 1.02
        
        return SN, max_iterations
    
    required_SN, iterations = calculate_SN(W18, ZR, S0, delta_PSI, MR)
    
    # Calculate provided SN
    provided_SN = SN1 + SN2 + SN3
    
    st.subheader("🎯 Structural Number (SN)")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.metric(
            "Required SN", 
            f"{required_SN:.2f}",
            help="SN ที่ต้องการจากการออกแบบ"
        )
    
    with col_b:
        delta_SN = provided_SN - required_SN
        st.metric(
            "Provided SN", 
            f"{provided_SN:.2f}",
            delta=f"{delta_SN:.2f}",
            delta_color="normal" if provided_SN >= required_SN else "inverse",
            help="SN ที่ได้จากชั้นทางที่ออกแบบ"
        )
    
    # Design adequacy
    st.markdown("---")
    if provided_SN >= required_SN:
        st.success("✅ **การออกแบบเหมาะสม (ADEQUATE)**")
        st.write(f"Provided SN มากกว่า Required SN: +{delta_SN:.2f}")
    else:
        st.error("❌ **การออกแบบไม่เพียงพอ (INADEQUATE)**")
        st.write(f"ต้องเพิ่ม SN อีก: {abs(delta_SN):.2f}")
        st.warning("⚠️ กรุณาเพิ่มความหนาของชั้นทางหรือปรับปรุงคุณภาพวัสดุ")
    
    # Pavement structure visualization
    st.markdown("---")
    st.subheader("📐 โครงสร้างผิวทาง")
    
    total_thickness = D1 + D2 + D3
    
    st.markdown(f"""
    ```
    ┌──────────────────────────────┐
    │  ชั้นผิวทาง (AC)              │ {D1:.1f}" ({D1*2.54:.1f} cm)
    │  a₁={a1:.2f}, m₁={m1:.1f}          │ SN₁ = {SN1:.2f}
    ├──────────────────────────────┤
    │  ชั้นฐาน (Base)               │ {D2:.1f}" ({D2*2.54:.1f} cm)
    │  a₂={a2:.2f}, m₂={m2:.1f}          │ SN₂ = {SN2:.2f}
    ├──────────────────────────────┤
    │  ชั้นรองฐาน (Subbase)         │ {D3:.1f}" ({D3*2.54:.1f} cm)
    │  a₃={a3:.2f}, m₃={m3:.1f}          │ SN₃ = {SN3:.2f}
    ├──────────────────────────────┤
    │  ดินเดิม (Subgrade)           │
    │  MR = {MR:,} psi             │
    └──────────────────────────────┘
    
    ความหนักรวม: {total_thickness:.1f}" ({total_thickness*2.54:.1f} cm)
    ```
    """)
    
    # Detailed summary
    st.markdown("---")
    st.subheader("📋 สรุปผลการออกแบบ")
    
    st.markdown(f"""
    **ข้อมูลการออกแบบ:**
    - ESAL (W₁₈): {W18:,.0f}
    - Reliability: {R}% (ZR = {ZR:.3f})
    - S₀: {S0:.2f}
    - ΔPSI: {delta_PSI:.1f}
    - MR: {MR:,} psi
    
    **ค่า Structural Number:**
    - SN₁ (Surface): {SN1:.2f}
    - SN₂ (Base): {SN2:.2f}
    - SN₃ (Subbase): {SN3:.2f}
    - **Total Provided SN: {provided_SN:.2f}**
    - **Required SN: {required_SN:.2f}**
    - **ผลต่าง: {delta_SN:+.2f}**
    
    **ความหนักชั้นทาง:**
    - Surface: {D1:.1f}" ({D1*2.54:.1f} cm)
    - Base: {D2:.1f}" ({D2*2.54:.1f} cm)
    - Subbase: {D3:.1f}" ({D3*2.54:.1f} cm)
    - **รวม: {total_thickness:.1f}" ({total_thickness*2.54:.1f} cm)**
    """)

# Bottom section - AASHTO equation
st.markdown("---")
with st.expander("📚 สมการ AASHTO 1993 Design Equation"):
    st.latex(r'''
    \log_{10}(W_{18}) = Z_R \cdot S_0 + 9.36 \cdot \log_{10}(SN+1) - 0.20 + 
    \frac{\log_{10}\left(\frac{\Delta PSI}{4.2-1.5}\right)}{0.40 + \frac{1094}{(SN+1)^{5.19}}} + 2.32 \cdot \log_{10}(M_R) - 8.07
    ''')
    
    st.latex(r'''
    SN = a_1 \cdot D_1 \cdot m_1 + a_2 \cdot D_2 \cdot m_2 + a_3 \cdot D_3 \cdot m_3
    ''')
    
    st.markdown("""
    **สัญลักษณ์:**
    - W₁₈ = Predicted 18-kip ESAL
    - ZR = Standard normal deviate
    - S₀ = Overall standard deviation
    - ΔPSI = Design serviceability loss
    - MR = Subgrade resilient modulus (psi)
    - SN = Structural number
    - aᵢ = Layer coefficient
    - Dᵢ = Layer thickness (inches)
    - mᵢ = Drainage coefficient
    """)

st.markdown("---")
st.caption("📚 อ้างอิง: AASHTO Guide for Design of Pavement Structures, 1993")
st.caption("⚠️ โปรแกรมนี้ใช้เพื่อการศึกษาเท่านั้น กรุณาปรึกษาวิศวกรผู้เชี่ยวชาญสำหรับการออกแบบจริง")
