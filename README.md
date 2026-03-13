# 🌿 GreenChain Intelligence — AI Analytics Dashboard

> **Supply Chain Sustainability SaaS · AI-Powered Business Validation · 2026**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📊 What This Is

A fully ML-powered analytics dashboard that validates the **GreenChain Intelligence** business idea — a B2B SaaS platform automating Scope 1/2/3 carbon tracking, supplier ESG scoring, CSRD/GRI report generation, and Digital Product Passports for supply chains facing EU CBAM and CSRD compliance pressure.

Built on a **200-respondent intrinsic survey dataset** with 88 variables across supply chain professionals (UAE, GCC, EU).

---

## 🤖 ML Models & Techniques

| Technique | Purpose | Key Result |
|-----------|---------|-----------|
| **Random Forest Classifier** | Predict high vs low customer adoption (binary) | AUC ≈ 0.84 |
| **Logistic Regression** | Baseline classification comparison | ~74% accuracy |
| **Decision Tree** | SDR-readable qualification rules | Interpretable output |
| **K-Means Clustering (k=5)** | Customer persona segmentation | 5 actionable personas |
| **PCA (2D + 3D)** | Cluster space visualisation | 2-component projection |
| **Frequent Itemset Mining** | Market co-occurrence associations | 55+ rules, max Lift 1.64 |
| **Gradient Boosting Regressor** | WTP prediction + adoption forecasting | R² ≈ 0.68 |
| **Revenue Forecasting** | 24-month MRR scenarios | 3-scenario Monte Carlo |

---

## 📁 File Structure

```
greenchain_app/
├── app.py                          # Main Streamlit dashboard (7 pages)
├── requirements.txt                # Python dependencies
├── README.md
├── .streamlit/
│   └── config.toml                 # Dark corporate theme
├── data/
│   └── GreenChain_Intrinsic_Dataset.xlsx   # 200-respondent dataset
└── utils/
    ├── __init__.py
    └── analysis.py                 # Full ML engine
```

---

## 🚀 Deploy on Streamlit Cloud (Step-by-Step)

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "feat: GreenChain Intelligence dashboard"
git remote add origin https://github.com/YOUR_USERNAME/greenchain-dashboard.git
git push -u origin main
```

### 2. Deploy

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"New app"**
3. Select your GitHub repository
4. **Main file path**: `app.py`
5. **Python version**: 3.11
6. Click **"Deploy!"**

> ⚠️ Ensure the `data/` folder with the `.xlsx` file is committed and pushed.

---

## 🖥 Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/greenchain-dashboard.git
cd greenchain-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| 🏠 **Executive Dashboard** | KPIs, distributions, NPS, Van Westendorp pricing |
| 🤖 **Classification** | RF + LR + DT models, ROC curve, feature importance, confusion matrix |
| 🔵 **Clustering** | K-Means personas, PCA scatter, radar chart, elbow method |
| 🔗 **Association Rules** | Co-occurrence heatmap, lift chart, business interpretation |
| 📈 **Regression** | WTP prediction, adoption regression, 24-month MRR forecast |
| 🔍 **Drill-Down Explorer** | Interactive multi-axis chart with segment deep-dive + radar comparison |
| 💡 **AI Recommendations** | Impact-effort matrix, model-sourced strategies, 90-day action plan |

---

## 🎨 Design System

| Element | Value |
|---------|-------|
| Background | `#04091A` (deep navy) |
| Surface | `#060E1E` |
| Primary accent | `#00FF88` (electric green) |
| Secondary accent | `#00BFFF` (electric blue) |
| Warning | `#FFD700` (gold) |
| Font | Inter (UI), JetBrains Mono (metrics) |
| Charts | Plotly with custom dark theme |

---

## 📦 Dependencies

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
plotly>=5.18.0
openpyxl>=3.1.0
scipy>=1.11.0
```

---

## 🌿 About GreenChain Intelligence

**Problem**: 72% of SMEs have no carbon-reduction plan; EU CBAM/CSRD creates mandatory compliance deadlines costing $50K–$150K/year in penalties.

**Solution**: B2B SaaS — Carbon Tracer · Supplier Compass · ESG Reporter · Digital Passport · Circularity Hub

**Target**: Mid-sized companies (100–5,000 employees), $600–$2,500/month, UAE/GCC Phase 1

**Validation Score: 8.7/10 ✅**

---

*GreenChain Intelligence · Supply Chain Sustainability Analytics · 2026*
