"""
GridWise — Plateforme de dimensionnement des infrastructures de recharge VE
Développée par Aminata Badiane Mbaye | EPT Thiès | 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from fpdf import FPDF
import io, math, datetime

# ── Configuration page ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GridWise",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS personnalisé ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-title {
        color: #00d4aa;
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin: 0;
    }
    .main-subtitle {
        color: #a0aec0;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    .metric-card {
        background: #f8fafc;
        border-left: 4px solid #00d4aa;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #718096;
    }
    .alert-ok {
        background: #f0fff4;
        border: 1px solid #68d391;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #276749;
    }
    .alert-warn {
        background: #fffbeb;
        border: 1px solid #f6ad55;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #744210;
    }
    .alert-danger {
        background: #fff5f5;
        border: 1px solid #fc8181;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #742a2a;
    }
    .section-header {
        color: #0f3460;
        border-bottom: 2px solid #00d4aa;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .footer {
        text-align: center;
        color: #a0aec0;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# ── En-tête ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <p class="main-title">⚡ GridWise</p>
    <p class="main-subtitle">Plateforme de dimensionnement des infrastructures de recharge pour véhicules électriques<br>
    Contexte Afrique de l'Ouest · Réseau SENELEC · Normes CEI 61000 · IEEE 519</p>
</div>
""", unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/electric-vehicle.png", width=80)
st.sidebar.markdown("## ⚡ GridWise")
st.sidebar.markdown("*Dimensionnement VE — Afrique de l'Ouest*")
st.sidebar.markdown("---")

