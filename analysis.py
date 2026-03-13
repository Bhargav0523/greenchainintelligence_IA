"""
GreenChain Intelligence — ML Analysis Engine
Classification | Clustering | Association Rules | Regression
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score, roc_auc_score, confusion_matrix,
    roc_curve, r2_score, mean_squared_error
)
import warnings
warnings.filterwarnings("ignore")

# ── Feature columns (36 encoded/numeric, no derived leakage) ─────────────────
FEATURES = [
    'A4: Company Size (Encoded)',
    'A6: EU Export (Encoded)',
    'A7: Supplier Count (Encoded)',
    'B1: Sustainability Maturity (1-5)',
    'B2: Carbon Measurement (Encoded)',
    'B4: ESG Report (Encoded)',
    'B6: Data Accuracy Confidence (1-5)',
    'C1: CBAM Awareness (1-5)',
    'C2: Buyer ESG Requests (Encoded)',
    'C3: Penalty Experience (Encoded)',
    'C4: Regulatory Investment Influence (1-5)',
    'C6: Solution Urgency (Encoded)',
    'D1: Scope3 Tracking Challenge (1-5)',
    'D2: Manual ESG Hours (Encoded)',
    'D3: ESG Cost (Encoded)',
    'D4: Supplier Data Difficulty (1-5)',
    'D5: Greenwashing Risk Concern (1-5)',
    'D6: Digital Passport (Encoded)',
    'D7: Unified Platform Gap Severity (1-5)',
    'E1: Carbon Dashboard Value (1-5)',
    'E2: Supplier Scoring Value (1-5)',
    'E3: ESG Report Gen Value (1-5)',
    'E4: Digital Passport Value (1-5)',
    'E5: Route Optimizer Value (1-5)',
    'E7: POC Trial Likelihood (1-5)',
    'E8: NPS Score (0-10)',
    'F1: Budget (Encoded)',
    'F7: Money-Back Guarantee Influence (1-5)',
    'G1: Tool Status (Encoded)',
    'G3: Current Solution Satisfaction (1-5)',
    'G5: Local Compliance Importance (1-5)',
    'G6: Startup Openness (Encoded)',
    'H1: Procurement Cycle (Encoded)',
    'H2: Stakeholders (Encoded)',
    'H4: POC Willingness (Encoded)',
    'H6: Referral Likelihood (1-5)',
]

FEATURE_LABELS = {
    'A4: Company Size (Encoded)':                  'Company Size',
    'A6: EU Export (Encoded)':                     'EU Export Status',
    'A7: Supplier Count (Encoded)':                'Supplier Count',
    'B1: Sustainability Maturity (1-5)':           'ESG Maturity',
    'B2: Carbon Measurement (Encoded)':            'Carbon Measurement',
    'B4: ESG Report (Encoded)':                    'ESG Report Status',
    'B6: Data Accuracy Confidence (1-5)':          'Data Confidence',
    'C1: CBAM Awareness (1-5)':                    'CBAM Awareness',
    'C2: Buyer ESG Requests (Encoded)':            'Buyer ESG Requests',
    'C3: Penalty Experience (Encoded)':            'Penalty Experience',
    'C4: Regulatory Investment Influence (1-5)':   'Reg. Investment Influence',
    'C6: Solution Urgency (Encoded)':              'Solution Urgency',
    'D1: Scope3 Tracking Challenge (1-5)':         'Scope3 Challenge',
    'D2: Manual ESG Hours (Encoded)':              'Manual ESG Hours',
    'D3: ESG Cost (Encoded)':                      'ESG Reporting Cost',
    'D4: Supplier Data Difficulty (1-5)':          'Supplier Data Difficulty',
    'D5: Greenwashing Risk Concern (1-5)':         'Greenwashing Concern',
    'D6: Digital Passport (Encoded)':              'Digital Passport Status',
    'D7: Unified Platform Gap Severity (1-5)':     'Platform Gap Severity',
    'E1: Carbon Dashboard Value (1-5)':            'Carbon Dashboard Value',
    'E2: Supplier Scoring Value (1-5)':            'Supplier Scoring Value',
    'E3: ESG Report Gen Value (1-5)':              'ESG Report Gen Value',
    'E4: Digital Passport Value (1-5)':            'Digital Passport Value',
    'E5: Route Optimizer Value (1-5)':             'Route Optimizer Value',
    'E7: POC Trial Likelihood (1-5)':              'POC Trial Likelihood',
    'E8: NPS Score (0-10)':                        'NPS Score',
    'F1: Budget (Encoded)':                        'ESG Budget',
    'F7: Money-Back Guarantee Influence (1-5)':    'Money-Back Influence',
    'G1: Tool Status (Encoded)':                   'Current ESG Tool',
    'G3: Current Solution Satisfaction (1-5)':     'Current Satisfaction',
    'G5: Local Compliance Importance (1-5)':       'Local Compliance Importance',
    'G6: Startup Openness (Encoded)':              'Startup Openness',
    'H1: Procurement Cycle (Encoded)':             'Procurement Cycle',
    'H2: Stakeholders (Encoded)':                  'Approval Stakeholders',
    'H4: POC Willingness (Encoded)':               'POC Willingness',
    'H6: Referral Likelihood (1-5)':               'Referral Likelihood',
}


def load_data(path="data/GreenChain_Intrinsic_Dataset.xlsx"):
    df = pd.read_excel(path, sheet_name="Raw Dataset", header=2)
    df.columns = df.columns.str.strip()
    return df


def compute_kpis(df):
    n = len(df)
    promoters  = (df["DERIVED: NPS Category"] == "Promoter").sum()
    detractors = (df["DERIVED: NPS Category"] == "Detractor").sum()
    return {
        "n":                  n,
        "high_urgency_pct":   round(float((df["DERIVED: Urgency Composite (0-13)"] >= 10).mean()) * 100, 1),
        "nps_score":          round(float((promoters - detractors) / n * 100), 1),
        "avg_wtp":            int(df["DERIVED: WTP Midpoint (USD)"].mean()),
        "poc_ready_pct":      round(float((df["H4: POC Willingness (Encoded)"] >= 2).mean()) * 100, 1),
        "avg_feature_val":    round(float(df["DERIVED: Feature Value Avg (1-5)"].mean()), 2),
        "open_startup_pct":   round(float((df["G6: Startup Openness (Encoded)"] >= 2).mean()) * 100, 1),
        "high_pain_pct":      round(float((df["DERIVED: Pain Severity Avg (1-5)"] >= 4.0).mean()) * 100, 1),
        "promoter_pct":       round(float(promoters / n * 100), 1),
        "avg_urgency":        round(float(df["DERIVED: Urgency Composite (0-13)"].mean()), 1),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 1. CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_classification(df):
    """
    Binary target: High Adoption (score >= 7) vs Low Adoption
    Models: Random Forest, Logistic Regression, Decision Tree
    """
    X = df[FEATURES].values.astype(float)
    y = (df["DERIVED: Adoption Score (0-11)"] >= 7).astype(int).values

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    sc = StandardScaler()
    X_tr_s = sc.fit_transform(X_tr)
    X_te_s  = sc.transform(X_te)

    # Random Forest
    rf = RandomForestClassifier(n_estimators=300, max_depth=8,
                                 min_samples_leaf=3, random_state=42)
    rf.fit(X_tr_s, y_tr)
    rf_pred  = rf.predict(X_te_s)
    rf_proba = rf.predict_proba(X_te_s)[:, 1]

    # Logistic Regression
    lr = LogisticRegression(max_iter=1000, C=1.0, random_state=42)
    lr.fit(X_tr_s, y_tr)
    lr_pred  = lr.predict(X_te_s)
    lr_proba = lr.predict_proba(X_te_s)[:, 1]

    # Decision Tree
    dt = DecisionTreeClassifier(max_depth=6, min_samples_leaf=5, random_state=42)
    dt.fit(X_tr_s, y_tr)
    dt_pred = dt.predict(X_te_s)

    # Cross-validation on RF
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(rf, X_tr_s, y_tr, cv=cv, scoring="accuracy")

    # Feature importance
    fi = pd.DataFrame({
        "feature": FEATURES,
        "label":   [FEATURE_LABELS[f] for f in FEATURES],
        "importance": rf.feature_importances_,
    }).sort_values("importance", ascending=False).head(15)

    # ROC
    fpr, tpr, thresholds = roc_curve(y_te, rf_proba)

    # Full-dataset predictions (for scatter/segment views)
    X_all_s = sc.transform(X)
    all_pred  = rf.predict(X_all_s)
    all_proba = rf.predict_proba(X_all_s)[:, 1]

    return {
        "rf_acc":   round(float(accuracy_score(y_te, rf_pred)), 4),
        "lr_acc":   round(float(accuracy_score(y_te, lr_pred)), 4),
        "dt_acc":   round(float(accuracy_score(y_te, dt_pred)), 4),
        "roc_auc":  round(float(roc_auc_score(y_te, rf_proba)), 4),
        "cv_mean":  round(float(cv_scores.mean()), 4),
        "cv_std":   round(float(cv_scores.std()), 4),
        "cm":       confusion_matrix(y_te, rf_pred).tolist(),
        "fpr":      fpr.tolist(),
        "tpr":      tpr.tolist(),
        "feature_imp": fi,
        "y_te":     y_te.tolist(),
        "y_pred":   rf_pred.tolist(),
        "y_proba":  rf_proba.tolist(),
        "all_pred": all_pred.tolist(),
        "all_proba":all_proba.tolist(),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 2. CLUSTERING
# ═══════════════════════════════════════════════════════════════════════════════
CLUSTER_FEATURES = [
    'B1: Sustainability Maturity (1-5)',
    'C1: CBAM Awareness (1-5)',
    'C4: Regulatory Investment Influence (1-5)',
    'C6: Solution Urgency (Encoded)',
    'D7: Unified Platform Gap Severity (1-5)',
    'DERIVED: Feature Value Avg (1-5)',
    'DERIVED: Urgency Composite (0-13)',
    'F1: Budget (Encoded)',
    'DERIVED: WTP Midpoint (USD)',
    'G6: Startup Openness (Encoded)',
    'E7: POC Trial Likelihood (1-5)',
    'H4: POC Willingness (Encoded)',
    'DERIVED: Adoption Score (0-11)',
    'E8: NPS Score (0-10)',
]

PERSONA_DEFS = [
    ("🔥 High-Value Immediate",    "#00FF88", "#00FF8830"),
    ("⚡ Urgency-Driven Converter","#00BFFF", "#00BFFF30"),
    ("💎 Strategic Enterprise",    "#FFD700", "#FFD70030"),
    ("🌱 Near-Term Pipeline",      "#7CFC00", "#7CFC0030"),
    ("⏳ Long-Term Nurture",       "#FF6B6B", "#FF6B6B30"),
]

def run_clustering(df, n_clusters=5):
    df_c = df[CLUSTER_FEATURES].copy().dropna()

    sc = MinMaxScaler()
    X_s = sc.fit_transform(df_c.values)

    # Elbow
    inertias = []
    for k in range(2, 10):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_s)
        inertias.append(float(km.inertia_))

    # Final model
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=15)
    labels = km.fit_predict(X_s)

    # Silhouette
    from sklearn.metrics import silhouette_score
    sil = round(float(silhouette_score(X_s, labels)), 4)

    # PCA 2D
    pca2 = PCA(n_components=2, random_state=42)
    coords2 = pca2.fit_transform(X_s)

    # PCA 3D
    pca3 = PCA(n_components=3, random_state=42)
    coords3 = pca3.fit_transform(X_s)

    df_c = df_c.copy()
    df_c["cluster"]  = labels
    df_c["pca_x"]    = coords2[:, 0]
    df_c["pca_y"]    = coords2[:, 1]
    df_c["pca3_x"]   = coords3[:, 0]
    df_c["pca3_y"]   = coords3[:, 1]
    df_c["pca3_z"]   = coords3[:, 2]

    # Cluster profiles (mean per cluster)
    profile = df_c.groupby("cluster")[CLUSTER_FEATURES].mean().round(3)

    # Assign personas by heuristic ordering on urgency + budget + adoption
    score_map = {}
    for ci in range(n_clusters):
        row = profile.loc[ci]
        s = (row.get("DERIVED: Urgency Composite (0-13)", 0) * 0.4 +
             row.get("F1: Budget (Encoded)", 0) * 2.0 +
             row.get("DERIVED: Adoption Score (0-11)", 0) * 0.5 +
             row.get("DERIVED: WTP Midpoint (USD)", 0) / 10000)
        score_map[ci] = s

    ranked = sorted(score_map, key=score_map.get, reverse=True)
    personas = {}
    for rank, ci in enumerate(ranked):
        p = PERSONA_DEFS[rank % len(PERSONA_DEFS)]
        personas[ci] = p

    return {
        "df_c":       df_c,
        "labels":     labels.tolist(),
        "profile":    profile,
        "personas":   personas,        # {cluster_id: (name, color, fill)}
        "inertias":   inertias,
        "silhouette": sil,
        "pca2_var":   pca2.explained_variance_ratio_.tolist(),
        "pca3_var":   pca3.explained_variance_ratio_.tolist(),
        "n_clusters": n_clusters,
        "cf":         CLUSTER_FEATURES,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 3. ASSOCIATION RULES
# ═══════════════════════════════════════════════════════════════════════════════
def run_association_rules(df):
    t = pd.DataFrame()
    t["High_Urgency"]    = (df["DERIVED: Urgency Composite (0-13)"] >= 10).astype(int)
    t["EU_Exporter"]     = (df["A6: EU Export (Encoded)"] >= 2).astype(int)
    t["Large_Company"]   = (df["A4: Company Size (Encoded)"] >= 4).astype(int)
    t["High_Budget"]     = (df["F1: Budget (Encoded)"] >= 3).astype(int)
    t["POC_Ready"]       = (df["H4: POC Willingness (Encoded)"] >= 2).astype(int)
    t["CBAM_Aware"]      = (df["C1: CBAM Awareness (1-5)"] >= 4).astype(int)
    t["High_Adoption"]   = (df["DERIVED: Adoption Score (0-11)"] >= 7).astype(int)
    t["Promoter"]        = (df["E8: NPS Score (0-10)"] >= 9).astype(int)
    t["High_Pain"]       = (df["DERIVED: Pain Severity Avg (1-5)"] >= 4.0).astype(int)
    t["Open_Startup"]    = (df["G6: Startup Openness (Encoded)"] >= 2).astype(int)
    t["High_WTP"]        = (df["DERIVED: WTP Midpoint (USD)"] >= 20000).astype(int)
    t["No_ESG_Tool"]     = (df["G1: Tool Status (Encoded)"] <= 2).astype(int)
    t["Manufacturing"]   = (df["A3: Industry Sector"] == "Manufacturing").astype(int)
    t["UAE_Based"]       = (df["A5: HQ Region"] == "UAE").astype(int)

    items = t.columns.tolist()
    n = len(t)
    rules = []
    for ant in items:
        for con in items:
            if ant == con:
                continue
            both    = int((t[ant] & t[con]).sum())
            ant_cnt = int(t[ant].sum())
            con_cnt = int(t[con].sum())
            if ant_cnt == 0 or con_cnt == 0:
                continue
            sup  = both / n
            conf = both / ant_cnt
            lift = conf / (con_cnt / n)
            if sup >= 0.10 and conf >= 0.50 and lift >= 1.0:
                rules.append({
                    "Antecedent":  ant,
                    "Consequent":  con,
                    "Support":     round(sup, 3),
                    "Confidence":  round(conf, 3),
                    "Lift":        round(lift, 3),
                })

    rules_df = (pd.DataFrame(rules)
                .sort_values("Lift", ascending=False)
                .drop_duplicates(subset=["Antecedent", "Consequent"])
                .reset_index(drop=True))

    # Co-occurrence matrix (for heatmap)
    co = np.zeros((len(items), len(items)))
    for i, a in enumerate(items):
        for j, b in enumerate(items):
            co[i, j] = float((t[a] & t[b]).mean()) if i != j else float(t[a].mean())

    RULE_INSIGHTS = {
        ("High_Urgency", "CBAM_Aware"):    "Urgent buyers are almost always CBAM-aware — lead all outbound with CBAM deadline messaging.",
        ("EU_Exporter",  "CBAM_Aware"):    "EU exporters are 1.5× more CBAM-aware — target UAE exporters to EU on LinkedIn for instant resonance.",
        ("Large_Company","High_WTP"):      "Large firms reliably have high WTP — pitch enterprise tier ($35K+) directly to 1000+ employee prospects.",
        ("High_Pain",    "POC_Ready"):     "Pain-heavy buyers immediately want a POC — qualify pain score in discovery; trigger POC offer on the same call.",
        ("CBAM_Aware",   "High_Urgency"):  "CBAM awareness directly drives urgency — every CBAM education touchpoint shortens the sales cycle.",
        ("High_Adoption","Promoter"):      "High-adoption prospects become promoters — activate reference programme at 90 days post-onboarding.",
        ("Open_Startup", "POC_Ready"):     "Startup-open prospects are the easiest POC conversions — segment and fast-track these in CRM.",
        ("No_ESG_Tool",  "High_Urgency"):  "Tool-less + high-urgency = easiest close — these prospects have no switching cost and urgent deadlines.",
        ("Manufacturing","High_Urgency"):  "Manufacturers are disproportionately urgent — allocate 40% of sales capacity to this vertical.",
        ("Promoter",     "POC_Ready"):     "NPS promoters are ready to trial — use them as reference accounts to lower enterprise prospect hesitancy.",
    }

    return {
        "rules_df":  rules_df,
        "trans":     t,
        "items":     items,
        "co_matrix": co,
        "insights":  RULE_INSIGHTS,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 4. REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════
REG_FEATURES = [
    'A4: Company Size (Encoded)',
    'A6: EU Export (Encoded)',
    'B1: Sustainability Maturity (1-5)',
    'C1: CBAM Awareness (1-5)',
    'C4: Regulatory Investment Influence (1-5)',
    'C6: Solution Urgency (Encoded)',
    'D1: Scope3 Tracking Challenge (1-5)',
    'D3: ESG Cost (Encoded)',
    'D7: Unified Platform Gap Severity (1-5)',
    'E7: POC Trial Likelihood (1-5)',
    'F1: Budget (Encoded)',
    'G5: Local Compliance Importance (1-5)',
    'G6: Startup Openness (Encoded)',
    'H1: Procurement Cycle (Encoded)',
]

REG_LABELS = {f: FEATURE_LABELS.get(f, f.split(":")[-1].strip()) for f in REG_FEATURES}


def run_regression(df):
    X  = df[REG_FEATURES].values.astype(float)
    sc = StandardScaler()

    results = {}

    # ── WTP Regression ────────────────────────────────────────────────────────
    y_wtp = df["DERIVED: WTP Midpoint (USD)"].values.astype(float)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y_wtp, test_size=0.25, random_state=42)
    X_tr_s = sc.fit_transform(X_tr); X_te_s = sc.transform(X_te)
    gb_wtp = GradientBoostingRegressor(n_estimators=300, max_depth=4,
                                        learning_rate=0.05, random_state=42)
    gb_wtp.fit(X_tr_s, y_tr)
    wtp_pred = gb_wtp.predict(X_te_s)
    results["wtp_r2"]   = round(float(r2_score(y_te, wtp_pred)), 4)
    results["wtp_rmse"] = round(float(np.sqrt(mean_squared_error(y_te, wtp_pred))), 0)
    results["wtp_actual"] = y_te.tolist()
    results["wtp_pred"]   = wtp_pred.tolist()

    wtp_fi = pd.DataFrame({
        "feature":    REG_FEATURES,
        "label":      [REG_LABELS[f] for f in REG_FEATURES],
        "importance": gb_wtp.feature_importances_,
    }).sort_values("importance", ascending=False)
    results["wtp_fi"] = wtp_fi

    # ── Adoption Score Regression ─────────────────────────────────────────────
    y_adp = df["DERIVED: Adoption Score (0-11)"].values.astype(float)
    X_tr2, X_te2, y_tr2, y_te2 = train_test_split(X, y_adp, test_size=0.25, random_state=42)
    X_tr2_s = sc.fit_transform(X_tr2); X_te2_s = sc.transform(X_te2)
    gb_adp = GradientBoostingRegressor(n_estimators=300, max_depth=4,
                                        learning_rate=0.05, random_state=42)
    gb_adp.fit(X_tr2_s, y_tr2)
    adp_pred = gb_adp.predict(X_te2_s)
    results["adp_r2"]   = round(float(r2_score(y_te2, adp_pred)), 4)
    results["adp_rmse"] = round(float(np.sqrt(mean_squared_error(y_te2, adp_pred))), 3)
    results["adp_actual"] = y_te2.tolist()
    results["adp_pred"]   = adp_pred.tolist()

    adp_fi = pd.DataFrame({
        "feature":    REG_FEATURES,
        "label":      [REG_LABELS[f] for f in REG_FEATURES],
        "importance": gb_adp.feature_importances_,
    }).sort_values("importance", ascending=False)
    results["adp_fi"] = adp_fi

    # ── 24-month MRR Forecast ─────────────────────────────────────────────────
    months = list(range(1, 25))
    churn  = 0.018

    def mrr_curve(conv_rate, acv):
        clients = 0.0
        mrr = []
        for m in months:
            new = max(1, round(50 * conv_rate * (1 + 0.025 * m)))
            clients = clients * (1 - churn) + new
            mrr.append(round(clients * acv / 12))
        return mrr

    forecast = pd.DataFrame({
        "Month":          months,
        "Optimistic MRR": mrr_curve(0.35, 27000),
        "Base Case MRR":  mrr_curve(0.25, 18000),
        "Pessimistic MRR":mrr_curve(0.15, 12600),
    })
    results["forecast"] = forecast

    # ── Van Westendorp stats ──────────────────────────────────────────────────
    vw = {
        "Too Cheap":    float(df["F2: VW Too Cheap (USD/yr)"].mean()),
        "Good Value":   float(df["F3: VW Good Value (USD/yr)"].mean()),
        "Expensive OK": float(df["F4: VW Expensive (USD/yr)"].mean()),
        "Too Expensive":float(df["F5: VW Too Expensive (USD/yr)"].mean()),
    }
    results["vw"] = vw

    # Raw VW columns for box plot
    results["vw_raw"] = {
        "Too Cheap":    df["F2: VW Too Cheap (USD/yr)"].tolist(),
        "Good Value":   df["F3: VW Good Value (USD/yr)"].tolist(),
        "Expensive OK": df["F4: VW Expensive (USD/yr)"].tolist(),
        "Too Expensive":df["F5: VW Too Expensive (USD/yr)"].tolist(),
    }

    return results
