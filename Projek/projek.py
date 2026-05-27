import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as pe

st.set_page_config(
    page_title="SPK Kamera — AHP",
    layout="wide",
    page_icon="📷",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=DM+Mono:wght@400;500&display=swap');

:root {
    --navy:   #0a1628;
    --navy2:  #112040;
    --navy3:  #1a3060;
    --accent: #3b82f6;
    --accent2:#60a5fa;
    --gold:   #f59e0b;
    --surface:#f8f9fc;
    --card:   #ffffff;
    --border: #e2e8f0;
    --text:   #0f172a;
    --muted:  #64748b;
    --success:#10b981;
    --danger: #ef4444;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

/*Sidebar*/
section[data-testid="stSidebar"] {
    background: var(--navy) !important;
    border-right: 1px solid rgba(59,130,246,0.15);
}
section[data-testid="stSidebar"] * {
    color: #c8d6f0 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.08) !important;
}

/*Main BG */
.stApp {
    background: var(--surface);
}
.main .block-container {
    padding: 2.5rem 2.8rem 3rem;
    max-width: 1280px;
}

/* Page Header */
.page-header {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy3) 100%);
    border-radius: 16px;
    padding: 2rem 2.4rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute;
    top: -60px;
    right: -60px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(59,130,246,0.12);
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 140px; height: 140px;
    border-radius: 50%;
    background: rgba(245,158,11,0.08);
}
.page-header h1 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    line-height: 1.15;
    position: relative;
    z-index: 1;
}
.page-header p {
    font-size: 0.9rem;
    color: rgba(200,214,240,0.85);
    margin: 0.5rem 0 0;
    position: relative;
    z-index: 1;
}
.page-header .badge {
    display: inline-block;
    background: rgba(59,130,246,0.25);
    border: 1px solid rgba(59,130,246,0.4);
    color: #93c5fd !important;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 0.7rem;
}

/* Nav Buttons (sidebar)*/
.nav-btn {
    display: flex;
    align-items: center;
    gap: 10px;
    background: transparent;
    border: none;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    width: 100%;
    text-align: left;
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    font-weight: 500;
    color: #8da8d4;
    transition: all 0.18s ease;
    margin-bottom: 4px;
}
.nav-btn:hover { background: rgba(59,130,246,0.12); color: #ffffff;
}
.nav-btn.active {
    background: linear-gradient(135deg, rgba(59,130,246,0.25), rgba(96,165,250,0.15));
    color: #ffffff !important;
    border: 1px solid rgba(59,130,246,0.3);
}
.nav-icon { font-size: 1rem;
}

/* Metric Cards*/
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 8px rgba(10,22,40,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(10,22,40,0.1);
}
.metric-card .label {
    font-size: 1.0rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.metric-card .value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: var(--navy);
    line-height: 1;
}

/* Section Heading */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--muted);
    font-weight: 700;
    border-bottom: 2px solid var(--border);
    padding-bottom: 0.6rem;
    margin: 2rem 0 1.2rem;
}

/* Search Box */
.stTextInput > div > div > input {
    background: #fff !important;
    border: 2px solid var(--accent) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1rem !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
    transition: box-shadow 0.2s;
}
.stTextInput > div > div > input:focus {
    box-shadow: 0 0 0 4px rgba(59,130,246,0.22) !important;
}
.stTextInput label {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: var(--navy) !important;
    letter-spacing: 0.02em;
}

/* Dataframe table header */
.stDataFrame thead th {
    background: var(--navy) !important;
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase;
    padding: 10px 14px !important;
    border: none !important;
}
.stDataFrame tbody tr:nth-child(even) {
    background: #f1f5fd !important;
}
.stDataFrame tbody tr:hover {
    background: #dbeafe !important;
}
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid var(--border) !important;
    box-shadow: 0 2px 10px rgba(10,22,40,0.07);
}

/*  Expander */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy2) 100%) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.03em;
    border: none !important;
    padding: 1rem 1.4rem !important;
}
.streamlit-expanderHeader p { color: #ffffff !important; }
.streamlit-expanderContent {
    background: #f0f5ff !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1rem 1.4rem !important;
}

/* Selectbox */
.stSelectbox label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: var(--navy) !important;
}
.stSelectbox > div > div {
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
}

/* Slider */
.stSlider label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: var(--navy) !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--accent) !important;
}

/*  Number Input  */
.stNumberInput label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: var(--navy) !important;
}

/* Button*/
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy3) 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.72rem 2.2rem !important;
    font-family: 'Plus Jakarta Sans', 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(10,22,40,0.25) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(10,22,40,0.35) !important;
    background: linear-gradient(135deg, #1a3060 0%, #2a4a80 100%) !important;
}

/* Alerts */
.stSuccess {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7) !important;
    border: 1px solid #86efac !important;
    border-radius: 10px !important;
    color: #166534 !important;
}
.stError {
    background: linear-gradient(135deg, #fef2f2, #fee2e2) !important;
    border: 1px solid #fca5a5 !important;
    border-radius: 10px !important;
    color: #991b1b !important;
}

/*  CR Pill  */
.cr-pill {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    font-weight: 500;
}
.cr-good { background: #dcfce7; color: #166534; border: 1px solid #86efac;
}
.cr-bad  { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5;
}

/*  Info Box  */
.info-box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 6px rgba(10,22,40,0.05);
}

/* Divider  */
.divider { height: 1px; background: var(--border);
margin: 2rem 0; }

/* Highlight Box */
.highlight-box {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border: 1px solid #93c5fd;
    border-radius: 12px;
    padding: 1.2rem 1.6rem;
    margin-bottom: 1rem;
}

