import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, shapiro, normaltest
import math
import re
import warnings
import base64
warnings.filterwarnings('ignore')

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Survey Data Analyzer", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# -------------------------
# LOAD BACKGROUND VIDEO
# -------------------------
def get_base64_video(video_path):
    """Convert video to base64 string"""
    try:
        with open(video_path, "rb") as video_file:
            return base64.b64encode(video_file.read()).decode()
    except FileNotFoundError:
        return None

# Ganti 'bganm.mp4' dengan nama file video Anda
bg_video = get_base64_video('bganm.mp4')

def get_base64_image(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None
# -------------------------
# LANGUAGE SYSTEM
# -------------------------
if 'language' not in st.session_state:
    st.session_state.language = "Indonesia"

texts = {
    "home": {"Indonesia": "Beranda", "English": "Home", "Chinese": "主页"},
    "browse": {"Indonesia": "Analisis Data", "English": "Browse Files", "Chinese": "浏览文件"},
    "profile": {"Indonesia": "Profil Pembuat", "English": "Creator Profile", "Chinese": "创建者简介"},
    "title": {"Indonesia": "Analisis Data Survei", "English": "Survey Data Analysis", "Chinese": "调查数据分析"},
    "subtitle": {"Indonesia": "Unggah file Excel Anda untuk memulai analisis", "English": "Upload your Excel file to start analysis", "Chinese": "上传您的 Excel 文件以开始分析"},
    "upload": {"Indonesia": "Unggah File Excel", "English": "Upload Excel File", "Chinese": "上传 Excel 文件"},
    "preview": {"Indonesia": "Pratinjau Data", "English": "Data Preview", "Chinese": "数据预览"},
    "desc": {"Indonesia": "Analisis Deskriptif", "English": "Descriptive Analysis", "Chinese": "描述性分析"},
    "select_columns": {"Indonesia": "Pilih kolom untuk analisis", "English": "Select columns for analysis", "Chinese": "选择要分析的列"},
    "no_numeric": {"Indonesia": "Tidak ada kolom numerik yang ditemukan", "English": "No numeric columns found", "Chinese": "未找到数字列"},
    "bar_chart": {"Indonesia": "Grafik Batang", "English": "Bar Chart", "Chinese": "柱状图"},
    "histogram": {"Indonesia": "Histogram", "English": "Histogram", "Chinese": "直方图"},
    "x_group": {"Indonesia": "Grup X", "English": "X Group", "Chinese": "X组"},
    "y_group": {"Indonesia": "Grup Y", "English": "Y Group", "Chinese": "Y组"},
    "other_group": {"Indonesia": "Lainnya", "English": "Other", "Chinese": "其他"},
    "x_total_created": {"Indonesia": "X_TOTAL dibuat dari {} kolom", "English": "X_TOTAL created from {} columns", "Chinese": "X_TOTAL 已从 {} 列创建"},
    "y_total_created": {"Indonesia": "Y_TOTAL dibuat dari {} kolom", "English": "Y_TOTAL created from {} columns", "Chinese": "Y_TOTAL 已从 {} 列创建"},
    "auto_assoc": {"Indonesia": "Analisis Asosiasi Otomatis", "English": "Automatic Association Analysis", "Chinese": "自动关联分析"},
    "select_var1": {"Indonesia": "Pilih variabel 1", "English": "Select variable 1", "Chinese": "选择变量1"},
    "select_var2": {"Indonesia": "Pilih variabel 2", "English": "Select variable 2", "Chinese": "选择变量2"},
    "data_type": {"Indonesia": "Tipe data", "English": "Data type", "Chinese": "数据类型"},
    "normality_test": {"Indonesia": "Uji Normalitas", "English": "Normality Test", "Chinese": "正态性检验"},
    "data_normal": {"Indonesia": "Data normal", "English": "Data normal", "Chinese": "数据正态"},
    "data_not_normal": {"Indonesia": "Data tidak normal", "English": "Data not normal", "Chinese": "数据非正态"},
    "using_spearman": {"Indonesia": "Data tidak normal → menggunakan Spearman Correlation", "English": "Data not normal → using Spearman Correlation", "Chinese": "数据非正态 → 使用斯皮尔曼相关"},
    "using_pearson": {"Indonesia": "Data normal → menggunakan Pearson Correlation", "English": "Data normal → using Pearson Correlation", "Chinese": "数据正态 → 使用皮尔逊相关"},
    "corr_result": {"Indonesia": "Hasil Korelasi", "English": "Correlation Result", "Chinese": "相关性结果"},
    "conclusion": {"Indonesia": "Kesimpulan", "English": "Conclusion", "Chinese": "结论"},
    "strong_corr": {"Indonesia": "Kuat", "English": "Strong", "Chinese": "强"},
    "moderate_corr": {"Indonesia": "Sedang", "English": "Moderate", "Chinese": "中等"},
    "weak_corr": {"Indonesia": "Lemah", "English": "Weak", "Chinese": "弱"},
    "no_corr": {"Indonesia": "Tidak ada korelasi", "English": "No correlation", "Chinese": "无相关"},
    "significant": {"Indonesia": "Signifikan", "English": "Significant", "Chinese": "显著"},
    "not_significant": {"Indonesia": "Tidak signifikan", "English": "Not significant", "Chinese": "不显著"},
    "both_numeric": {"Indonesia": "Kedua variabel numeric 😊", "English": "Both variables are numeric 😊", "Chinese": "两个变量都是数值型 😊"},
    "not_both_numeric": {"Indonesia": "Variabel tidak keduanya numeric", "English": "Variables are not both numeric", "Chinese": "变量不都是数值型"},
    "run_auto_analysis": {"Indonesia": "Jalankan Analisis Otomatis", "English": "Run Auto Analysis", "Chinese": "运行自动分析"},
    "pos_corr": {"Indonesia": "positif", "English": "positive", "Chinese": "正"},
    "neg_corr": {"Indonesia": "negatif", "English": "negative", "Chinese": "负"},
    "results_show": {"Indonesia": "Hasil menunjukkan korelasi", "English": "Results show", "Chinese": "结果显示"},
    "with_strength": {"Indonesia": "dengan kekuatan", "English": "with", "Chinese": "相关性，强度为"},
    "p_value_is": {"Indonesia": "Nilai p =", "English": "P-value =", "Chinese": "P值 ="},
    "so_relationship": {"Indonesia": "sehingga hubungan", "English": "so the relationship is", "Chinese": "因此关系"},
    "welcome": {"Indonesia": "Selamat Datang", "English": "Welcome", "Chinese": "欢迎"},
    "welcome_text": {"Indonesia": "Sistem analisis data survei yang powerful dan mudah digunakan", "English": "Powerful and easy-to-use survey data analysis system", "Chinese": "强大且易于使用的调查数据分析系统"},
    "get_started": {"Indonesia": "Mulai Analisis", "English": "Get Started", "Chinese": "开始分析"},
    "feature1_title": {"Indonesia": "Analisis Deskriptif", "English": "Descriptive Analysis", "Chinese": "描述性分析"},
    "feature1_desc": {"Indonesia": "Ringkasan statistik lengkap dan visualisasi data survei Anda", "English": "Comprehensive statistical summaries and visualizations", "Chinese": "全面的统计摘要和可视化"},
    "feature2_title": {"Indonesia": "Grafik Visual", "English": "Visual Charts", "Chinese": "可视化图表"},
    "feature2_desc": {"Indonesia": "Grafik batang dan histogram interaktif untuk pemahaman data yang lebih baik", "English": "Interactive charts for better data understanding", "Chinese": "交互式图表，更好地理解数据"},
    "feature3_title": {"Indonesia": "Analisis Korelasi", "English": "Correlation Analysis", "Chinese": "相关性分析"},
    "feature3_desc": {"Indonesia": "Temukan hubungan antar variabel dengan uji korelasi otomatis", "English": "Discover relationships with automatic correlation testing", "Chinese": "通过自动相关性测试发现关系"},
    "creator_name": {"Indonesia": "Nama Pembuat", "English": "Creator Name", "Chinese": "创建者姓名"},
    "Creator_Information": {"Indonesia": "Informasi Kreator", "English": "Creator Information", "Chinese": "创作者信息"},
    "about_app": {"Indonesia": "Tentang Aplikasi", "English": "About Application", "Chinese": "关于应用"},
}

# -------------------------
# VIDEO BACKGROUND STYLING
# -------------------------
if bg_video:
    st.markdown(f"""
    <style>
        /* Video Background */
        #video-background {{
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%;
            min-height: 100%;
            width: auto;
            height: auto;
            z-index: -1;
            object-fit: cover;
            filter: blur(8px);
            -webkit-filter: blur(8px);
        }}
        
        /* Remove white transparent overlay */
        .stApp {{
            background: transparent !important;
        }}
        
        [data-testid="stAppViewContainer"] {{
            background: transparent !important;
        }}
        
        /* Add slight dark overlay for better text readability */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.3);
            z-index: -1;
        }}
    </style>
    
    <video autoplay muted loop playsinline id="video-background">
        <source src="data:video/mp4;base64,{bg_video}" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
    </style>
    """, unsafe_allow_html=True)

# -------------------------
# MODERN STYLING WITH BLUR EFFECT
# -------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Video Background Fix */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: -1;
    }
            
     /* Header Styling with Glass Effect */
    header[data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Toolbar with Glass Effect */
    .stToolbar {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
    }
    
    /* Deploy button styling */
    .stDeployButton {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    
    .stDeployButton:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Sidebar with Glassmorphism Effect */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        font-size: 1.1rem;
        font-weight: 600;
        color: white !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        color: white !important;
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateX(5px);
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: white !important;
        border-color: transparent;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar Text Styling */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: white !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
    }
    
    /* Main Content Area */
    .main .block-container {
        padding-top: 2rem;
    }
    
    /* Content Cards with Glass Effect */
    .content-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 1.5rem 0;
        color: white;
    }
    
    .content-card h1,
    .content-card h2,
    .content-card h3,
    .content-card h4,
    .content-card p,
    .content-card li {
        color: white;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        margin: 2rem auto;
        max-width: 900px;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        line-height: 1.2;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.7);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
        margin-bottom: 2rem;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
    }
    
    /* Feature Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        height: 100%;
        text-align: center;
        color: white;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        color: white;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }
    
    .feature-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
    }
    
    .feature-desc {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    /* Buttons with Glass Effect */
    .stButton > button {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 1rem 2.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* Language Buttons */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Profile Card */
    .profile-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 20px;
        padding: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        text-align: center;
        max-width: 600px;
        margin: 2rem auto;
        color: white;
    }
    
    /* PROFILE AVATAR FIX */
    .profile-avatar {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        margin: 0 auto 1.5rem;
        border: 3px solid rgba(255, 255, 255, 0.3);
        overflow: hidden;
        position: relative;
    }
    
    .profile-avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }
    
    /* Fallback jika gambar tidak ditemukan */
    .profile-avatar:not(:has(img[src])) {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 4rem;
        color: white;
    }
    
    .profile-name {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 5px rgba(0, 0, 0, 0.8);
    }
    
    .profile-role {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 1.5rem;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
    }
    
    .profile-info {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: left;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Association Analysis Boxes */
    .assoc-box {
        background: rgba(40, 40, 40, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid rgba(102, 126, 234, 0.8);
        color: white;
        font-weight: 500;
        font-size: 1.1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .normality-box {
        background: rgba(255, 243, 205, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #333;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .result-box {
        background: rgba(209, 236, 241, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #333;
    }
    
    .conclusion-box {
        background: rgba(212, 237, 218, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #333;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: white;
        font-weight: 700;
        text-shadow: 0 2px 5px rgba(0, 0, 0, 0.8);
    }
    
    /* Text elements */
    p, li, span, div:not([class*="st-"]) {
        color: white;
    }
    
    /* File Uploader */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 10px;
        border: 1px dashed rgba(255, 255, 255, 0.3);
    }
            
    /* Tombol Browse Files */
    .stFileUploader button {
        background: #000000 !important;
        color: white !important;
        border: 2px solid #000000 !important;
        padding: 0.75rem 2rem !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3) !important;
        margin-top: 1rem !important;
        margin: 1rem auto !important;  /* LINE BARU - untuk posisi tengah */
        display: block !important; 
    }
    
    .stFileUploader button:hover {
        background: #333333 !important;
        border-color: #333333 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Teks di dalam file uploader */
    .stFileUploader > div > div > div > div {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
    }
    
    .stFileUploader > div > div > small {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.9rem !important;
    }
    
    /* Dataframe */
    .dataframe {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        color: white !important;
    }
    
    .dataframe th {
        background: rgba(0, 0, 0, 0.3) !important;
        color: white !important;
    }
    
    .dataframe td {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
    }
    
    /* Selectboxes and Multiselect */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover {
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
    }
            
     /* ================================================ */
    /* COMPLETE DROPDOWN FIX - GUARANTEED VISIBLE TEXT */
    /* ================================================ */

    /* 1. MAIN SELECTBOX CONTAINER */
    .stSelectbox > div {
        background: transparent !important;
        border-radius: 8px !important;
    }

    /* 2. SELECT INPUT FIELD (box yang diklik) */
    .stSelectbox [data-baseweb="select"] > div {
        background: rgba(20, 20, 20, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
        min-height: 42px !important;
        display: flex !important;
        align-items: center !important;
    }

    /* 3. SELECTED VALUE TEXT (text di dalam box) */
    .stSelectbox [data-baseweb="select"] > div > div {
        color: black !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8) !important;
    }

    /* 4. PLACEHOLDER TEXT (saat belum pilih) */
    .stSelectbox [data-baseweb="select"] > div > div:empty::before {
        content: attr(placeholder) !important;
        color: rgba(255, 255, 255, 0.7) !important;
        font-style: italic !important;
    }

    /* 5. HOVER EFFECT */
    .stSelectbox [data-baseweb="select"] > div:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
    }

    /* 6. DROPDOWN POPUP CONTAINER */
    [data-baseweb="popover"] {
        background: rgba(30, 30, 30, 0.98) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 10px !important;
        margin-top: 8px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        z-index: 10000 !important;
        overflow: hidden !important;
    }

    /* 7. DROPDOWN LIST */
    [data-baseweb="menu"] {
        background: rgba(30, 30, 30, 0.98) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-radius: 10px !important;
        padding: 8px 0 !important;
        max-height: 350px !important;
        overflow-y: auto !important;
    }

    /* 8. EACH OPTION ITEM */
    [data-baseweb="menu"] li,
    [role="option"] {
        background: transparent !important;
        padding: 12px 16px !important;
        margin: 0 !important;
        font-size: 14px !important;
        min-height: 44px !important;
        display: flex !important;
        align-items: center !important;
        color: white !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8) !important;
    }

    /* 9. HOVER EFFECT FOR OPTIONS */
    [data-baseweb="menu"] li:hover,
    [role="option"]:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.4) 0%, rgba(118, 75, 162, 0.4) 100%) !important;
        color: white !important;
    }

    /* 10. SELECTED OPTION */
    [data-baseweb="menu"] [aria-selected="true"],
    [role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.7) 0%, rgba(118, 75, 162, 0.7) 100%) !important;
        color: white !important;
        font-weight: 600 !important;
    }

    /* 11. TEXT INSIDE OPTIONS */
    [data-baseweb="menu"] li span,
    [role="option"] span,
    [data-baseweb="menu"] li div,
    [role="option"] div {
        color: white !important;
        font-size: 14px !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8) !important;
    }

    /* 12. ARROW/DROPDOWN ICON */
    [data-baseweb="select"] svg {
        fill: white !important;
        opacity: 0.8 !important;
    }

    /* 13. SCROLLBAR STYLING */
    [data-baseweb="menu"]::-webkit-scrollbar {
        width: 8px;
    }

    [data-baseweb="menu"]::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }

    [data-baseweb="menu"]::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 4px;
    }

    [data-baseweb="menu"]::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.5);
    }

    /* 14. FIX FOR SPECIFIC DROPDOWNS */
    div[data-testid="stSelectbox"][data-key*="var"] [data-baseweb="select"] > div > div {
        color: white !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }

    /* 15. FORCE WHITE TEXT ON ALL SELECTBOXES */
    .stSelectbox * {
        color: white !important;
    }

    /* 16. IMPORTANT: OVERRIDE ANY INVISIBLE TEXT */
    .stSelectbox,
    .stSelectbox *,
    [data-baseweb="select"],
    [data-baseweb="select"] *,
    [data-baseweb="menu"],
    [data-baseweb="menu"] * {
        color: white !important;
    }
        
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------
with st.sidebar:
    st.markdown("Navigation")
    page = st.radio(
        "",
        [texts["home"][st.session_state.language], 
         texts["browse"][st.session_state.language], 
         texts["profile"][st.session_state.language]],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("## 🌍 Language")
    
    if st.button("🇮🇩 Indonesia", use_container_width=True, key="lang_id"):
        st.session_state.language = "Indonesia"
        st.rerun()
    
    if st.button("🇬🇧 English", use_container_width=True, key="lang_en"):
        st.session_state.language = "English"
        st.rerun()
    
    if st.button("🇨🇳 中文", use_container_width=True, key="lang_cn"):
        st.session_state.language = "Chinese"
        st.rerun()

language = st.session_state.language

# -------------------------
# HELPER FUNCTIONS
# -------------------------
def check_normality(data, alpha=0.05):
    try:
        data_clean = data.dropna()
        if len(data_clean) < 3:
            return None, None
        stat, p_value = shapiro(data_clean)
        return stat, p_value
    except:
        try:
            stat, p_value = normaltest(data_clean)
            return stat, p_value
        except:
            return None, None

def get_correlation_strength(rho):
    abs_rho = abs(rho)
    if abs_rho >= 0.7:
        return texts["strong_corr"][language]
    elif abs_rho >= 0.5:
        return texts["moderate_corr"][language]
    elif abs_rho >= 0.3:
        return texts["weak_corr"][language]
    else:
        return texts["no_corr"][language]

def format_p_value(p):
    if p < 0.0001:
        return "0.0000"
    else:
        return f"{p:.4f}"

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def plot_barh(ax, series, max_bars=20):
    try:
        counts = series.value_counts(dropna=False)
        if len(counts) == 0:
            ax.text(0.5, 0.5, "No data", ha='center', va='center', fontsize=10, color='red')
            return
        if len(counts) > max_bars:
            counts = counts.nlargest(max_bars)
        counts.sort_index().plot(kind='barh', ax=ax, color='#667eea')
    except Exception as e:
        ax.text(0.5, 0.5, f"Error: {str(e)[:30]}", ha='center', va='center', fontsize=9, color='red')

def render_group_charts(df, cols, group_name):
    if not cols:
        return
    
    st.markdown(f'<div class="content-card"><h3>📊 {texts["bar_chart"][language]} ({group_name})</h3></div>', unsafe_allow_html=True)
    max_per_row = 3
    
    for row in chunk_list(cols, max_per_row):
        cols_ui = st.columns(len(row))
        for i, col_name in enumerate(row):
            with cols_ui[i]:
                fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
                try:
                    plot_barh(ax, df[col_name])
                    ax.set_title(col_name, fontsize=10, fontweight='bold')
                    ax.tick_params(axis='both', labelsize=8)
                except:
                    ax.text(0.5, 0.5, "Chart error", ha='center', va='center', fontsize=10, color='red')
                plt.tight_layout()
                st.pyplot(fig, clear_figure=True)
                plt.close(fig)

    st.markdown(f'<div class="content-card"><h3>📈 {texts["histogram"][language]} ({group_name})</h3></div>', unsafe_allow_html=True)
    for row in chunk_list(cols, max_per_row):
        cols_ui = st.columns(len(row))
        for i, col_name in enumerate(row):
            with cols_ui[i]:
                fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
                try:
                    coldata = pd.to_numeric(df[col_name], errors='coerce').dropna()
                    if len(coldata) == 0:
                        raise ValueError("no numeric data")
                    num_bins = min(20, max(5, int(np.sqrt(len(coldata)))))
                    ax.hist(coldata, bins=num_bins, edgecolor='black', alpha=0.7, color='#764ba2')
                    ax.set_title(col_name, fontsize=10, fontweight='bold')
                    ax.tick_params(axis='both', labelsize=8)
                except:
                    ax.text(0.5, 0.5, "No numeric data", ha='center', va='center', fontsize=10, color='red')
                plt.tight_layout()
                st.pyplot(fig, clear_figure=True)
                plt.close(fig)

# -------------------------
# PAGE: HOME
# -------------------------
if page == texts["home"][language]:
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">{texts["welcome"][language]}</h1>
        <p class="hero-subtitle">{texts["welcome_text"][language]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">{texts["feature1_title"][language]}</div>
            <div class="feature-desc">{texts["feature1_desc"][language]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">{texts["feature2_title"][language]}</div>
            <div class="feature-desc">{texts["feature2_desc"][language]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">🔗</div>
            <div class="feature-title">{texts["feature3_title"][language]}</div>
            <div class="feature-desc">{texts["feature3_desc"][language]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)

# -------------------------
# PAGE: BROWSE FILES
# -------------------------
elif page == texts["browse"][language]:
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">{texts["title"][language]}</h1>
        <p class="hero-subtitle">{texts["subtitle"][language]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        texts["upload"][language],
        type=["xlsx", "xls"]
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            
            if df.empty:
                st.error("Excel file is empty")
                st.stop()
                
        except Exception as e:
            st.error(f"Failed to read file: {str(e)}")
            st.stop()

        st.markdown(f'<div class="content-card"><h2>📁 {texts["preview"][language]}</h2></div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        df = df.copy()
        maybe_numeric = []
        for col in df.columns:
            try:
                coerced = pd.to_numeric(df[col], errors='coerce')
                non_na_ratio = coerced.notna().sum() / max(len(coerced), 1)
                if non_na_ratio >= 0.5:
                    df[col] = coerced
                    maybe_numeric.append(col)
            except:
                continue

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        st.markdown(f'<div class="content-card"><h2>📈 {texts["desc"][language]}</h2></div>', unsafe_allow_html=True)

        if len(numeric_cols) == 0:
            st.warning(texts["no_numeric"][language])
        else:
            selected_desc_cols = st.multiselect(
                texts["select_columns"][language],
                numeric_cols,
                default=numeric_cols[:10] if len(numeric_cols) > 10 else numeric_cols
            )

            if selected_desc_cols:
                st.write(df[selected_desc_cols].describe())

                def starts_with_letter(c, letter):
                    try:
                        return bool(re.match(rf"^\s*{letter}", str(c), flags=re.I))
                    except:
                        return False

                x_cols = [c for c in selected_desc_cols if starts_with_letter(c, 'x')]
                y_cols = [c for c in selected_desc_cols if starts_with_letter(c, 'y')]
                other_cols = [c for c in selected_desc_cols if c not in x_cols + y_cols]

                x_total = None
                y_total = None
                
                if x_cols:
                    try:
                        x_total = df[x_cols].sum(axis=1)
                        df['X_TOTAL'] = x_total
                        st.success("✅ " + texts["x_total_created"][language].format(len(x_cols)))
                    except Exception as e:
                        st.warning(f"Could not create X_TOTAL: {str(e)}")
                
                if y_cols:
                    try:
                        y_total = df[y_cols].sum(axis=1)
                        df['Y_TOTAL'] = y_total
                        st.success("✅ " + texts["y_total_created"][language].format(len(y_cols)))
                    except Exception as e:
                        st.warning(f"Could not create Y_TOTAL: {str(e)}")
                
                if x_cols:
                    render_group_charts(df, x_cols, texts["x_group"][language])
                if y_cols:
                    render_group_charts(df, y_cols, texts["y_group"][language])
                if other_cols:
                    render_group_charts(df, other_cols, texts["other_group"][language])

        # Association Analysis
        st.markdown(f'<div class="content-card"><h2>🤖 {texts["auto_assoc"][language]}</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {texts['select_var1'][language]}")
            var1_options = ["-- Pilih --"] + numeric_cols
            var1 = st.selectbox("", var1_options, key="var1_select")
        
        with col2:
            st.markdown(f"### {texts['select_var2'][language]}")
            if var1 != "-- Pilih --":
                var2_options = ["-- Pilih --"] + [col for col in numeric_cols if col != var1]
            else:
                var2_options = ["-- Pilih --"] + numeric_cols
            var2 = st.selectbox("", var2_options, key="var2_select")
        
        if var1 != "-- Pilih --" and var2 != "-- Pilih --":
            st.markdown("---")
            st.markdown(f"### {texts['data_type'][language]}")
            
            is_var1_numeric = pd.api.types.is_numeric_dtype(df[var1])
            is_var2_numeric = pd.api.types.is_numeric_dtype(df[var2])
            
            st.markdown(f"**{var1}:** {'Numeric' if is_var1_numeric else 'Non-numeric'}")
            st.markdown(f"**{var2}:** {'Numeric' if is_var2_numeric else 'Non-numeric'}")
            
            if is_var1_numeric and is_var2_numeric:
                st.markdown(f'<div class="assoc-box">✓ {texts["both_numeric"][language]}</div>', unsafe_allow_html=True)
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    if st.button(f"🚀 {texts['run_auto_analysis'][language]}", type="primary", use_container_width=True):
                        st.markdown("---")
                        st.markdown(f"### {texts['normality_test'][language]}")
                        
                        data1 = pd.to_numeric(df[var1], errors='coerce').dropna()
                        data2 = pd.to_numeric(df[var2], errors='coerce').dropna()
                        
                        _, p1 = check_normality(data1)
                        _, p2 = check_normality(data2)
                        
                        if p1 is not None:
                            is_normal1 = p1 > 0.05
                            st.markdown(f"**{var1}:** p = {p1:.4f} - {'✓' if is_normal1 else '✗'} {texts['data_normal'][language] if is_normal1 else texts['data_not_normal'][language]}")
                        
                        if p2 is not None:
                            is_normal2 = p2 > 0.05
                            st.markdown(f"**{var2}:** p = {p2:.4f} - {'✓' if is_normal2 else '✗'} {texts['data_normal'][language] if is_normal2 else texts['data_not_normal'][language]}")
                        
                        use_spearman = (p1 is not None and p1 <= 0.05) or (p2 is not None and p2 <= 0.05)
                        
                        st.markdown("---")
                        
                        if use_spearman:
                            st.markdown(f'<div class="normality-box">{texts["using_spearman"][language]}</div>', unsafe_allow_html=True)
                            method = "spearman"
                        else:
                            st.markdown(f'<div class="normality-box">{texts["using_pearson"][language]}</div>', unsafe_allow_html=True)
                            method = "pearson"
                        
                        try:
                            temp_df = df[[var1, var2]].copy()
                            temp_df[var1] = pd.to_numeric(temp_df[var1], errors='coerce')
                            temp_df[var2] = pd.to_numeric(temp_df[var2], errors='coerce')
                            temp_df = temp_df.dropna()
                            
                            if len(temp_df) >= 2:
                                x_data = temp_df[var1].values
                                y_data = temp_df[var2].values
                                
                                if method == "pearson":
                                    corr_coef, p_value = pearsonr(x_data, y_data)
                                else:
                                    corr_coef, p_value = spearmanr(x_data, y_data)
                                
                                st.markdown(f"""
                                <div class="result-box">
                                    <h3>{texts['corr_result'][language]}</h3>
                                    <h4>{method.upper()}</h4>
                                    <p style="font-size: 1.2rem; font-weight: bold;">rho = {corr_coef:.4f}</p>
                                    <p style="font-size: 1.2rem; font-weight: bold;">P-value = {format_p_value(p_value)}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                strength = get_correlation_strength(corr_coef)
                                direction = texts["pos_corr"][language] if corr_coef > 0 else texts["neg_corr"][language]
                                
                                st.markdown(f"""
                                <div class="conclusion-box">
                                    <h3>{texts['conclusion'][language]}</h3>
                                    <p>{texts["results_show"][language]} {direction} {texts["with_strength"][language]} {strength}</p>
                                    <p>{texts["p_value_is"][language]} {format_p_value(p_value)} - {texts["significant"][language] if p_value < 0.05 else texts["not_significant"][language]}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
                                ax.scatter(x_data, y_data, alpha=0.7, color='#667eea', s=60, edgecolors='white', linewidth=0.5)
                                
                                if method == "pearson":
                                    z = np.polyfit(x_data, y_data, 1)
                                    p = np.poly1d(z)
                                    ax.plot(x_data, p(x_data), color='#764ba2', linewidth=2, linestyle='--', alpha=0.8)
                                
                                ax.set_xlabel(var1, fontsize=12, fontweight='bold')
                                ax.set_ylabel(var2, fontsize=12, fontweight='bold')
                                ax.set_title(f"Scatter Plot: {var1} vs {var2}\n({method.upper()} r = {corr_coef:.4f}, p = {format_p_value(p_value)})", fontsize=14, fontweight='bold')
                                ax.grid(True, alpha=0.3, linestyle='--')
                                
                                plt.tight_layout()
                                st.pyplot(fig)
                                plt.close(fig)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                st.markdown(f'<div class="assoc-box">⚠ {texts["not_both_numeric"][language]}</div>', unsafe_allow_html=True)

# -------------------------
# PAGE: CREATOR PROFILE (SIMPLE & FIXED VERSION)
# -------------------------
elif page == texts["profile"][language]:
    # HERO SECTION
    st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">{texts["profile"][language]}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Convert image to base64
    img_base64 = None
    image_paths = ["author.jpg", "Author.jpg", "AUTHOR.jpg", "./author.jpg"]
    
    for img_path in image_paths:
        img_base64 = get_base64_image(img_path)
        if img_base64:
            break
    
    if img_base64:
        # PROFILE CARD dengan base64 image
        st.markdown(f"""
        <div class="profile-card">
            <div class="profile-avatar">
                <img src="data:image/jpeg;base64,{img_base64}" alt="Profile Photo">
            </div>
            <div class="profile-name">Fayruz Novarendi</div>
            <div class="profile-role">Data Analyst & Programmer</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback jika gambar tidak ditemukan
        st.markdown("""
        <div class="profile-card">
            <div class="profile-avatar" style="display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 4rem;">👤</span>
            </div>
            <div class="profile-name">Fayruz Novarendi</div>
            <div class="profile-role">Data Analyst & Programmer</div>
        </div>
        """, unsafe_allow_html=True)
        st.warning("⚠️ Gambar 'author.jpg' tidak ditemukan di folder yang sama")
    
    # CONTACT INFO
    Creator_Information = {"Indonesia": "Informasi Kreator", "English": "Creator Information", "Chinese": "创作者信息"}[language]
    
    st.markdown(f'<div class="content-card"><h3>{Creator_Information}</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 10px;">
            <p><strong>Student ID:</strong><br>004202400053</p>
            <p><strong>Class:</strong><br>Industrial Engineering Class 1</p>
            <p><strong>Group:</strong><br>Group 8</p>        
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 10px;">
            <p><strong>Course:</strong><br>Statistic 1</p>
            <p><strong>Contribution:</strong><br>Processing data and creating this website</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ABOUT APP SECTION - Menggunakan teks langsung tanpa dictionary kompleks
    st.markdown(f'<div class="content-card"><h3>{texts["about_app"][language]}</h3>', unsafe_allow_html=True)
    
    if language == "Indonesia":
        about_content = """
        <p>Aplikasi ini dirancang untuk membantu Anda menganalisis data survei dengan mudah dan cepat.</p>
        
        <p><strong>Fitur:</strong></p>
        <ul>
            <li>Analisis statistik deskriptif</li>
            <li>Visualisasi data interaktif</li>
            <li>Uji korelasi Pearson & Spearman</li>
            <li>Support multi-bahasa</li>
            <li>Interface user-friendly</li>
        </ul>
        """
    elif language == "English":
        about_content = """
        <p>This application is designed to help you analyze survey data easily and quickly.</p>
        
        <p><strong>Features:</strong></p>
        <ul>
            <li>Descriptive statistical analysis</li>
            <li>Interactive data visualization</li>
            <li>Pearson & Spearman correlation tests</li>
            <li>Multi-language support</li>
            <li>User-friendly interface</li>
        </ul>
        """
    else:  # Chinese
        about_content = """
        <p>此应用程序旨在帮助您轻松快速地分析调查数据。</p>
        
        <p><strong>功能:</strong></p>
        <ul>
            <li>描述性统计分析</li>
            <li>交互式数据可视化</li>
            <li>Pearson & Spearman 相关性测试</li>
            <li>多语言支持</li>
            <li>用户友好界面</li>
        </ul>
        """
    
    st.markdown(about_content, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # TECH STACK
    tech_title = {"Indonesia": "Teknologi yang Digunakan", "English": "Technology Stack", "Chinese": "使用的技术"}[language]
    
    st.markdown(f'<div class="content-card"><h3>{tech_title}</h3>', unsafe_allow_html=True)
    
    tech_cols = st.columns(4)
    with tech_cols[0]:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2rem;">🐍</div>
            <div>Python</div>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_cols[1]:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2rem;">📊</div>
            <div>Streamlit</div>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_cols[2]:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2rem;">📈</div>
            <div>Pandas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_cols[3]:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2rem;">🔬</div>
            <div>SciPy</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)