module = st.sidebar.radio(
    "📋 Modules",
    [
        "🏠 Accueil",
        "📍 1. Données du site",
        "🔌 2. Dimensionnement électrique",
        "📊 3. Qualité de l'énergie",
        "💰 4. Analyse économique",
        "📄 5. Rapport PDF"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Développée par**")
st.sidebar.markdown("Aminata Badiane Mbaye")
st.sidebar.markdown("*Ingénieure EnR/EE — EPT Thiès*")
st.sidebar.markdown(f"*v1.0 · {datetime.date.today().year}*")

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 0 : ACCUEIL
# ══════════════════════════════════════════════════════════════════════════════
if module == "🏠 Accueil":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">5</div>
            <div class="metric-label">Modules intégrés</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">IEC + IEEE</div>
            <div class="metric-label">Normes internationales</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">SENELEC</div>
            <div class="metric-label">Tarifs & paramètres réseau</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 Comment utiliser GridWise ?")

    steps = {
        "📍 Étape 1 — Données du site": "Renseignez le nombre et type de bornes, les heures d'usage et le tarif SENELEC applicable.",
        "🔌 Étape 2 — Dimensionnement électrique": "Obtenez la puissance souscrite optimale, la section des câbles, le disjoncteur et le transformateur recommandés.",
        "📊 Étape 3 — Qualité de l'énergie": "Vérifiez la conformité aux normes CEI 61000-3-12 et IEEE 519 : THD(I), harmoniques, FHL.",
        "💰 Étape 4 — Analyse économique": "Calculez le CAPEX, l'OPEX, les pénalités SENELEC évitées et le retour sur investissement.",
        "📄 Étape 5 — Rapport PDF": "Générez un rapport complet et professionnel à remettre à votre client ou bailleur.",
    }

    for title, desc in steps.items():
        with st.expander(title):
            st.write(desc)

    st.markdown("---")
    st.info("👈 **Commencez par le Module 1** dans le menu à gauche.")

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1 : DONNÉES DU SITE
# ══════════════════════════════════════════════════════════════════════════════
elif module == "📍 1. Données du site":
    st.markdown("<h2 class='section-header'>📍 Données du site</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🏢 Identification du site")
        st.session_state['nom_site'] = st.text_input("Nom du site", "Station SGM Sacré-Cœur")
        st.session_state['pays'] = st.selectbox("Pays", ["Sénégal", "Côte d'Ivoire", "Mali", "Burkina Faso", "Guinée", "Autre"])
        st.session_state['ville'] = st.text_input("Ville", "Dakar")
        st.session_state['tension_reseau'] = st.selectbox("Tension réseau (V)", [380, 400, 415], index=0)

    with col2:
        st.markdown("#### 🔌 Configuration des bornes")
        st.session_state['type_borne'] = st.selectbox(
            "Type de borne",
            ["DC Rapide (50–120 kW)", "DC Ultra-rapide (150–350 kW)", "AC Standard (7–22 kW)", "AC Accélérée (22–43 kW)"]
        )
        st.session_state['puissance_borne'] = st.number_input("Puissance unitaire par borne (kW)", min_value=3.7, max_value=350.0, value=120.0, step=0.1)
        st.session_state['nb_bornes'] = st.number_input("Nombre de bornes", min_value=1, max_value=50, value=2)
        st.session_state['simultaneite'] = st.slider(
            "Taux de simultanéité (%)",
            min_value=10, max_value=100, value=80,
            help="Pourcentage de bornes fonctionnant simultanément en heure de pointe"
        )

    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### ⏱️ Profil d'usage")
        st.session_state['heures_jour'] = st.number_input("Heures d'exploitation par jour", min_value=1, max_value=24, value=16)
        st.session_state['jours_semaine'] = st.number_input("Jours d'exploitation par semaine", min_value=1, max_value=7, value=7)
        st.session_state['taux_occupation'] = st.slider(
            "Taux d'occupation moyen (%)",
            min_value=5, max_value=100, value=40,
            help="Proportion du temps où les bornes sont effectivement utilisées"
        )

    with col4:
        st.markdown("#### 💡 Tarif SENELEC")
        st.session_state['tarif'] = st.selectbox(
            "Tarif applicable",
            ["BT — Tarif Général (TG)", "BT — Tarif Prime Fixe (PFP)", "MT — Moyenne Tension"]
        )
        if "PFP" in st.session_state.get('tarif', ''):
            st.session_state['ps_actuelle'] = st.number_input("Puissance souscrite actuelle (kW)", min_value=0, max_value=5000, value=70)
            st.info("💡 Tarif PFP : Prime fixe = 2 868,39 FCFA/kW/mois")
        st.session_state['prix_kwh'] = st.number_input("Prix kWh revendu aux clients (FCFA)", min_value=0, max_value=5000, value=650)

    # Résumé
    st.markdown("---")
    st.markdown("#### 📋 Résumé de la configuration")
    nb = st.session_state.get('nb_bornes', 2)
    pu = st.session_state.get('puissance_borne', 120)
    simul = st.session_state.get('simultaneite', 80) / 100
    p_total = nb * pu
    p_pointe = p_total * simul

    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("Puissance installée totale", f"{p_total:.0f} kW")
    with col6:
        st.metric("Puissance de pointe estimée", f"{p_pointe:.0f} kW")
    with col7:
        courant = p_pointe / (math.sqrt(3) * st.session_state.get('tension_reseau', 380) / 1000)
        st.metric("Courant de pointe estimé", f"{courant:.1f} A")

    st.session_state['p_total'] = p_total
    st.session_state['p_pointe'] = p_pointe
    st.session_state['courant_pointe'] = courant

    st.success("✅ Données du site enregistrées. Passez au Module 2 →")

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2 : DIMENSIONNEMENT ÉLECTRIQUE
# ══════════════════════════════════════════════════════════════════════════════
elif module == "🔌 2. Dimensionnement électrique":
    st.markdown("<h2 class='section-header'>🔌 Dimensionnement électrique</h2>", unsafe_allow_html=True)

    p_pointe = st.session_state.get('p_pointe', 192)
    tension = st.session_state.get('tension_reseau', 380)
    nb_bornes = st.session_state.get('nb_bornes', 2)

    # ── Puissance souscrite recommandée ───────────────────────────────────────
    st.markdown("#### ⚡ Puissance souscrite recommandée")
    marge = st.slider("Marge de sécurité sur la puissance souscrite (%)", 10, 40, 20)
    ps_recommandee = p_pointe * (1 + marge / 100)

    # Arrondir aux paliers SENELEC standard
    paliers = [6, 9, 12, 15, 18, 24, 30, 36, 45, 54, 63, 72, 90, 108, 126, 144, 162, 180, 200, 250, 315, 400, 500, 630, 800, 1000]
    ps_finale = next((p for p in paliers if p >= ps_recommandee), ps_recommandee)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Puissance de pointe", f"{p_pointe:.0f} kW")
    with col2:
        st.metric("PS recommandée (avec marge)", f"{ps_recommandee:.0f} kW")
    with col3:
        st.metric("PS standard SENELEC", f"{ps_finale:.0f} kW", delta="palier normalisé")

    st.session_state['ps_finale'] = ps_finale

    # ── Section câbles ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🔗 Section des câbles d'alimentation")

    longueur = st.number_input("Longueur du câble principal (m)", min_value=5, max_value=500, value=30)
    materiau = st.radio("Matériau conducteur", ["Cuivre (Cu)", "Aluminium (Al)"], horizontal=True)
    chute_max = st.number_input("Chute de tension admissible (%)", min_value=1.0, max_value=5.0, value=3.0)

    rho = 0.01786 if "Cuivre" in materiau else 0.02941  # Ω·mm²/m
    I_calcul = p_pointe * 1000 / (math.sqrt(3) * tension)
    # Section par chute de tension : S = (√3 × ρ × L × I) / (ΔU × U)
    delta_u = tension * chute_max / 100
    S_calc = (math.sqrt(3) * rho * longueur * I_calcul) / delta_u
    # Section normalisée (mm²)
    sections_norm = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
    S_norm = next((s for s in sections_norm if s >= S_calc), 300)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Courant de calcul", f"{I_calcul:.1f} A")
    with col5:
        st.metric("Section calculée", f"{S_calc:.1f} mm²")
    with col6:
        st.metric("Section normalisée", f"{S_norm} mm²", delta="selon NF C 15-100")

    # ── Disjoncteur ───────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🔒 Protection — Disjoncteur général")

    # Calibre = 1.25 × In
    calibre_calc = I_calcul * 1.25
    calibres_norm = [16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600]
    calibre_norm = next((c for c in calibres_norm if c >= calibre_calc), 1600)

    col7, col8 = st.columns(2)
    with col7:
        st.metric("Calibre calculé (1,25 × In)", f"{calibre_calc:.0f} A")
    with col8:
        st.metric("Calibre normalisé recommandé", f"{calibre_norm} A", delta="4P")

    # ── Transformateur ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🏭 Transformateur")

    besoin_transfo = p_pointe > 100
    if besoin_transfo:
        st.warning(f"⚠️ Puissance > 100 kW → raccordement MT/BT probablement nécessaire.")
        # Puissance transfo avec marge harmonique (FHL)
        fhl = st.slider("Facteur de déclassement harmonique FHL (IEEE C57.110)", 1.0, 2.5, 1.8, 0.1)
        s_transfo_calc = ps_finale / 0.9 * fhl  # cos φ = 0.9 supposé
        transfo_norm = [100, 160, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000]
        s_transfo_norm = next((t for t in transfo_norm if t >= s_transfo_calc), 2000)

        col9, col10 = st.columns(2)
        with col9:
            st.metric("Puissance transfo calculée (avec FHL)", f"{s_transfo_calc:.0f} kVA")
        with col10:
            st.metric("Puissance transfo normalisée", f"{s_transfo_norm} kVA")
        st.session_state['s_transfo'] = s_transfo_norm
    else:
        st.info("✅ Puissance ≤ 100 kW — raccordement BT direct possible.")
        st.session_state['s_transfo'] = 0

    # Résumé dimensionnement
    st.markdown("---")
    st.markdown("#### 📋 Récapitulatif du dimensionnement")
    recap = {
        "Paramètre": ["Puissance souscrite", "Section câble", "Calibre disjoncteur", "Transformateur"],
        "Valeur recommandée": [
            f"{ps_finale} kW",
            f"{S_norm} mm² {materiau[:2]}",
            f"{calibre_norm} A — 4P",
            f"{st.session_state.get('s_transfo', 'N/A')} kVA" if besoin_transfo else "Non requis"
        ]
    }
    st.dataframe(pd.DataFrame(recap), use_container_width=True, hide_index=True)

    st.session_state['section_cable'] = S_norm
    st.session_state['calibre_disj'] = calibre_norm
    st.session_state['I_calcul'] = I_calcul

    st.success("✅ Dimensionnement calculé. Passez au Module 3 →")

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 3 : QUALITÉ DE L'ÉNERGIE
# ══════════════════════════════════════════════════════════════════════════════
elif module == "📊 3. Qualité de l'énergie":
    st.markdown("<h2 class='section-header'>📊 Qualité de l'énergie</h2>", unsafe_allow_html=True)

    st.markdown("#### 📥 Source des données harmoniques")
    source = st.radio(
        "Comment renseigner les harmoniques ?",
        ["Saisie manuelle (mesures terrain)", "Estimation par défaut (DC rapide 120 kW)"],
        horizontal=True
    )

    if source == "Estimation par défaut (DC rapide 120 kW)":
        # Valeurs issues de la campagne de mesure PFE (Site A, SGM Sacré-Cœur)
        thd_i = 4.5
        h5 = 4.5; h7 = 3.1; h11 = 1.8; h13 = 1.2
        thd_v = 2.1
        fp = 0.97
        st.info("📊 Valeurs par défaut issues de la campagne de mesures (PEL 102, Site A — SGM Sacré-Cœur, Dakar, juin 2026)")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Courant**")
            thd_i = st.number_input("THD(I) mesuré (%)", 0.0, 100.0, 4.5, 0.1)
            h5 = st.number_input("H5 (%)", 0.0, 50.0, 4.5, 0.1)
            h7 = st.number_input("H7 (%)", 0.0, 50.0, 3.1, 0.1)
            h11 = st.number_input("H11 (%)", 0.0, 50.0, 1.8, 0.1)
            h13 = st.number_input("H13 (%)", 0.0, 50.0, 1.2, 0.1)
        with col2:
            st.markdown("**Tension**")
            thd_v = st.number_input("THD(V) mesuré (%)", 0.0, 20.0, 2.1, 0.1)
            fp = st.number_input("Facteur de puissance (cos φ)", 0.5, 1.0, 0.97, 0.01)

    st.markdown("---")
    st.markdown("#### ✅ Conformité normative")

    # CEI 61000-3-12 (courant, In > 16A)
    limite_thdi_iec = 8.0
    limite_h5 = 10.0
    limite_h7 = 8.0
    limite_h11 = 5.0
    limite_h13 = 4.0

    # EN 50160 (tension)
    limite_thdv_en = 8.0

    # IEEE 519-2022 (tension au PCC)
    limite_thdv_ieee = 5.0

    normes = {
        "Paramètre": ["THD(I)", "H5", "H7", "H11", "H13", "THD(V)", "THD(V)"],
        "Norme": ["CEI 61000-3-12", "CEI 61000-3-12", "CEI 61000-3-12", "CEI 61000-3-12", "CEI 61000-3-12", "EN 50160", "IEEE 519-2022"],
        "Limite (%)": [limite_thdi_iec, limite_h5, limite_h7, limite_h11, limite_h13, limite_thdv_en, limite_thdv_ieee],
        "Mesuré (%)": [thd_i, h5, h7, h11, h13, thd_v, thd_v],
        "Statut": []
    }

    for m, l in zip(normes["Mesuré (%)"], normes["Limite (%)"]):
        if m <= l * 0.8:
            normes["Statut"].append("✅ Conforme")
        elif m <= l:
            normes["Statut"].append("⚠️ Limite")
        else:
            normes["Statut"].append("❌ Non conforme")

    df_normes = pd.DataFrame(normes)
    st.dataframe(df_normes, use_container_width=True, hide_index=True)

    # ── Graphique spectre harmonique ──────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📈 Spectre harmonique du courant")

    harmoniques = [1, 5, 7, 11, 13]
    amplitudes = [100, h5, h7, h11, h13]
    limites_harm = [None, limite_h5, limite_h7, limite_h11, limite_h13]

    fig, ax = plt.subplots(figsize=(8, 4))
    couleurs = ['#0f3460' if h == 1 else ('#e74c3c' if (limites_harm[i] and amplitudes[i] > limites_harm[i]) else '#00d4aa')
                for i, h in enumerate(harmoniques)]
    bars = ax.bar([f"H{h}" for h in harmoniques], amplitudes, color=couleurs, width=0.5, zorder=3)

    # Limites
    for i, (h, lim) in enumerate(zip(harmoniques, limites_harm)):
        if lim:
            ax.hlines(lim, i - 0.35, i + 0.35, colors='red', linestyles='--', linewidth=1.5)

    ax.set_ylabel("Amplitude (% du fondamental)")
    ax.set_title("Spectre harmonique du courant — CEI 61000-3-12")
    ax.set_ylim(0, max(amplitudes) * 1.3)
    ax.grid(axis='y', alpha=0.3, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    patch_lim = mpatches.Patch(color='red', linestyle='--', fill=False, label='Limite CEI 61000-3-12')
    patch_ok = mpatches.Patch(color='#00d4aa', label='Conforme')
    patch_nok = mpatches.Patch(color='#e74c3c', label='Non conforme')
    ax.legend(handles=[patch_lim, patch_ok, patch_nok], loc='upper right', fontsize=8)

    st.pyplot(fig)
    plt.close()

    # ── FHL ───────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🏭 Facteur de déclassement harmonique (FHL — IEEE C57.110)")

    # FHL = Σ(Ih²/I1² × h²) / Σ(Ih²/I1²)
    ih_rel = [h5/100, h7/100, h11/100, h13/100]
    h_nums = [5, 7, 11, 13]
    num = sum(ih**2 * h**2 for ih, h in zip(ih_rel, h_nums))
    den = sum(ih**2 for ih in ih_rel) + 1  # +1 pour le fondamental normalisé
    fhl = 1 + num / den if den > 0 else 1.0

    col3, col4 = st.columns(2)
    with col3:
        st.metric("FHL calculé", f"{fhl:.2f}")
    with col4:
        if fhl < 1.5:
            st.markdown('<div class="alert-ok">✅ Déclassement faible — transformateur standard acceptable</div>', unsafe_allow_html=True)
        elif fhl < 2.0:
            st.markdown('<div class="alert-warn">⚠️ Déclassement modéré — prévoir transformateur de type K ou déclassement de 15–20%</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-danger">❌ Déclassement élevé — transformateur K-factor obligatoire</div>', unsafe_allow_html=True)

    st.session_state['thd_i'] = thd_i
    st.session_state['thd_v'] = thd_v
    st.session_state['fhl'] = fhl
    st.session_state['fp'] = fp
    st.session_state['h5'] = h5
    st.session_state['h7'] = h7

    st.success("✅ Analyse qualité énergie terminée. Passez au Module 4 →")

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 4 : ANALYSE ÉCONOMIQUE
# ══════════════════════════════════════════════════════════════════════════════
elif module == "💰 4. Analyse économique":
    st.markdown("<h2 class='section-header'>💰 Analyse économique</h2>", unsafe_allow_html=True)

    nb_bornes = st.session_state.get('nb_bornes', 2)
    pu_borne = st.session_state.get('puissance_borne', 120)
    ps_finale = st.session_state.get('ps_finale', 250)
    heures = st.session_state.get('heures_jour', 16)
    jours = st.session_state.get('jours_semaine', 7)
    taux_occ = st.session_state.get('taux_occupation', 40) / 100
    prix_kwh_client = st.session_state.get('prix_kwh', 650)

    st.markdown("#### 💸 CAPEX — Investissement initial")
    col1, col2 = st.columns(2)
    with col1:
        cout_borne = st.number_input("Coût unitaire borne DC (FCFA)", 0, 100_000_000, 15_000_000, 500_000,
                                      help="Borne DC 120 kW : environ 12–18 M FCFA")
        cout_genie_civil = st.number_input("Génie civil & raccordement (FCFA)", 0, 50_000_000, 5_000_000, 500_000)
        cout_transfo = st.number_input("Transformateur + TGBT (FCFA)", 0, 30_000_000, 8_000_000, 500_000)
    with col2:
        cout_etude = st.number_input("Études & ingénierie (FCFA)", 0, 10_000_000, 2_000_000, 100_000)
        cout_divers = st.number_input("Divers & imprévus (FCFA)", 0, 10_000_000, 1_500_000, 100_000)

    capex_total = nb_bornes * cout_borne + cout_genie_civil + cout_transfo + cout_etude + cout_divers

    st.metric("**CAPEX TOTAL**", f"{capex_total:,.0f} FCFA", delta=f"≈ {capex_total/655.957:,.0f} €")

    st.markdown("---")
    st.markdown("#### 📅 OPEX — Charges annuelles")

    col3, col4 = st.columns(2)
    with col3:
        # Facture SENELEC annuelle
        p_moy = pu_borne * nb_bornes * taux_occ
        energie_annuelle = p_moy * heures * jours * 52  # kWh/an
        tarif_kwh_senelec = st.number_input("Tarif SENELEC achat kWh (FCFA)", 50, 500, 145)
        facture_energie = energie_annuelle * tarif_kwh_senelec

        # Prime fixe PFP
        prime_fixe = st.number_input("Prime fixe SENELEC/mois (FCFA/kW)", 0, 10000, 2868)
        facture_prime = prime_fixe * ps_finale * 12

    with col4:
        maintenance = st.number_input("Maintenance annuelle (FCFA)", 0, 20_000_000, 2_000_000, 100_000)
        assurance = st.number_input("Assurance annuelle (FCFA)", 0, 5_000_000, 500_000, 50_000)
        salaires = st.number_input("Personnel (FCFA/an)", 0, 20_000_000, 3_600_000, 100_000)

    opex_annuel = facture_energie + facture_prime + maintenance + assurance + salaires

    st.markdown("---")
    st.markdown("#### 💹 Revenus annuels")
    revenus_annuels = energie_annuelle * prix_kwh_client

    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("Énergie vendue/an", f"{energie_annuelle:,.0f} kWh")
    with col6:
        st.metric("Revenus bruts/an", f"{revenus_annuels:,.0f} FCFA")
    with col7:
        marge_brute = revenus_annuels - opex_annuel
        st.metric("Marge brute/an", f"{marge_brute:,.0f} FCFA",
                  delta="bénéfice" if marge_brute > 0 else "déficit")

    # ROI
    st.markdown("---")
    st.markdown("#### 📊 Retour sur investissement (ROI)")

    if marge_brute > 0:
        roi_ans = capex_total / marge_brute
        col8, col9 = st.columns(2)
        with col8:
            st.metric("ROI estimé", f"{roi_ans:.1f} ans")
        with col9:
            if roi_ans < 5:
                st.markdown('<div class="alert-ok">✅ Excellent — ROI < 5 ans</div>', unsafe_allow_html=True)
            elif roi_ans < 10:
                st.markdown('<div class="alert-warn">⚠️ Acceptable — ROI entre 5 et 10 ans</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-danger">❌ Long — ROI > 10 ans, revoir les paramètres</div>', unsafe_allow_html=True)

        # Graphique cash flow cumulé
        annees = list(range(0, 16))
        cashflow_cumul = [-capex_total + marge_brute * a for a in annees]

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        couleurs_cf = ['#00d4aa' if v >= 0 else '#e74c3c' for v in cashflow_cumul]
        ax2.bar(annees, [v/1_000_000 for v in cashflow_cumul], color=couleurs_cf, zorder=3)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.set_xlabel("Années")
        ax2.set_ylabel("Cash flow cumulé (M FCFA)")
        ax2.set_title("Évolution du cash flow cumulé")
        ax2.grid(axis='y', alpha=0.3, zorder=0)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        st.pyplot(fig2)
        plt.close()
    else:
        st.error("⚠️ Le projet n'est pas rentable avec ces paramètres. Augmentez le prix de vente ou réduisez les charges.")

    # Sauvegarde pour rapport
    st.session_state['capex'] = capex_total
    st.session_state['opex'] = opex_annuel
    st.session_state['revenus'] = revenus_annuels
    st.session_state['marge'] = marge_brute
    st.session_state['energie_an'] = energie_annuelle
    st.session_state['roi'] = capex_total / marge_brute if marge_brute > 0 else 0

    st.success("✅ Analyse économique terminée. Passez au Module 5 pour générer votre rapport →")

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 5 : RAPPORT PDF
# ══════════════════════════════════════════════════════════════════════════════
elif module == "📄 5. Rapport PDF":
    st.markdown("<h2 class='section-header'>📄 Rapport de dimensionnement</h2>", unsafe_allow_html=True)

    st.info("📋 Le rapport récapitule tous les résultats des modules 1 à 4.")

    nom_client = st.text_input("Nom du client / promoteur", "Sénégal Green Mobility")
    ref_projet = st.text_input("Référence projet", f"GW-{datetime.date.today().strftime('%Y%m%d')}-001")
    ingenieur = st.text_input("Ingénieur(e) responsable", "Aminata Badiane Mbaye")

    if st.button("📄 Générer le rapport PDF", type="primary"):
        pdf = FPDF()
        pdf.add_page()

        # En-tête
        pdf.set_fill_color(15, 52, 96)
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_text_color(0, 212, 170)
        pdf.set_font("Helvetica", "B", 24)
        pdf.set_xy(10, 10)
        pdf.cell(0, 10, "GridWise", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(200, 200, 200)
        pdf.cell(0, 6, "Rapport de dimensionnement d'infrastructure de recharge VE", ln=True)
        pdf.ln(15)

        # Infos projet
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "INFORMATIONS PROJET", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(60, 6, "Client :", border=0)
        pdf.cell(0, 6, nom_client, ln=True)
        pdf.cell(60, 6, "Référence :", border=0)
        pdf.cell(0, 6, ref_projet, ln=True)
        pdf.cell(60, 6, "Site :", border=0)
        pdf.cell(0, 6, f"{st.session_state.get('nom_site','—')} — {st.session_state.get('ville','—')}", ln=True)
        pdf.cell(60, 6, "Date :", border=0)
        pdf.cell(0, 6, datetime.date.today().strftime("%d/%m/%Y"), ln=True)
        pdf.cell(60, 6, "Ingénieur(e) :", border=0)
        pdf.cell(0, 6, ingenieur, ln=True)
        pdf.ln(5)

        # Section 1
        pdf.set_fill_color(0, 212, 170)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, "  1. CONFIGURATION DU SITE", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 10)
        items1 = [
            ("Nombre de bornes", f"{st.session_state.get('nb_bornes','—')}"),
            ("Type de borne", st.session_state.get('type_borne','—')),
            ("Puissance unitaire", f"{st.session_state.get('puissance_borne','—')} kW"),
            ("Puissance installée", f"{st.session_state.get('p_total','—'):.0f} kW"),
            ("Puissance de pointe", f"{st.session_state.get('p_pointe','—'):.0f} kW"),
        ]
        for label, val in items1:
            pdf.cell(80, 6, label + " :", border=0)
            pdf.cell(0, 6, str(val), ln=True)
        pdf.ln(3)

        # Section 2
        pdf.set_fill_color(0, 212, 170)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, "  2. DIMENSIONNEMENT ÉLECTRIQUE", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 10)
        items2 = [
            ("Puissance souscrite recommandée", f"{st.session_state.get('ps_finale','—')} kW"),
            ("Section câble", f"{st.session_state.get('section_cable','—')} mm²"),
            ("Calibre disjoncteur", f"{st.session_state.get('calibre_disj','—')} A — 4P"),
            ("Transformateur", f"{st.session_state.get('s_transfo', 'Non requis')} kVA" if st.session_state.get('s_transfo', 0) > 0 else "Non requis"),
        ]
        for label, val in items2:
            pdf.cell(80, 6, label + " :", border=0)
            pdf.cell(0, 6, str(val), ln=True)
        pdf.ln(3)

        # Section 3
        pdf.set_fill_color(0, 212, 170)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, "  3. QUALITÉ DE L'ÉNERGIE", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 10)
        items3 = [
            ("THD(I)", f"{st.session_state.get('thd_i','—'):.1f} % (limite CEI 61000-3-12 : 8 %)"),
            ("THD(V)", f"{st.session_state.get('thd_v','—'):.1f} % (limite EN 50160 : 8 %)"),
            ("Facteur de puissance", f"{st.session_state.get('fp','—'):.2f}"),
            ("FHL (IEEE C57.110)", f"{st.session_state.get('fhl','—'):.2f}"),
        ]
        for label, val in items3:
            pdf.cell(80, 6, label + " :", border=0)
            pdf.cell(0, 6, str(val), ln=True)
        pdf.ln(3)

        # Section 4
        pdf.set_fill_color(0, 212, 170)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, "  4. ANALYSE ÉCONOMIQUE", ln=True, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 10)
        items4 = [
            ("CAPEX total", f"{st.session_state.get('capex',0):,.0f} FCFA"),
            ("OPEX annuel", f"{st.session_state.get('opex',0):,.0f} FCFA/an"),
            ("Revenus annuels", f"{st.session_state.get('revenus',0):,.0f} FCFA/an"),
            ("Marge brute annuelle", f"{st.session_state.get('marge',0):,.0f} FCFA/an"),
            ("ROI estimé", f"{st.session_state.get('roi',0):.1f} ans"),
        ]
        for label, val in items4:
            pdf.cell(80, 6, label + " :", border=0)
            pdf.cell(0, 6, str(val), ln=True)
        pdf.ln(5)

        # Pied de page
        pdf.set_fill_color(15, 52, 96)
        pdf.set_y(-20)
        pdf.rect(0, pdf.get_y(), 210, 20, 'F')
        pdf.set_text_color(200, 200, 200)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(0, 6, f"GridWise — Rapport généré le {datetime.date.today().strftime('%d/%m/%Y')} | {ingenieur} | Confidentiel", ln=True, align='C')

        # Export
        pdf_bytes = bytes(pdf.output())
        st.download_button(
            label="⬇️ Télécharger le rapport PDF",
            data=pdf_bytes,
            file_name=f"GridWise_{ref_projet}.pdf",
            mime="application/pdf",
            type="primary"
        )
        st.success("✅ Rapport généré avec succès !")

# Footer
st.markdown("""
<div class="footer">
    ⚡ GridWise — Plateforme de dimensionnement d'infrastructures de recharge VE · Afrique de l'Ouest<br>
    Développée par <strong>Aminata Badiane Mbaye</strong> | EPT Thiès | Master EnR/EE | 2026<br>
    Normes : CEI 61000-3-12 · IEEE 519-2022 · EN 50160 · IEEE C57.110 · SENELEC PFP
</div>
""", unsafe_allow_html=True)