/* Profile Detail  */
.profile-detail { font-size: 0.86rem;
color: #374151; line-height: 2.1; }
.profile-detail strong {
    color: var(--navy);
    font-weight: 600;
    min-width: 140px;
    display: inline-block;
}

/*  Multiselect  */
.stMultiSelect label {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: var(--navy) !important;
}
</style>
""", unsafe_allow_html=True)


# KONFIGURASI POOL KRITERIA
POOL_KRITERIA = {
    'Price':                    {'type': 'Cost',    'short': 'Price'},
    'Weight (inc. batteries)':  {'type': 'Cost',    'short': 'Weight'},
    'Dimensions':               {'type': 'Cost',    'short': 'Dims'},
    'Zoom wide (W)':            {'type': 'Cost',    'short': 'Zoom W'},
    'Zoom tele (T)':            {'type': 'Benefit', 'short': 'Zoom T'},
    'Effective pixels':         {'type': 'Benefit', 'short': 'Pixels'},
    'Max resolution':           {'type': 'Benefit', 'short': 'Max Res'},
    'Low resolution':           {'type': 'Benefit', 'short': 'Low Res'},
    'Normal focus range':       {'type': 'Cost',    'short': 'Norm Focus'},
    'Macro focus range':        {'type': 'Cost',    'short': 'Mac Focus'},
    'Storage included':         {'type': 'Benefit', 'short': 'Storage'},
    'Release date':             {'type': 'Benefit', 'short': 'Year'},
}


# DATA LOADER
@st.cache_data
def load_data():
    df = pd.read_csv('Projek/camera_dataset_cleaned.csv')
    numeric_cols = list(POOL_KRITERIA.keys())
    df = df.dropna(subset=numeric_cols)
    df['Price'] = df['Price'] * 17839
    return df

df = load_data()


# SESSION STATE
if 'menu' not in st.session_state:
    st.session_state.menu = "Data"
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = list(df.nsmallest(20, 'Price')['Model'].unique())
if 'selected_kriteria' not in st.session_state:
    st.session_state.selected_kriteria = [
        'Price', 'Weight (inc. batteries)', 'Dimensions',
        'Zoom wide (W)', 'Effective pixels'
    ]
if 'top_n' not in st.session_state:
    st.session_state.top_n = 10


# SIDEBAR NAVIGASI
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.4rem 0 0.8rem 0;">
        <div style="font-family:'Syne',sans-serif; font-size:1.35rem; font-weight:800;
                    color:#ffffff; line-height:1.2; letter-spacing:-0.01em;">
             SPK Kamera Digital untuk Kebutuhan Traveling/Vlog
        </div>
        <div style="font-size:0.7rem; color:#4a6a9a; letter-spacing:0.1em;
                    text-transform:uppercase; margin-top:5px; font-weight:600;">
            Analytic Hierarchy Process
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    nav_items = [
        ("", "Data",            "Jelajahi Dataset"),
        ("", "Perhitungan AHP", "Bobot & Rekomendasi"),
        ("", "Profil",          "Tentang Sistem"),
    ]

    for icon, label, desc in nav_items:
        is_active = st.session_state.menu == label
        clicked = st.button(
            f"{icon}  {label}",
            key=f"nav_{label}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        )
        if clicked:
            st.session_state.menu = label
            st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem; color:#3a5a8a; line-height:1.9;'>"
        "Dataset &nbsp;<b style='color:#6090c0'>Camera Digital</b><br>"
        f"Alternatif &nbsp;<b style='color:#6090c0'>{len(df)} kamera</b><br>"
        f"Kriteria &nbsp;<b style='color:#6090c0'>12 tersedia</b><br>"
        f"Filter aktif &nbsp;<b style='color:#60a5fa'>{len(st.session_state.selected_models)} kamera</b>"
        "</div>",
        unsafe_allow_html=True
    )

menu = st.session_state.menu

# HALAMAN 1 — DATA
if menu == "Data":

    st.markdown("""
    <div class="page-header">
        <div class="badge"> Dataset</div>
        <h1>Dataset Kamera Digital</h1>
        <p>Spesifikasi teknis dari berbagai model kamera yang tersedia sebagai alternatif keputusan.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("", "Total Alternatif", len(df)),
        ("", "Total Kriteria",   len(POOL_KRITERIA)),
        ("", "Tahun Awal",       int(df['Release date'].min())),
        ("", "Tahun Akhir",      int(df['Release date'].max())),
    ]
    for col, (icon, label, val) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="icon">{icon}</div>
                <div class="label">{label}</div>
                <div class="value">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Filter & Pencarian Data</div>', unsafe_allow_html=True)

    col_search, col_brand = st.columns([2, 2])
    with col_search:
        search = st.text_input(
            "Cari Model Kamera",
            placeholder="Ketik nama kamera, mis: Canon, Nikon...",
            help="Pencarian tidak sensitif huruf besar/kecil"
        )
    with col_brand:
        year_range = st.slider(
            "Filter Tahun Rilis",
            int(df['Release date'].min()),
            int(df['Release date'].max()),
            (int(df['Release date'].min()), int(df['Release date'].max())),
            help="Seret untuk memfilter rentang tahun rilis kamera"
        )

    col_px, col_price = st.columns(2)
    with col_px:
        min_px = st.number_input(
            "Minimum Effective Pixels (MP)",
            min_value=float(df['Effective pixels'].min()),
            max_value=float(df['Effective pixels'].max()),
            value=float(df['Effective pixels'].min()),
            step=1.0,
            help="Filter kamera berdasarkan resolusi minimum"
        )
    with col_price:
        max_price = st.number_input(
            "Maksimum Harga (Rp)",
            min_value=float(df['Price'].min()),
            max_value=float(df['Price'].max()),
            value=float(df['Price'].max()),
            step=1000000.0,  # Mengubah step menjadi 1 juta rupiah
            help="Filter kamera berdasarkan batas harga maksimum"
        )

    display_df = df.copy()
    if search:
        display_df = display_df[display_df['Model'].str.contains(search, case=False, na=False)]
    display_df = display_df[
        (display_df['Release date'] >= year_range[0]) &
        (display_df['Release date'] <= year_range[1]) &
        (display_df['Effective pixels'] >= min_px) &
        (display_df['Price'] <= max_price)
    ]

    st.markdown(f"""
    <div class="highlight-box">
        <span style="font-size:0.85rem; color:#1e40af; font-weight:600;">
            Menampilkan <b>{len(display_df)}</b> dari <b>{len(df)}</b> kamera
        </span>
        <span style="font-size:0.8rem; color:#3b82f6; margin-left:1rem;">
            {'(semua data)' if len(display_df)==len(df) else '(difilter)'}
        </span>
    </div>
    """, unsafe_allow_html=True)

    format_dict = {
        "Price": "Rp {:,.0f}",
        "Release date": "{:.0f}",
        "Effective pixels": "{:.1f}",
        "Weight (inc. batteries)": "{:.0f}"
    }

    st.dataframe(
        display_df.reset_index(drop=True).style.format(format_dict, na_rep="-"),
        use_container_width=True,
        height=500,
    )


