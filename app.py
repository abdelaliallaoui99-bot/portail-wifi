import streamlit as st
import random
import string
import pandas as pd
import io
from datetime import datetime, time, date

# Configuration de la page pour une expérience premium responsive
st.set_page_config(
    page_title="Serval S.A.S - Portail Wi-Fi Visiteurs",
    page_icon="📶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialisation de la base de données simulée en mémoire pour Serval S.A.S
if 'db' not in st.session_state:
    st.session_state.db = {
        'users': {
            'admin': {'password': 'admin123', 'role': 'admin', 'firstname': 'Jean', 'lastname': 'Dupond', 'email': 'admin@serval.fr', 'active': True},
            'accueil': {'password': 'accueil123', 'role': 'accueil', 'firstname': 'Marie', 'lastname': 'Martin', 'email': 'accueil@serval.fr', 'active': True}
        },
        'requests': [
            {
                'id': 1,
                'visitor_lastname': 'Dupont',
                'visitor_firstname': 'Jean',
                'visitor_email': 'jean.dupont@email.com',
                'company': 'DDVH S.A.',
                'host': 'Yanis Talbi',
                'reason': 'Réunion',
                'date': date(2026, 7, 9),
                'start_time': time(9, 0),
                'end_time': time(11, 0),
                'duration': 2.0,
                'rgpd': True,
                'comments': 'Entretien annuel d\'évaluation.',
                'wifi_user': 'serval_dupo44',
                'wifi_pass': 'K9xP2w7Z'
            },
            {
                'id': 2,
                'visitor_lastname': 'Sartre',
                'visitor_firstname': 'Paul',
                'visitor_email': 'p.sartre@solutions.fr',
                'company': 'TechSolutions',
                'host': 'Alice Bernard',
                'reason': 'Maintenance technique',
                'date': date(2026, 7, 8),
                'start_time': time(14, 0),
                'end_time': time(18, 0),
                'duration': 4.0,
                'rgpd': True,
                'comments': 'Maintenance annuelle du serveur principal.',
                'wifi_user': 'serval_sart12',
                'wifi_pass': 'T7pQ9v8B'
            }
        ],
        'emails_sent': []
    }

# Variables d'état pour gérer l'authentification et la navigation interne
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Formulaire"
if 'last_generated_ticket' not in st.session_state:
    st.session_state.last_generated_ticket = None

# Variables temporaires pour réinitialiser le formulaire
if 'form_reset_trigger' not in st.session_state:
    st.session_state.form_reset_trigger = False

# CSS unifié basé sur la charte Serval S.A.S (Vert #004737 & Orange #e05326)
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700;
        color: #004737;
    }
    
    /* En-tête Serval */
    .header-container {
        background-color: #004737;
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border-bottom: 5px solid #e05326;
        display: flex;
        align-items: center;
        gap: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* En-tête de Session Active (Page 2) */
    .serval-header {
        background: linear-gradient(135deg, #004737 0%, #0c6a53 100%);
        padding: 20px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        border-bottom: 5px solid #e05326;
        box-shadow: 0 8px 25px rgba(0, 71, 55, 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .serval-header-left {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .serval-header h1 {
        color: white !important;
        margin: 0 !important;
        font-size: 24px !important;
    }
    .serval-header p {
        color: #f4f7f6;
        margin: 4px 0 0 0;
        font-size: 13px;
        opacity: 0.9;
    }
    
    /* Logo officiel Serval */
    .logo-serval {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-width: 90px;
        background: white;
        padding: 10px;
        border-radius: 8px;
    }
    .logo-icon {
        position: relative;
        width: 35px;
        height: 40px;
    }
    .logo-curve-1 {
        position: absolute;
        width: 26px;
        height: 26px;
        border: 6px solid #e05326;
        border-color: #e05326 transparent transparent #e05326;
        border-radius: 50% 0 50% 50%;
        transform: rotate(-45deg);
        top: 0;
    }
    .logo-curve-2 {
        position: absolute;
        width: 26px;
        height: 26px;
        border: 6px solid #e05326;
        border-color: transparent #e05326 #e05326 transparent;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        bottom: 0;
    }
    .logo-word {
        color: #004737;
        font-weight: bold;
        font-size: 1.2rem;
        font-family: sans-serif;
        margin-top: 0.2rem;
        letter-spacing: 0.5px;
    }
    
    /* Zone de Connexion Agrandie */
    .login-box {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        padding: 2.5rem 2rem;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #e05326;
        margin-top: 0.5rem;
    }
    
    /* Blocs d'information */
    .content-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #004737;
    }
    .content-title {
        color: #004737;
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.8rem;
    }
    
    /* Chiffres clés */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-top: 1.5rem;
    }
    .stat-card {
        background: #f4f7f6;
        padding: 0.8rem;
        border-radius: 6px;
        text-align: center;
        border-bottom: 3px solid #e05326;
    }
    .stat-number {
        color: #004737;
        font-size: 1.3rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #475569;
    }
    
    /* Messages de notification personnalisés */
    .custom-error-banner {
        background-color: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 15px;
        border-radius: 10px;
        color: #991b1b;
        margin-bottom: 20px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .custom-success-banner {
        background-color: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 15px;
        border-radius: 10px;
        color: #166534;
        margin-bottom: 20px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Design du Ticket Wi-Fi Serval */
    .ticket-wrapper {
        display: flex;
        justify-content: center;
        padding: 15px 0;
    }
    .wifi-ticket-card {
        background: #ffffff;
        border: 2px dashed #004737;
        border-radius: 16px;
        width: 440px;
        position: relative;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
        overflow: hidden;
    }
    .ticket-top {
        background-color: #004737;
        color: white;
        padding: 20px;
        text-align: center;
    }
    .ticket-top h3 {
        color: white !important;
        margin: 0 !important;
        font-size: 20px;
        letter-spacing: 1px;
    }
    .ticket-top p {
        color: #f4f7f6;
        margin: 5px 0 0 0;
        font-size: 11px;
        text-transform: uppercase;
        font-weight: 600;
    }
    .ticket-bottom {
        padding: 25px;
        background-color: #ffffff;
    }
    .ticket-info-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 12px;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 6px;
    }
    .ticket-info-label {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
    }
    .ticket-info-value {
        font-size: 13px;
        color: #004737;
        font-weight: 600;
    }
    .ticket-credentials-box {
        background-color: #f4f7f6;
        border-left: 4px solid #e05326;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin-top: 15px;
    }
    .creds-title {
        font-size: 11px;
        color: #004737;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .creds-user, .creds-pass {
        font-family: 'Space Grotesk', monospace;
        font-size: 16px;
        font-weight: 700;
        margin: 4px 0;
    }
    .creds-user span { color: #004737; }
    .creds-pass span { color: #e05326; }
    
    /* Badges de statut */
    .custom-badge-active {
        background-color: #dcfce7;
        color: #15803d;
        padding: 4px 10px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }
    .custom-badge-expired {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 4px 10px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }
    
    /* Boutons personnalisés orange */
    div.stButton > button:first-child {
        background-color: #e05326;
        color: white;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #b83f1b;
        color: white;
    }
    
    /* Conteneur principal (Cartes blanches) */
    .content-card {
        background-color: white;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        margin-bottom: 25px;
    }
    
    .serval-footer {
        text-align: center;
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# --- FONCTIONS REQUISES ---
def check_login(username, password):
    """Vérifie l'exactitude des comptes conformément à la spécification."""
    users = st.session_state.db['users']
    if username in users:
        if users[username]['password'] == password:
            if users[username]['active']:
                st.session_state.logged_in = True
                st.session_state.user_role = users[username]['role']
                st.session_state.username = username
                st.session_state.current_page = "Formulaire"
                st.rerun()
            else:
                return "Ce compte utilisateur est actuellement désactivé."
        else:
            return "Mot de passe incorrect."
    else:
        return f"Identifiant '{username}' inconnu."

def logout():
    """Déconnexion sécurisée de la session."""
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.last_generated_ticket = None
    st.session_state.current_page = "Formulaire"
    st.rerun()

def get_visit_status(visit_date, start_time, end_time):
    """Calcule dynamiquement le statut de la visite en temps réel."""
    today = date(2026, 7, 9) # Date fixe de simulation
    current_time = time(16, 3) # Heure fixe de simulation
    
    if visit_date < today:
        return "Terminé"
    elif visit_date > today:
        return "En cours"
    else:
        if current_time > end_time:
            return "Terminé"
        else:
            return "En cours"

def generate_wifi_credentials(lastname):
    """Génère de manière sécurisée des identifiants Wi-Fi uniques."""
    clean_name = "".join(x for x in lastname.lower() if x.isalnum())[:4]
    random_num = random.randint(10, 99)
    wifi_user = f"serval_{clean_name}{random_num}"
    characters = string.ascii_uppercase + string.digits
    wifi_pass = "".join(random.choice(characters) for _ in range(8))
    return wifi_user, wifi_pass


# ==========================================
# --- ÉCRAN 1 : CONNEXION (PAGE INTERNE 1) ---
# ==========================================
if not st.session_state.logged_in:
    st.markdown("""
    <div class="header-container">
        <div class="logo-serval">
            <div class="logo-icon">
                <div class="logo-curve-1"></div>
                <div class="logo-curve-2"></div>
            </div>
            <div class="logo-word">serval</div>
        </div>
        <div class="header-text-block">
            <div class="header-title" style="color:white; font-size:2rem; font-weight:700;">Serval S.A.S</div>
            <div class="header-subtitle" style="color:#f4f7f6;">Portail de Gestion des Accès Wi-Fi Visiteurs</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.4, 1.6], gap="large")
    
    with col_left:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h3 style="color:#004737; margin-top:0; margin-bottom:1.5rem;">🔑 Connexion Sécurisée</h3>', unsafe_allow_html=True)
        
        username_input = st.text_input("Identifiant", placeholder="Ex: accueil", key="login_username")
        password_input = st.text_input("Mot de passe", type="password", placeholder="••••••••", key="login_password")
        
        st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)
        if st.button("Se connecter", use_container_width=True):
            if not username_input or not password_input:
                st.markdown('<div class="custom-error-banner"><i class="fa-solid fa-circle-exclamation"></i> Veuillez renseigner tous les champs.</div>', unsafe_allow_html=True)
            else:
                err_msg = check_login(username_input, password_input)
                if err_msg:
                    st.markdown(f'<div class="custom-error-banner"><i class="fa-solid fa-circle-exclamation"></i> <span>{err_msg}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_right:
        st.markdown("""
        <div class="content-box">
            <div class="content-title">🌱 Serval, partenaire des éleveurs de demain</div>
            <p style="font-size: 0.9rem; margin-bottom: 0; text-align: justify; color: #334155;">
            <b>Expert de la nutrition des jeunes animaux</b><br>
            Fabricant français d’aliment d’allaitement et de solutions nutritionnelles de haute qualité pour jeunes animaux depuis plus de 60 ans.
            </p>
        </div>
        
        <div class="content-box">
            <div class="content-title">🛡️ Traçabilité &amp; Sécurité Informatique</div>
            <p style="font-size: 0.9rem; margin-bottom: 0; text-align: justify; color: #334155;">
            Chaque ticket d'accès Wi-Fi généré est temporaire, tracé conformément aux réglementations de sécurité du DSI, et transmis de manière éco-conçue directement par e-mail.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div class="stat-grid">
        <div class="stat-card"><div class="stat-number">+ 100 M€</div><div class="stat-label">Chiffre d'affaires</div></div>
        <div class="stat-card"><div class="stat-number">+ 1 000 000</div><div class="stat-label">Animaux nourris / an</div></div>
        <div class="stat-card"><div class="stat-number">4</div><div class="stat-label">Usines dans le monde</div></div>
        <div class="stat-card"><div class="stat-number">+ 100</div><div class="stat-label">Collaborateurs</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="serval-footer">
        Mentions légales - Politique de confidentialité - © 2026 Serval S.A.S - 📍 Sainte-Eanne, France
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# --- MODE CONNECTÉ (PAGES INTERNES) ---
# ==========================================
else:
    # 1. En-tête de session dynamique
    st.markdown(f"""
    <div class="serval-header">
        <div class="serval-header-left">
            <div class="logo-serval">
                <div class="logo-icon">
                    <div class="logo-curve-1"></div>
                    <div class="logo-curve-2"></div>
                </div>
                <div class="logo-word">serval</div>
            </div>
            <div>
                <h1>Serval S.A.S - Portail Wi-Fi</h1>
                <p>Gestionnaire d'accès Internet Visiteurs • Connecté : <b>{st.session_state.username.capitalize()}</b> ({st.session_state.user_role.upper()})</p>
            </div>
        </div>
        <div style="text-align: right;">
            <span class="custom-badge-active" style="background-color: #f4f7f6; color: #004737; font-weight:700;">🟢 CONTRÔLE ACTIF</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Barre de Navigation d'onglets réactifs
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1.2, 1.2, 1.2, 0.8])
    with nav_col1:
        if st.button("📝 Formulaire de déclaration", use_container_width=True, type="primary" if st.session_state.current_page == "Formulaire" else "secondary", key="nav_form"):
            st.session_state.current_page = "Formulaire"
            st.session_state.last_generated_ticket = None
            st.rerun()
    with nav_col2:
        if st.button("📊 Historique des connexions", use_container_width=True, type="primary" if st.session_state.current_page == "Historique" else "secondary", key="nav_dash"):
            st.session_state.current_page = "Historique"
            st.session_state.last_generated_ticket = None
            st.rerun()
    with nav_col3:
        if st.session_state.user_role == 'admin':
            if st.button("⚙️ Gestion des comptes", use_container_width=True, type="primary" if st.session_state.current_page == "Gestion des comptes" else "secondary", key="nav_accounts"):
                st.session_state.current_page = "Gestion des comptes"
                st.session_state.last_generated_ticket = None
                st.rerun()
    with nav_col4:
        if st.button("🚪 Se déconnecter", use_container_width=True, key="nav_logout"):
            logout()

    st.markdown("<br>", unsafe_allow_html=True)


    # ==========================================
    # --- ÉCRAN : FORMULAIRE DE DÉCLARATION ---
    # ==========================================
    if st.session_state.current_page == "Formulaire":
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="margin-top:0;"><i class="fa-solid fa-file-signature"></i> Formulaire de déclaration</h2>', unsafe_allow_html=True)
        st.write("Saisissez les informations du visiteur pour activer son accès temporaire sécurisé.")
        st.markdown("<br>", unsafe_allow_html=True)

        # Réinitialisation forcée des valeurs
        if st.session_state.form_reset_trigger:
            st.session_state.form_reset_trigger = False
            st.session_state.f_lastname = ""
            st.session_state.f_firstname = ""
            st.session_state.f_email = ""
            st.session_state.f_company = ""
            st.session_state.f_host = ""
            st.session_state.f_reason = ""
            st.session_state.f_comments = ""
            st.session_state.f_rgpd = False

        col_f1, col_f2 = st.columns(2, gap="large")
        
        with col_f1:
            visitor_lastname = st.text_input("Nom du visiteur *", placeholder="Ex: Dupont", key="f_lastname")
            visitor_firstname = st.text_input("Prénom du visiteur *", placeholder="Ex: Jean", key="f_firstname")
            visitor_email = st.text_input("E-mail du visiteur *", placeholder="Ex: jean.dupont@email.com", key="f_email")
            company = st.text_input("Société *", placeholder="Ex: DDVH S.A.", key="f_company")
            
        with col_f2:
            # Champ texte libre pour le motif (conformément à vos instructions)
            reason = st.text_input("Motif de la visite *", placeholder="Ex: Réunion, Maintenance, Entretien...", key="f_reason")
            host = st.text_input("Personne visitée (Nom et prénom) *", placeholder="Ex: Yanis Talbi", key="f_host")
            visit_date = st.date_input("Date de visite *", date(2026, 7, 9), key="f_date")
            
            time_col1, time_col2 = st.columns(2)
            with time_col1:
                start_time = st.time_input("Heure de début d'accès *", time(9, 0), key="f_start")
            with time_col2:
                end_time = st.time_input("Heure de fin d'accès *", time(11, 0), key="f_end")

        comments = st.text_area("Observations additionnelles / Commentaires (Optionnel)", placeholder="Précisez ici les détails de la visite...", height=80, key="f_comments")
        
        st.markdown("<br>", unsafe_allow_html=True)
        rgpd = st.checkbox("Le visiteur accepte la charte informatique de Serval S.A.S et donne son consentement pour le traitement temporaire de ses données (RGPD). *", key="f_rgpd")
        
        st.markdown("<br><hr style='border: 1px solid #f1f5f9; margin-bottom: 20px;'>", unsafe_allow_html=True)
        
        btn_col1, btn_col2, btn_col3, _ = st.columns([1, 1, 1, 2.5])
        
        with btn_col1:
            valider_btn = st.button("Valider", use_container_width=True, key="btn_validate_req")
        with btn_col2:
            annuler_btn = st.button("Annuler (Vider)", use_container_width=True, key="btn_reset_req")
        with btn_col3:
            voir_tab_btn = st.button("Historique", use_container_width=True, key="btn_view_dashboard")

        # Action d'annulation
        if annuler_btn:
            st.session_state.form_reset_trigger = True
            st.rerun()

        # Navigation vers l'historique
        if voir_tab_btn:
            st.session_state.current_page = "Historique"
            st.rerun()

        # Action de validation
        if valider_btn:
            if not visitor_lastname or not visitor_firstname or not visitor_email or not company or not host or not reason:
                st.markdown('<div class="custom-error-banner"><i class="fa-solid fa-circle-exclamation"></i> Veuillez renseigner l\'ensemble des champs obligatoires marqués d\'un astérisque (*).</div>', unsafe_allow_html=True)
            elif not rgpd:
                st.markdown('<div class="custom-error-banner"><i class="fa-solid fa-circle-exclamation"></i> L\'acceptation de la charte de confidentialité RGPD est obligatoire pour valider la demande.</div>', unsafe_allow_html=True)
            else:
                # Calcul de la durée
                dt_start = datetime.combine(visit_date, start_time)
                dt_end = datetime.combine(visit_date, end_time)
                duration_hours = (dt_end - dt_start).total_seconds() / 3600.0
                
                if duration_hours <= 0:
                    st.markdown('<div class="custom-error-banner"><i class="fa-solid fa-circle-exclamation"></i> Erreur : L\'heure de fin d\'accès doit être après l\'heure de début d\'accès.</div>', unsafe_allow_html=True)
                elif duration_hours > 7.0:
                    st.markdown('<div class="custom-error-banner"><i class="fa-solid fa-circle-exclamation"></i> <b>Limitation DSI :</b> La durée calculée est de {:.1f} heures. Le système interdit d\'accorder une durée supérieure à 7 heures par visiteur.</div>'.format(duration_hours), unsafe_allow_html=True)
                else:
                    # Identifiants Wi-Fi sécurisés
                    wifi_user, wifi_pass = generate_wifi_credentials(