# HALAMAN 2 — PERHITUNGAN AHP
elif menu == "Perhitungan AHP":

    st.markdown("""
    <div class="page-header">
        <div class="badge">AHP</div>
        <h1>Perhitungan AHP</h1>
        <p>Tentukan kriteria dan bobot prioritas melalui perbandingan berpasangan skala Saaty secara dinamis.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">1. Konfigurasi Alternatif & Kriteria</div>', unsafe_allow_html=True)

    #LANGKAH 1 PEMILIHAN KRITERIA DAN ALTERNATIF
    with st.expander("Konfigurasi Sistem Pendukung Keputusan", expanded=True):
        st.markdown("**A. Pilih Kriteria Penilaian (Wajib 5)**")

        selected_kriteria = st.multiselect(
            "Pilih tepat 5 kriteria untuk membentuk matriks perbandingan 5x5:",
            options=list(POOL_KRITERIA.keys()),
            default=st.session_state.get('selected_kriteria', []),
            max_selections=5,
            key="kriteria_multiselect"
        )

        if selected_kriteria != st.session_state.get('selected_kriteria', []):
            st.session_state.selected_kriteria = selected_kriteria

        st.markdown("<br>**B. Filter Tahun & Pilih Alternatif Kamera**", unsafe_allow_html=True)
        
        rentang_tahun = st.slider(
            "Filter batas tahun rilis kamera:",
            int(df['Release date'].min()),
            int(df['Release date'].max()),
            (int(df['Release date'].min()), int(df['Release date'].max())),
            key="ahp_year_filter"
        )
        
        df_ahp_filtered = df[(df['Release date'] >= rentang_tahun[0]) & (df['Release date'] <= rentang_tahun[1])]

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("Top 20 Termurah (Sesuai Tahun)", use_container_width=True, key="btn_termurah"):
                st.session_state.models_multiselect = list(df_ahp_filtered.nsmallest(20, 'Price')['Model'].unique())

        with col_btn2:
            if st.button("Top 20 Resolusi Tinggi (Sesuai Tahun)", use_container_width=True, key="btn_resolusi"):
                st.session_state.models_multiselect = list(df_ahp_filtered.nlargest(20, 'Effective pixels')['Model'].unique())

        col_a1, col_a2 = st.columns([3, 1])
        with col_a1:
            all_models_filtered = list(df_ahp_filtered['Model'].unique())
            current_defaults = [m for m in st.session_state.get('models_multiselect', st.session_state.get('selected_models', [])) if m in all_models_filtered]

            def on_models_change():
                pass

            selected_models = st.multiselect(
                "Pilih/hapus kamera secara manual:",
                options=all_models_filtered,
                default=current_defaults,
                key="models_multiselect",
                on_change=on_models_change
            )
            st.session_state.selected_models = selected_models

        with col_a2:
            top_n = st.slider(
                "Top N Hasil",
                min_value=5,
                max_value=50,
                value=st.session_state.get('top_n', 10),
                step=5,
                key="top_n_slider"
            )
            st.session_state.top_n = top_n

        # Ambil data alternatif yang fix dipilih
        df_sel = df[df['Model'].isin(selected_models)].copy()

        st.markdown(f"""
        <div style="margin-top:0.8rem; margin-bottom:0.5rem;">
            <span class="cr-pill cr-good">{len(df_sel)} alternatif aktif</span>
            <span class="cr-pill {'cr-good' if len(selected_kriteria) == 5 else 'cr-bad'}">
                {len(selected_kriteria)}/5 kriteria terpilih
            </span>
        </div>
        """, unsafe_allow_html=True)

    if len(df_sel) < 2:
        st.error("Pilih minimal 2 kamera sebagai alternatif untuk melanjutkan.")
        st.stop()
    if len(selected_kriteria) != 5:
        st.warning("Anda wajib memilih tepat 5 kriteria untuk melanjutkan perhitungan matriks 5x5.")
        st.stop()


    with st.expander("Panduan Memahami Istilah Kriteria (Kamus Data)", expanded=False):
        st.markdown("""
<div style="font-size:0.85rem; color:#374151; line-height:1.8; margin-bottom:1rem;">
Agar penilaian perbandingan Anda lebih objektif, berikut adalah arti dari masing-masing kriteria teknis beserta sifat penilainya:
</div>

**Kategori Benefit (Semakin besar nilainya, semakin bagus):**
* **Zoom tele (T)**: Jangkauan zoom maksimal. Semakin besar angkanya, semakin jauh objek yang bisa difoto tanpa pecah.
* **Effective pixels**: Resolusi sensor kamera utama. Semakin tinggi (MP), gambar semakin tajam dan detail.
* **Max resolution**: Ukuran maksimal foto yang bisa dihasilkan. Penting jika Anda ingin mencetak foto ukuran besar.
* **Low resolution**: Opsi resolusi terendah. Berguna untuk menghemat kapasitas penyimpanan memori.
* **Storage included**: Kapasitas memori penyimpanan bawaan dari pabrik.
* **Release date**: Tahun rilis. Semakin baru tahunnya, biasanya membawa teknologi dan fitur prosesor gambar yang lebih mutakhir.

**Kategori Cost (Semakin kecil nilainya, semakin bagus):**
* **Price**: Harga beli kamera. Tentu saja, semakin murah semakin menguntungkan anggaran Anda.
* **Weight**: Berat fisik kamera (termasuk baterai). Semakin ringan, semakin nyaman dibawa bepergian (*travel-friendly*).
* **Dimensions**: Ukuran fisik kamera. Semakin kecil angkanya, kamera semakin ringkas dan tidak memakan tempat.
* **Zoom wide (W)**: Sudut pandang terlebar lensa. Angka yang *lebih kecil* berarti bidang pandang lebih luas, sangat cocok untuk foto pemandangan/landscape.
* **Normal focus range**: Jarak fokus normal minimum. Semakin dekat angkanya, semakin cepat kamera mengunci fokus pada jarak standar.
* **Macro focus range**: Jarak fokus khusus makro minimum. Semakin kecil angkanya, semakin dekat kamera bisa memotret objek kecil (seperti serangga atau detail perhiasan).
        """, unsafe_allow_html=True)


    #LANGKAH 2 INPUT PERBANDINGAN BERPASANGAN (PAIRWISE COMPARISON)
    st.markdown('<div class="section-heading">2. Perbandingan Berpasangan Kriteria</div>', unsafe_allow_html=True)

    saaty_scale = {
        "9 — Kiri mutlak lebih penting":                        9.0,
        "8 — Kiri di antara sangat dan mutlak lebih penting":   8.0,
        "7 — Kiri sangat lebih penting":                        7.0,
        "6 — Kiri di antara lebih dan sangat lebih penting":    6.0,
        "5 — Kiri lebih penting":                               5.0,
        "4 — Kiri di antara sedikit dan lebih penting":         4.0,
        "3 — Kiri sedikit lebih penting":                       3.0,
        "2 — Kiri di antara sama dan sedikit lebih penting":    2.0,
        "1 — Sama penting":                                     1.0,
        "1/2 — Kanan di antara sama dan sedikit lebih penting": 1/2,
        "1/3 — Kanan sedikit lebih penting":                    1/3,
        "1/4 — Kanan di antara sedikit dan lebih penting":      1/4,
        "1/5 — Kanan lebih penting":                            1/5,
        "1/6 — Kanan di antara lebih dan sangat lebih penting": 1/6,
        "1/7 — Kanan sangat lebih penting":                     1/7,
        "1/8 — Kanan di antara sangat dan mutlak lebih penting":1/8,
        "1/9 — Kanan mutlak lebih penting":                     1/9,
    }

    pasangan = [
        (selected_kriteria[i], selected_kriteria[j])
        for i in range(len(selected_kriteria))
        for j in range(i + 1, len(selected_kriteria))
    ]

    bobot_input = {}
    st.markdown(
        "<div style='font-size:0.82rem; color:#374151; padding:0.5rem 0 1rem;'>"
        "Pilih nilai untuk setiap pasang kriteria. Skala Saaty 1–9 mencerminkan "
        "tingkat kepentingan relatif antar kriteria."
        "</div>",
        unsafe_allow_html=True
    )

    for i in range(0, len(pasangan), 2):
        col1, col2 = st.columns(2, gap="large")
        k1_a, k1_b = pasangan[i]
        with col1:
            st.markdown(f"<small style='color:#64748b;font-size:0.75rem;'>Perbandingan {i+1}</small>", unsafe_allow_html=True)
            val1 = st.selectbox(
                f"**{k1_a}** vs  **{k1_b}**",
                list(saaty_scale.keys()),
                index=8, key=f"sel_{i}"
            )
            bobot_input[pasangan[i]] = saaty_scale[val1]

        if i + 1 < len(pasangan):
            k2_a, k2_b = pasangan[i + 1]
            with col2:
                st.markdown(f"<small style='color:#64748b;font-size:0.75rem;'>Perbandingan {i+2}</small>", unsafe_allow_html=True)
                val2 = st.selectbox(
                    f"**{k2_a}** vs  **{k2_b}**",
                    list(saaty_scale.keys()),
                    index=8, key=f"sel_{i+1}"
                )
                bobot_input[pasangan[i + 1]] = saaty_scale[val2]

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col_btn, col_info = st.columns([2, 3])
    with col_btn:
        run = st.button("Hitung Rekomendasi Kamera", type="primary", use_container_width=True)
    with col_info:
        st.markdown(f"""
        <div style="padding:0.6rem; font-size:0.82rem; color:#64748b;">
            Akan memproses <b style="color:#0a1628">{len(df_sel)}</b> alternatif kamera
            menggunakan matriks berukuran <b style="color:#0a1628">5 x 5</b>.
        </div>
        """, unsafe_allow_html=True)

    if run:

        #LANGKAH 3 MEMBANGUN MATRIKS PERBANDINGAN BERPASANGAN
        n = 5
        matriks = np.ones((n, n))
        idx = 0
        for i in range(n):
            for j in range(i + 1, n):
                val = bobot_input[pasangan[idx]]
                matriks[i, j] = val
                matriks[j, i] = 1.0 / val
                idx += 1

        #LANGKAH 4MENGHITUNG JUMLAH TIAP KOLOM
        kolom_sum = matriks.sum(axis=0)

        #LANGKAH 5NORMALISASI MATRIKS
        matriks_norm = matriks / kolom_sum

        #ANGKAH 6MENGHITUNG EIGEN VECTOR (BOBOT PRIORITAS)
        eigen_vector = matriks_norm.mean(axis=1)

        #LANGKAH 7MENGHITUNG LAMBDA MAX
        lambda_max = (kolom_sum * eigen_vector).sum()

        #LANGKAH 8 MENGHITUNG CONSISTENCY INDEX (CI)
        CI = (lambda_max - n) / (n - 1)

        #LANGKAH 9CONSISTENCY RATIO (CR)
        RI = 1.12
        CR = CI / RI if RI != 0 else 0

        st.markdown('<div class="section-heading">Analisis Matriks & Bobot Kriteria</div>', unsafe_allow_html=True)

        col_valid, col_bobot = st.columns([1, 1], gap="large")

        with col_valid:
            cr_class = "cr-good" if CR <= 0.1 else "cr-bad"
            cr_label = "KONSISTEN" if CR <= 0.1 else "TIDAK KONSISTEN"
            st.markdown(f"""
            <div class="info-box" style="padding: 1.2rem; text-align: center;">
                <h4 style="margin: 0; color: #1a3060;">Validasi Consistency Ratio (CR)</h4>
                <div style="font-family: 'DM Mono', monospace; font-size: 2.2rem; font-weight: bold;
                            color: {'#10b981' if CR <= 0.1 else '#ef4444'};">
                    {CR:.4f}
                </div>
                <div class="cr-pill {cr_class}" style="margin-top: 0.5rem; font-size:0.9rem;">
                    {cr_label}
                </div>
                <p style="font-size: 0.8rem; color: #64748b; margin-top: 0.8rem;">
                    Syarat matematis: Nilai CR harus kurang dari atau sama dengan 0.1 (CR ≤ 0.1)
                    agar pembobotan dianggap rasional dan dapat diandalkan.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col_bobot:
            df_bobot = (
                pd.DataFrame({"Kriteria": selected_kriteria, "Bobot": eigen_vector})
                .sort_values("Bobot", ascending=False)
                .reset_index(drop=True)
            )
            df_bobot.index += 1
            st.dataframe(
                df_bobot.style
                    .format({"Bobot": "{:.4f}"})
                    .bar(subset=["Bobot"], color="#1a3060", vmin=0, vmax=1),
                use_container_width=True, height=210
            )

        with st.expander("Lihat Detail Matriks Perbandingan Berpasangan (Heatmap)", expanded=False):
            df_matriks = pd.DataFrame(matriks, index=selected_kriteria, columns=selected_kriteria)
            st.dataframe(df_matriks.style.format("{:.3f}").background_gradient(
                cmap='Blues', axis=None, vmin=0.1
            ), use_container_width=True)

        #TABEL NORMALISASI MATRIKS
        with st.expander("Lihat Detail Normalisasi Matriks & Perhitungan Bobot", expanded=False):

            st.markdown(
                "<div style='font-size:0.82rem; font-weight:600; color:#0a1628; "
                "margin-bottom:0.4rem;'>Matriks Perbandingan Berpasangan (Original)</div>",
                unsafe_allow_html=True
            )
            df_matriks_raw = pd.DataFrame(
                matriks,
                index=selected_kriteria,
                columns=selected_kriteria
            )
            st.dataframe(
                df_matriks_raw.style.format("{:.4f}").background_gradient(
                    cmap='Blues', axis=None, vmin=0.1
                ),
                use_container_width=True,
                height=215
            )

            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

            st.markdown(
                "<div style='font-size:0.82rem; font-weight:600; color:#0a1628; "
                "margin-bottom:0.4rem;'>Jumlah Tiap Kolom (pembagi normalisasi)</div>",
                unsafe_allow_html=True
            )
            df_kolom_sum = pd.DataFrame(
                [kolom_sum],
                columns=selected_kriteria,
                index=["Jumlah Kolom"]
            )
            st.dataframe(
                df_kolom_sum.style.format("{:.4f}").background_gradient(
                    cmap='Oranges', axis=None
                ),
                use_container_width=True,
                height=80
            )

            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

            st.markdown(
                "<div style='font-size:0.82rem; font-weight:600; color:#0a1628; "
                "margin-bottom:0.4rem;'>Matriks Ternormalisasi + Bobot Prioritas (Rata-rata Baris)</div>",
                unsafe_allow_html=True
            )
            df_norm_display = pd.DataFrame(
                matriks_norm,
                index=selected_kriteria,
                columns=selected_kriteria
            )
            df_norm_display["Bobot (Rata-rata Baris)"] = eigen_vector
            st.dataframe(
                df_norm_display.style
                    .format("{:.4f}")
                    .background_gradient(subset=["Bobot (Rata-rata Baris)"], cmap="Greens")
                    .background_gradient(subset=selected_kriteria, cmap="Blues", axis=None),
                use_container_width=True,
                height=215
            )

            st.markdown(
                "<div style='font-size:0.78rem; color:#64748b; margin-top:0.5rem;'>"
                "Catatan: Jumlah seluruh nilai pada kolom Bobot = 1.0 (100%). "
                "Nilai ini adalah eigen vector yang dipakai sebagai bobot di seluruh tahap selanjutnya."
                "</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            '<div class="section-heading">Transparansi Perhitungan Consistency Ratio (CR)</div>',
            unsafe_allow_html=True
        )

        col_cr1, col_cr2 = st.columns(2, gap="large")

        with col_cr1:
            # Rincian perhitungan lambda_max per elemen (dot product)
            lmax_detail = " + ".join(
                "({ks:.3f} x {ev:.4f})".format(ks=kolom_sum[i], ev=eigen_vector[i])
                for i in range(n)
            )

            html_cr1 = (
                '<div class="info-box">'
                '<div style="font-size:0.82rem; color:#374151; line-height:2.2;">'

                '<b style="color:#0a1628; font-size:0.85rem;">'
                'Langkah 1 &mdash; Hitung &lambda;<sub>max</sub>'
                '</b><br>'
                '<span style="color:#64748b; font-size:0.78rem;">'
                '&lambda;<sub>max</sub> = &Sigma; (Jumlah Kolom &times; Bobot Prioritas)'
                '</span><br>'
                '<span style="font-family:monospace; font-size:0.76rem; color:#1e40af;">'
                '= ' + lmax_detail +
                '</span><br>'
                '<b>&lambda;<sub>max</sub> = ' + '{:.4f}'.format(lambda_max) + '</b>'

                '<br><br>'

                '<b style="color:#0a1628; font-size:0.85rem;">'
                'Langkah 2 &mdash; Hitung CI (Consistency Index)'
                '</b><br>'
                '<span style="color:#64748b; font-size:0.78rem;">'
                'CI = (&lambda;<sub>max</sub> &minus; n) / (n &minus; 1)'
                '&nbsp;|&nbsp; n = ukuran matriks = ' + str(n) +
                '</span><br>'
                '<span style="font-family:monospace; font-size:0.76rem; color:#1e40af;">'
                '= (' + '{:.4f}'.format(lambda_max) + ' &minus; ' + str(n) + ')'
                ' / (' + str(n) + ' &minus; 1)<br>'
                '= ' + '{:.4f}'.format(lambda_max - n) + ' / ' + str(n - 1) +
                '</span><br>'
                '<b>CI = ' + '{:.4f}'.format(CI) + '</b>'

                '<br><br>'

                '<b style="color:#0a1628; font-size:0.85rem;">'
                'Langkah 3 &mdash; Nilai RI (Random Index)'
                '</b><br>'
                '<span style="color:#64748b; font-size:0.78rem;">'
                'RI adalah nilai rata-rata konsistensi acak untuk matriks n&times;n.<br>'
                'Nilainya tetap dan diambil dari tabel Saaty.<br>'
                'Untuk n = 5 &rarr; <b>RI = ' + str(RI) + '</b>'
                '</span><br>'
                '<b>RI = ' + str(RI) + '</b>'

                '</div>'
                '</div>'
            )
            st.markdown(html_cr1, unsafe_allow_html=True)

        with col_cr2:
            cr_color      = "#10b981" if CR <= 0.1 else "#ef4444"
            cr_status     = "KONSISTEN" if CR <= 0.1 else "TIDAK KONSISTEN"
            cr_bg         = "#f0fdf4" if CR <= 0.1 else "#fef2f2"
            cr_border     = "#86efac" if CR <= 0.1 else "#fca5a5"
            cr_keterangan = (
                "Perbandingan berpasangan yang dilakukan dinilai konsisten "
                "secara matematis dan dapat diterima untuk proses pengambilan keputusan."
                if CR <= 0.1 else
                "Nilai CR melebihi batas 0.10. Silakan tinjau ulang perbandingan "
                "berpasangan pada Langkah 2 agar lebih konsisten."
            )

            html_cr2 = (
                '<div class="info-box">'
                '<div style="font-size:0.82rem; color:#374151; line-height:2.2;">'
                '<b style="color:#0a1628; font-size:0.85rem;">'
                'Langkah 4 &mdash; Hitung CR (Consistency Ratio)'
                '</b><br>'
                '<span style="color:#64748b; font-size:0.78rem;">'
                'CR = CI / RI &nbsp;&rarr;&nbsp; Syarat konsistensi: CR &le; 0.10'
                '</span><br>'
                '<span style="font-family:monospace; font-size:0.76rem; color:#1e40af;">'
                '= ' + '{:.4f}'.format(CI) + ' / ' + str(RI) + '<br>'
                '= ' + '{:.4f}'.format(CR) +
                '</span>'
                '</div>'

                '<div style="text-align:center; padding:1.2rem 0.5rem; margin-top:0.8rem;'
                ' background:' + cr_bg + '; border:1px solid ' + cr_border + ';'
                ' border-radius:12px;">'
                '<div style="font-family:monospace; font-size:2rem;'
                ' font-weight:bold; color:' + cr_color + ';">'
                'CR = ' + '{:.4f}'.format(CR) +
                '</div>'
                '<div style="font-size:0.85rem; font-weight:700;'
                ' color:' + cr_color + '; margin-top:0.3rem;">'
                + cr_status +
                '</div>'
                '<div style="font-size:0.78rem; color:#64748b;'
                ' margin-top:0.6rem; padding:0 1rem;">'
                + cr_keterangan +
                '</div>'
                '</div>'

                '<div style="font-size:0.78rem; color:#64748b; margin-top:1rem;'
                ' line-height:1.9; padding:0.6rem 0.8rem;'
                ' background:#f8f9fc; border-radius:8px;'
                ' border:1px solid #e2e8f0;">'
                '<b style="color:#374151;">Referensi Tabel RI (Saaty, 1980):</b><br>'
                'n=1 &rarr; 0.00 &nbsp;|&nbsp; n=2 &rarr; 0.00 &nbsp;|&nbsp;'
                'n=3 &rarr; 0.58 &nbsp;|&nbsp; n=4 &rarr; 0.90<br>'
                '<b>n=5 &rarr; ' + str(RI) + '</b> &nbsp;|&nbsp;'
                'n=6 &rarr; 1.24 &nbsp;|&nbsp;'
                'n=7 &rarr; 1.32 &nbsp;|&nbsp;'
                'n=8 &rarr; 1.41'
                '</div>'
                '</div>'
            )
            st.markdown(html_cr2, unsafe_allow_html=True)

        if CR > 0.1:
            st.error("Nilai CR melebihi 0.1. Silakan tinjau ulang perbandingan di Langkah 2 agar lebih konsisten.")
            st.stop()

        #LANGKAH 10 NORMALISASI NILAI ALTERNATIF PER KRITERIA
        df_k = df_sel.copy()
        for i, k in enumerate(selected_kriteria):
            k_type = POOL_KRITERIA[k]['type']
            if k_type == 'Cost':
                df_k[f'norm_{k}'] = df_k[k].min() / df_k[k]
            else:
                df_k[f'norm_{k}'] = df_k[k] / df_k[k].max()

        #LANGKAH 11 HITUNG SKOR AKHIR (WEIGHTED SUM)
        df_k['Skor Akhir'] = sum(
            df_k[f'norm_{k}'] * eigen_vector[i]
            for i, k in enumerate(selected_kriteria)
        )


        # TABEL PERHITUNGAN SAW
        with st.expander("Lihat Detail Normalisasi Data & Perhitungan Akhir (Metode SAW)", expanded=False):
            
            st.markdown(
                "<div style='font-size:0.82rem; font-weight:600; color:#0a1628; margin-bottom:0.4rem;'>"
                "Langkah 1: Matriks Keputusan (Data Asli)</div>",
                unsafe_allow_html=True
            )
            df_asli = df_k[['Model'] + selected_kriteria].copy()
            df_asli.index = range(1, len(df_asli) + 1)
            st.dataframe(df_asli, use_container_width=True)

            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

            st.markdown(
                "<div style='font-size:0.82rem; font-weight:600; color:#0a1628; margin-bottom:0.4rem;'>"
                "Langkah 2: Matriks Normalisasi (R)</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div style='font-size:0.75rem; color:#64748b; margin-bottom:0.8rem;'>"
                "• <b>Atribut Benefit</b> (Makin besar makin baik): <i>Nilai / Nilai Max Kolom</i><br>"
                "• <b>Atribut Cost</b> (Makin kecil makin baik): <i>Nilai Min Kolom / Nilai</i>"
                "</div>",
                unsafe_allow_html=True
            )
            
            norm_cols = [f'norm_{k}' for k in selected_kriteria]
            df_norm_saw = df_k[['Model'] + norm_cols].copy()
            
            rename_dict = {f'norm_{k}': k for k in selected_kriteria}
            df_norm_saw.rename(columns=rename_dict, inplace=True)
            df_norm_saw.index = range(1, len(df_norm_saw) + 1)
            
            st.dataframe(
                df_norm_saw.style
                .format({k: "{:.4f}" for k in selected_kriteria})
                .background_gradient(cmap="Blues", axis=None), 
                use_container_width=True
            )
            
            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
            
            st.markdown(
                "<div style='font-size:0.82rem; font-weight:600; color:#0a1628; margin-bottom:0.4rem;'>"
                "Langkah 3: Perhitungan Skor Akhir (Pembobotan)</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div style='font-size:0.75rem; color:#64748b; margin-bottom:0.8rem;'>"
                "Mengalikan setiap nilai pada Matriks Normalisasi (R) dengan Bobot Prioritas (W) dari AHP.<br>"
                "<b>Skor Akhir (V) = &Sigma; (R &times; W)</b>"
                "</div>",
                unsafe_allow_html=True
            )
            
            #dataframe untuk menampilkan hasil R x W
            df_skor = df_k[['Model']].copy()
            for i, k in enumerate(selected_kriteria):
                #mencantumkan bobot pengalinya
                nama_kolom = f"{k} (× {eigen_vector[i]:.3f})"
                df_skor[nama_kolom] = df_k[f'norm_{k}'] * eigen_vector[i]
                
            df_skor['Skor Akhir'] = df_k['Skor Akhir']
            df_skor.index = range(1, len(df_skor) + 1)
            
            
            format_skor = {col: "{:.4f}" for col in df_skor.columns if col != 'Model'}
            
            st.dataframe(
                df_skor.style
                .format(format_skor)
                .background_gradient(subset=['Skor Akhir'], cmap="Greens")
                .background_gradient(subset=[col for col in df_skor.columns if col not in ['Model', 'Skor Akhir']], cmap="Blues", axis=None), 
                use_container_width=True
            )

        #LANGKAH 12 PERANKINGAN ALTERNATIF
        df_hasil = (
            df_k[['Model'] + selected_kriteria + ['Skor Akhir']]
            .sort_values('Skor Akhir', ascending=False)
            .reset_index(drop=True)
        )
        df_hasil.index += 1

        st.markdown(f'<div class="section-heading">Peringkat Alternatif (Top {top_n})</div>', unsafe_allow_html=True)

        top3   = df_hasil.head(3)
        medals = ["1", "2", "3"]
        c1, c2, c3 = st.columns(3)
        for col, (_, row), medal in zip([c1, c2, c3], top3.iterrows(), medals):
            with col:
                st.markdown(f"""
                <div class="metric-card" style="border-left:4px solid #1a3060; text-align:center;">
                    <div style="font-size:2rem;">{medal}</div>
                    <div class="label" style="margin-top:0.4rem;">Peringkat #{row.name}</div>
                    <div style="font-family:'Syne',sans-serif; font-size:0.95rem;
                                font-weight:700; color:#0a1628; margin:0.4rem 0;">
                        {row['Model'][:28]}
                    </div>
                    <div style="font-family:'DM Mono',monospace; font-size:1.1rem;
                                font-weight:600; color:#3b82f6;">
                        {row['Skor Akhir']:.5f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(
            df_hasil.head(top_n).style.format({"Skor Akhir": "{:.5f}"})
                .background_gradient(subset=["Skor Akhir"], cmap="Blues"),
            use_container_width=True,
            height=400,
        )

        st.markdown(f'<div class="section-heading">Visualisasi Top {min(top_n, 10)} Rekomendasi</div>', unsafe_allow_html=True)

        top_vis = df_hasil.head(min(top_n, 10)).sort_values('Skor Akhir', ascending=True)
        n_bars  = len(top_vis)

        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.patch.set_facecolor('#0a1628')

        ax = axes[0]
        ax.set_facecolor('#0f1e38')

        cmap   = LinearSegmentedColormap.from_list('navy_blue', ['#1e3a6e', '#60a5fa'], N=n_bars)
        colors = [cmap(i / max(n_bars - 1, 1)) for i in range(n_bars)]

        bars = ax.barh(
            range(n_bars),
            top_vis['Skor Akhir'].values,
            color=colors,
            height=0.62,
            edgecolor='none',
        )

        for i, (bar, val) in enumerate(zip(bars, top_vis['Skor Akhir'].values)):
            ax.barh(
                bar.get_y() + bar.get_height() / 2,
                bar.get_width(),
                height=0.08,
                color='#93c5fd',
                alpha=0.4,
                edgecolor='none',
            )
            ax.text(
                bar.get_width() + 0.001,
                bar.get_y() + bar.get_height() / 2,
                f"{val:.4f}",
                va='center', ha='left',
                fontsize=8.5, color='#93c5fd',
                fontfamily='monospace', fontweight='bold'
            )

        model_labels = [m[:22] + '…' if len(m) > 22 else m for m in top_vis['Model'].values]
        ax.set_yticks(range(n_bars))
        ax.set_yticklabels(model_labels, fontsize=9, color='#c8d6f0')
        ax.tick_params(axis='x', colors='#4a6a9a', labelsize=8)
        ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
        ax.xaxis.grid(True, color='#1e3a5f', linestyle='--', linewidth=0.6)
        ax.set_axisbelow(True)
        ax.set_xlabel('Skor Preferensi', fontsize=9, color='#4a6a9a', labelpad=8)
        ax.set_title(
            f'Top {n_bars} Rekomendasi Kamera',
            fontsize=12, fontweight='bold', color='#ffffff',
            pad=14, loc='left', fontfamily='monospace'
        )

        ax2 = axes[1]
    
        k_labels_short = [POOL_KRITERIA[k]['short'] for k in selected_kriteria]

        colors_donut = ['#1e3a8a', '#2563eb', '#3b82f6', '#60a5fa', '#f59e0b']

        wedges, texts, autotexts = ax2.pie(
            eigen_vector, 
            labels=k_labels_short, 
            autopct='%1.1f%%',
            startangle=140, 
            colors=colors_donut,
            textprops=dict(color="#c8d6f0", fontsize=9.5, fontweight='600'),
    
            wedgeprops=dict(width=0.35, edgecolor='#0a1628', linewidth=3)
        )

        for autotext in autotexts:
            autotext.set_color('#ffffff')
            autotext.set_fontsize(8.5)
            autotext.set_weight('bold')

        ax2.set_title(
            'Proporsi Bobot Kriteria',
            fontsize=12, fontweight='bold', color='#ffffff',
            pad=20, fontfamily='monospace'
        )

        fig.tight_layout(pad=3)
        st.pyplot(fig)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Export Hasil Keputusan</div>', unsafe_allow_html=True)
        
        col_dl, col_dl_info = st.columns([1, 2])
        
        with col_dl:
            df_export = df_hasil.head(top_n).copy()
            csv_data = df_export.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="Unduh Laporan Rekomendasi (CSV)",
                data=csv_data,
                file_name='laporan_spk_kamera.csv',
                mime='text/csv',
                use_container_width=True,
                type="primary"
            )
            
        with col_dl_info:
            st.markdown(f"""
            <div style="font-size:0.85rem; color:#64748b; padding-top:0.4rem;">
                Unduh hasil perhitungan ini dalam format <b>.csv</b> untuk dibuka di Microsoft Excel atau Google Sheets. 
                Data yang diexport mencakup <b>Top {top_n}</b> kamera beserta nilai kriteria dan skor akhir AHP.
            </div>
            """, unsafe_allow_html=True)


# HALAMAN 3 — PROFIL
elif menu == "Profil":

    st.markdown("""
    <div class="page-header">
        <div class="badge">Profil</div>
        <h1>Profil Pengembang</h1>
        <p>Informasi pengembang sistem pendukung keputusan kamera digital berbasis AHP.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Identitas Pengembang</div>', unsafe_allow_html=True)

    col_img, col_info = st.columns([1, 3], gap="large")
    with col_img:
        st.image("Projek/ea1.jpg", width=130)
    with col_info:
        st.markdown("""
        <div class="profile-detail">
            <strong>Nama</strong> Mufid Dhamarjati Kusuma<br>
            <strong>NIM</strong> 123240171<br>
            <strong>Peran</strong> Developer<br>
            <strong>Program Studi</strong> Informatika<br>
        </div>
        """, unsafe_allow_html=True)

    col_img, col_info = st.columns([1, 3], gap="large")
    with col_img:
        st.image("Projek/ea.jpg", width=130)
    with col_info:
        st.markdown("""
        <div class="profile-detail">
            <strong>Nama</strong> Munadhil Mutawakkil<br>
            <strong>NIM</strong> 123240154<br>
            <strong>Peran</strong> Developer<br>
            <strong>Program Studi</strong> Informatika<br>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Tentang Sistem</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown("""
        <div class="info-box">
            <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em; color:#9ca3af;font-weight:600;margin-bottom:0.7rem;">Arsitektur Metode</div>
            <div style="font-size:0.88rem;color:#374151;line-height:1.8;">
                Sistem ini mengimplementasikan arsitektur hibrida <b>AHP-SAW</b>. Metode <b>Analytic Hierarchy Process (AHP)</b> digunakan pada tahap awal untuk menerjemahkan preferensi subjektif pengguna ke dalam bobot prioritas yang konsisten. Setelah bobot didapatkan, metode <b>Simple Additive Weighting (SAW)</b> mengeksekusi data spesifikasi kuantitatif kamera secara objektif. Penggabungan ini menghasilkan keputusan yang akurat dan efisien secara komputasi.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="info-box">
            <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                        color:#9ca3af;font-weight:600;margin-bottom:0.7rem;">Kriteria Dinamis</div>
            <div style="font-size:0.88rem;color:#374151;line-height:1.8;">
                Sistem beroperasi secara dinamis di mana pengguna diwajibkan memilih <b>5 kriteria</b> prioritas dari <b>12 atribut</b> yang tersedia. Sistem secara otomatis mengenali sifat kriteria, apakah itu atribut <i>Cost</i> (semakin kecil semakin baik) atau <i>Benefit</i> (semakin besar semakin baik), untuk proses normalisasi pada tahap perhitungan SAW.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                    color:#9ca3af;font-weight:600;margin-bottom:0.7rem;">Teknologi</div>
        <div style="font-size:0.88rem;color:#374151;line-height:1.8;">
            Dibangun menggunakan <b>Python</b>, <b>Streamlit</b>, <b>Pandas</b>,
            <b>NumPy</b>, dan <b>Matplotlib</b> sebagai bagian dari tugas proyek akhir
            mata kuliah Praktikum Sistem Pendukung Keputusan.
        </div>
    </div>
    """, unsafe_allow_html=True)
