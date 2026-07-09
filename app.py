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
if 'temp_request' not in st.session_state:
    st.session_state.temp_request = None
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
    .session-header {
        background-color: #f4f7f6;
        border-left: 5px solid #004737;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
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
            if username == "accueil" and password == "acceuil123":
                return "Mot de passe incorrect. Attention : c'est <strong>'accueil123'</strong> (le <em>'u'</em> s'écrit avant le <em>'e'</em> !)."
            return "Mot de passe incorrect."
    else:
        return f"Identifiant '{username}' inconnu."

def logout():
    """Déconnexion sécurisée de la session."""
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.temp_request = None
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
# --- MODE CONNECTÉ (PAGE 2, 3, 4 et 5) ---
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
        if st.button("📊 Tableau de bord", use_container_width=True, type="primary" if st.session_state.current_page == "Tableau de bord" else "secondary", key="nav_dash"):
            st.session_state.current_page = "Tableau de bord"
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
    # --- ÉCRAN 2 : FORMULAIRE DE DÉCLARATION ---
    # ==========================================
    if st.session_state.current_page == "Formulaire":
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="margin-top:0;"><i class="fa-solid fa-file-signature"></i> Écran 2 - Formulaire de déclaration</h2>', unsafe_allow_html=True)
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
            st.session_state.f_reason = "Réunion"
            st.session_state.f_comments = ""
            st.session_state.f_rgpd = False

        col_f1, col_f2 = st.columns(2, gap="large")
        
        with col_f1:
            visitor_lastname = st.text_input("Nom du visiteur *", placeholder="Ex: Dupont", key="f_lastname")
            visitor_firstname = st.text_input("Prénom du visiteur *", placeholder="Ex: Jean", key="f_firstname")
            visitor_email = st.text_input("E-mail du visiteur *", placeholder="Ex: jean.dupont@email.com", key="f_email")
            company = st.text_input("Société *", placeholder="Ex: DDVH S.A.", key="f_company")
            
        with col_f2:
            reason = st.selectbox("Motif de la visite *", ["Réunion", "Entretien", "Maintenance technique", "Prestation externe", "Autre motif"], key="f_reason")
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
            voir_tab_btn = st.button("Tableau de bord", use_container_width=True, key="btn_view_dashboard")

        # Action d'annulation
        if annuler_btn:
            st.session_state.form_reset_trigger = True
            st.rerun()

        # Navigation vers tableau de bord
        if voir_tab_btn:
            st.session_state.current_page = "Tableau de bord"
            st.rerun()

        # Action de validation
        if valider_btn:
            if not visitor_lastname or not visitor_firstname or not visitor_email or not company or not host:
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
                    wifi_user, wifi_pass = generate_wifi_credentials(visitor_lastname)
                    
                    st.session_state.temp_request = {
                        'visitor_lastname': visitor_lastname,
                        'visitor_firstname': visitor_firstname,
                        'visitor_email': visitor_email,
                        'company': company,
                        'host': host,
                        'reason': reason,
                        'date': visit_date,
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': round(duration_hours, 1),
                        'rgpd': True,
                        'comments': comments,
                        'wifi_user': wifi_user,
                        'wifi_pass': wifi_pass
                    }
                    st.session_state.current_page = "Récapitulatif"
                    st.rerun()
                    
        st.markdown('</div>', unsafe_allow_html=True)


    # ==========================================
    # --- ÉCRAN 3 : RÉCAPITULATIF & TICKET ---
    # ==========================================
    elif st.session_state.current_page == "Récapitulatif":
        if st.session_state.temp_request is None and st.session_state.last_generated_ticket is None:
            st.warning("Aucun récapitulatif disponible.")
        else:
            req = st.session_state.temp_request if st.session_state.temp_request else st.session_state.last_generated_ticket
            
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown('<h2 style="margin-top:0;"><i class="fa-solid fa-file-contract"></i> Écran 3 - Récapitulatif de la déclaration</h2>', unsafe_allow_html=True)
            st.write("Dossier validé et enregistré. L'e-mail de notification automatique a été envoyé au visiteur.")
            st.markdown("<br>", unsafe_allow_html=True)

            # Enregistrement final en base
            if st.session_state.temp_request is not None:
                new_id = len(st.session_state.db['requests']) + 1
                final_record = {
                    'id': new_id,
                    **req
                }
                st.session_state.db['requests'].append(final_record)
                
                # E-mail automatique réglementaire (PDF page 4)
                email_body = f"""Bonjour,

Votre accès Wifi a été activé.

Nom: {req['visitor_firstname']} {req['visitor_lastname']}
Société: {req['company']}
Motif: {req['reason']}
Heure début de la visite : {req['start_time'].strftime('%H:%M')}
Heure fin de la visite : {req['end_time'].strftime('%H:%M')}
Durée de la visite : {req['duration']} heure(s)

Serval vous souhaite la bienvenue, bonne visite.

Cordialement,

Service informatique"""
                
                st.session_state.db['emails_sent'].append({
                    'to': req['visitor_email'],
                    'subject': "🔑 Votre accès Wifi Serval S.A.S",
                    'body': email_body,
                    'time': datetime.now().strftime('%H:%M:%S')
                })
                
                st.session_state.last_generated_ticket = final_record
                st.session_state.temp_request = None
                st.rerun()

            st.markdown('<div class="custom-success-banner"><i class="fa-solid fa-circle-check" style="font-size:22px;"></i> Activation réussie ! L\'accès réseau est actif et le ticket a été transmis par e-mail.</div>', unsafe_allow_html=True)

            col_details, col_ticket = st.columns([1.2, 1], gap="large")
            
            with col_details:
                st.markdown("<h4>📋 Récapitulatif des informations</h4>", unsafe_allow_html=True)
                st.markdown(f"""
                <table style="width: 100%; border-collapse: collapse; margin-top: 15px; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden;">
                    <tr style="border-bottom: 1px solid #e2e8f0; background:#f8fafc;"><td style="padding: 12px 18px; font-weight: 600; color: #475569;">Nom Complet</td><td style="padding: 12px 18px; font-weight: bold; color: #004737;">{req['visitor_lastname'].upper()} {req['visitor_firstname']}</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 12px 18px; font-weight: 600; color: #475569;">E-mail</td><td style="padding: 12px 18px; color: #334155;">{req['visitor_email']}</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 12px 18px; font-weight: 600; color: #475569;">Société</td><td style="padding: 12px 18px; color: #334155;">{req['company']}</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 12px 18px; font-weight: 600; color: #475569;">Motif</td><td style="padding: 12px 18px; color: #334155;">{req['reason']}</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 12px 18px; font-weight: 600; color: #475569;">Collaborateur visité</td><td style="padding: 12px 18px; color: #334155;">{req['host']}</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 12px 18px; font-weight: 600; color: #475569;">Date &amp; Heures</td><td style="padding: 12px 18px; color: #334155;">Le {req['date'].strftime('%d/%m/%Y')} (de {req['start_time'].strftime('%H:%M')} à {req['end_time'].strftime('%H:%M')})</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 12px 18px; font-weight: 600; color: #475569;">Durée de session</td><td style="padding: 12px 18px; color: #e05326; font-weight: bold;">{req['duration']} heure(s) (Max 7h)</td></tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;"><td style="padding: 12px 18px; font-weight: 600; color: #475569;">Habilitation RGPD</td><td style="padding: 12px 18px; color: #16a34a; font-weight: bold;">✅ Validée et conservée</td></tr>
                </table>
                """, unsafe_allow_html=True)
                
                st.markdown("<br><h4>✉️ Copie de la notification envoyée</h4>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 20px; border-radius: 10px; font-family: monospace; white-space: pre-wrap; font-size:12px; color:#1e293b;">
<b>De:</b> informatique@serval.fr<br><b>À:</b> {req['visitor_email']}<br><b>Sujet:</b> 🔑 Votre accès Wifi Serval S.A.S<br>---<br>Bonjour,

Votre accès Wifi a été activé.

Nom: {req['visitor_firstname']} {req['visitor_lastname']}
Société: {req['company']}
Motif: {req['reason']}
Heure début de la visite : {req['start_time'].strftime('%H:%M')}
Heure fin de la visite : {req['end_time'].strftime('%H:%M')}
Durée de la visite : {req['duration']} heure(s)

Serval vous souhaite la bienvenue, bonne visite.

Cordialement,
Service informatique
                </div>
                """, unsafe_allow_html=True)

            with col_ticket:
                st.markdown("<h4>📶 Ticket d'Accès d'Origine</h4>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="ticket-wrapper">
                    <div class="wifi-ticket-card">
                        <div class="ticket-top">
                            <h3>📶 TICKET WI-FI SERVAL</h3>
                            <p>Réseau : Wi-Fi-Visiteurs</p>
                        </div>
                        <div class="ticket-bottom">
                            <div class="ticket-info-row">
                                <span class="ticket-info-label">ID Session</span>
                                <span class="ticket-info-value">#00{req['id'] if 'id' in req else 'NEW'}</span>
                            </div>
                            <div class="ticket-info-row">
                                <span class="ticket-info-label">Visiteur</span>
                                <span class="ticket-info-value">{req['visitor_firstname']} {req['visitor_lastname'].upper()}</span>
                            </div>
                            <div class="ticket-info-row">
                                <span class="ticket-info-label">Société</span>
                                <span class="ticket-info-value">{req['company']}</span>
                            </div>
                            <div class="ticket-info-row">
                                <span class="ticket-info-label">Validité</span>
                                <span class="ticket-info-value">Le {req['date'].strftime('%d/%m/%Y')}</span>
                            </div>
                            <div class="ticket-info-row">
                                <span class="ticket-info-label">Horaires</span>
                                <span class="ticket-info-value">{req['start_time'].strftime('%H:%M')} - {req['end_time'].strftime('%H:%M')} ({req['duration']}h)</span>
                            </div>
                            <div class="ticket-credentials-box">
                                <div class="creds-title">🔑 Identifiants Wi-Fi</div>
                                <div class="creds-user">ID : <span>{req['wifi_user']}</span></div>
                                <div class="creds-pass">Clé : <span>{req['wifi_pass']}</span></div>
                            </div>
                            <div style="text-align: center; margin-top: 15px; font-size: 10px; color: #94a3b8; font-style: italic;">
                                Ce ticket d'accès est temporaire, nominal et soumis à archivage.
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br><hr style='border: 1px solid #f1f5f9; margin-bottom: 20px;'>", unsafe_allow_html=True)
            if st.button("Aller au Tableau de bord", type="primary", use_container_width=True, key="btn_go_to_board"):
                st.session_state.current_page = "Tableau de bord"
                st.session_state.last_generated_ticket = None
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)


    # ==========================================
    # --- ÉCRAN 4 : TABLEAU DE BORD (DOUBLE VUE) ---
    # ==========================================
    elif st.session_state.current_page == "Tableau de bord":
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="margin-top:0;"><i class="fa-solid fa-chart-line"></i> Écran 4 - Tableau de bord</h2>', unsafe_allow_html=True)
        st.write("Consultez, filtrez et exportez l'ensemble des déclarations d'accès Wi-Fi.")
        st.markdown("<br>", unsafe_allow_html=True)

        requests_list = st.session_state.db['requests']
        today_date = date(2026, 7, 9) # Date fixe de simulation réglementaire

        # -----------------------------
        # VUE HÔTE D'ACCUEIL (Simulée)
        # -----------------------------
        if st.session_state.user_role == 'accueil':
            st.markdown("<h3>📊 Vue Accueil (Visiteurs du jour uniquement)</h3>", unsafe_allow_html=True)
            
            # Filtre strict sur le jour même (9 Juillet 2026)
            today_visitors = [r for r in requests_list if r['date'] == today_date]
            
            col_actions_acc, _ = st.columns([1.2, 3])
            with col_actions_acc:
                if st.button("➕ Nouveau visiteur", use_container_width=True, key="acc_new_vis"):
                    st.session_state.current_page = "Formulaire"
                    st.rerun()
            
            if not today_visitors:
                st.info("Aucun visiteur n'est enregistré pour aujourd'hui.")
            else:
                table_header = """
                <table style="width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
                    <thead>
                        <tr style="background-color: #f8fafc; border-bottom: 2px solid #e2e8f0; text-align: left;">
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Nom</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Prénom</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Société</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Personne visitée</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Motif</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Heure début</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Heure fin</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Durée</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                table_rows = ""
                for r in today_visitors:
                    table_rows += f"""
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px; font-weight: 600; color: #004737;">{r['visitor_lastname'].upper()}</td>
                        <td style="padding: 12px;">{r['visitor_firstname']}</td>
                        <td style="padding: 12px;">{r['company']}</td>
                        <td style="padding: 12px;">{r['host']}</td>
                        <td style="padding: 12px;"><span style="background-color:#f4f7f6; padding:3px 8px; border-radius:4px; font-size:12px;">{r['reason']}</span></td>
                        <td style="padding: 12px; font-family:monospace;">{r['start_time'].strftime('%H:%M')}</td>
                        <td style="padding: 12px; font-family:monospace;">{r['end_time'].strftime('%H:%M')}</td>
                        <td style="padding: 12px; font-weight: bold; color: #e05326;">{r['duration']} h</td>
                    </tr>
                    """
                st.markdown(table_header + table_rows + "</tbody></table>", unsafe_allow_html=True)

        # -----------------------------
        # VUE ADMINISTRATEUR (Historique + Filtres)
        # -----------------------------
        else:
            st.markdown("<h3>🛠️ Vue Administrateur (Historique complet &amp; Filtres)</h3>", unsafe_allow_html=True)
            
            # Formulaire de filtrage multi-critères
            col_search1, col_search2, col_search3 = st.columns(3)
            with col_search1:
                search_lastname = st.text_input("🔍 Filtrer par nom ou prénom du visiteur...", "").lower()
            with col_search2:
                search_host = st.text_input("🔍 Filtrer par personne visitée...", "").lower()
            with col_search3:
                search_status = st.selectbox("🚦 Filtrer par statut...", ["Tous", "En cours", "Terminé"])

            # Application dynamique des filtres de recherche
            filtered_requests = []
            for r in requests_list:
                status_calc = get_visit_status(r['date'], r['start_time'], r['end_time'])
                
                # Validation critères
                match_lastname = search_lastname in r['visitor_lastname'].lower() or search_lastname in r['visitor_firstname'].lower()
                match_host = search_host in r['host'].lower()
                match_status = search_status == "Tous" or search_status == status_calc
                
                if match_lastname and match_host and match_status:
                    r_copy = r.copy()
                    r_copy['status'] = status_calc
                    filtered_requests.append(r_copy)

            # Ligne d'actions pour administrateur
            col_act1, col_act2, _ = st.columns([1.2, 1.2, 2.5])
            with col_act1:
                if st.button("➕ Nouveau visiteur", use_container_width=True, key="admin_add_vis_btn"):
                    st.session_state.current_page = "Formulaire"
                    st.rerun()
            with col_act2:
                # Export CSV conforme
                if filtered_requests:
                    df = pd.DataFrame(filtered_requests)
                    # Nettoyage des mots de passe pour des raisons de conformité
                    if 'wifi_pass' in df.columns:
                        df = df.drop(columns=['wifi_pass'])
                    csv_io = io.StringIO()
                    df.to_csv(csv_io, index=False, sep=';', encoding='utf-8')
                    st.download_button(
                        label="📥 Exporter en CSV",
                        data=csv_io.getvalue(),
                        file_name=f"export_wifi_visiteurs_{datetime.now().strftime('%d_%m_%Y')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key="btn_download_csv"
                    )

            if not filtered_requests:
                st.info("Aucune déclaration d'accès ne correspond à vos critères de recherche.")
            else:
                table_header = """
                <table style="width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
                    <thead>
                        <tr style="background-color: #f8fafc; border-bottom: 2px solid #e2e8f0; text-align: left;">
                            <th style="padding: 12px; font-weight: 700; color: #475569;">ID</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Visiteur</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Société</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Personne visitée</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Motif</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Date & Durée</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Compte Wi-Fi</th>
                            <th style="padding: 12px; font-weight: 700; color: #475569;">Statut</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                table_rows = ""
                for r in filtered_requests:
                    status_badge = (
                        '<span class="custom-badge-active">En cours</span>' 
                        if r['status'] == 'En cours' 
                        else '<span class="custom-badge-expired">Terminé</span>'
                    )
                    table_rows += f"""
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px; font-weight: bold; color: #004737;">#00{r['id']}</td>
                        <td style="padding: 12px;"><b>{r['visitor_lastname'].upper()}</b> {r['visitor_firstname']}<br><span style="font-size:11px; color:#64748b;">{r['visitor_email']}</span></td>
                        <td style="padding: 12px;">{r['company']}</td>
                        <td style="padding: 12px;">{r['host']}</td>
                        <td style="padding: 12px;"><span style="background-color:#f4f7f6; padding:3px 8px; border-radius:4px; font-size:12px;">{r['reason']}</span></td>
                        <td style="padding: 12px;">Le {r['date'].strftime('%d/%m/%Y')}<br><span style="font-size:11px; font-weight:600; color:#e05326;">({r['duration']} heure(s))</span></td>
                        <td style="padding: 12px; font-family: monospace; font-size:11px; background:#fafafa;">Utilisateur : {r['wifi_user']}</td>
                        <td style="padding: 12px;">{status_badge}</td>
                    </tr>
                    """
                st.markdown(table_header + table_rows + "</tbody></table>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


    # ==========================================
    # --- ÉCRAN 5 : GESTION DES COMPTES (ADMIN) ---
    # ==========================================
    elif st.session_state.current_page == "Gestion des comptes" and st.session_state.user_role == 'admin':
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="margin-top:0;"><i class="fa-solid fa-users-gear"></i> Écran 5 - Gestion des comptes</h2>', unsafe_allow_html=True)
        st.write("Gérez les habilitations et les accès des agents d'accueil et des administrateurs du portail.")
        st.markdown("<br>", unsafe_allow_html=True)

        # 1. Création de compte
        st.markdown("<h4>➕ Créer un nouveau compte utilisateur</h4>", unsafe_allow_html=True)
        c_col1, c_col2, c_col3, c_col4 = st.columns(4)
        with c_col1:
            new_id = st.text_input("Identifiant *", placeholder="Ex: martin_a")
        with c_col2:
            new_pwd = st.text_input("Mot de passe *", type="password", placeholder="••••••••")
        with c_col3:
            new_role = st.selectbox("Rôle du compte *", ["accueil", "admin"])
        with c_col4:
            new_first = st.text_input("Prénom", placeholder="Ex: Albert")
            new_last = st.text_input("Nom", placeholder="Ex: Martin")

        if st.button("Créer le compte utilisateur", use_container_width=True):
            if not new_id or not new_pwd or not new_first or not new_last:
                st.error("Les champs marqués d'un astérisque (*) sont obligatoires.")
            elif new_id in st.session_state.db['users']:
                st.error("Cet identifiant est déjà utilisé par un autre utilisateur.")
            else:
                st.session_state.db['users'][new_id] = {
                    'password': new_pwd,
                    'role': new_role,
                    'firstname': new_first,
                    'lastname': new_last,
                    'active': True
                }
                st.success(f"Le compte utilisateur '{new_id}' a été créé avec succès !")
                st.rerun()

        st.markdown("<hr style='border:1px solid #f1f5f9; margin: 30px 0;'>", unsafe_allow_html=True)

        # 2. Liste des comptes et modifications interactives
        st.markdown("<h4>📋 Comptes utilisateurs enregistrés</h4>", unsafe_allow_html=True)
        
        users_db = st.session_state.db['users']
        
        for username, data in list(users_db.items()):
            col_info, col_pwd, col_action = st.columns([2, 2, 1])
            with col_info:
                st.markdown(f"👤 **{data['firstname']} {data['lastname']}** (`{username}`)")
                role_label = "🔥 ADMINISTRATEUR" if data['role'] == 'admin' else "📋 ACCUEIL / SÉCURITÉ"
                st.markdown(f"<small style='color: #4f46e5; font-weight:bold;'>{role_label}</small>", unsafe_allow_html=True)
            with col_pwd:
                temp_new_pwd = st.text_input(f"Modifier mot de passe", value=data['password'], type="password", key=f"pwd_field_{username}")
                if temp_new_pwd != data['password']:
                    st.session_state.db['users'][username]['password'] = temp_new_pwd
                    st.toast(f"Mot de passe de '{username}' mis à jour !")
            with col_action:
                if username == st.session_state.username:
                    st.markdown("<span style='color: #94a3b8; font-size:12px; font-style:italic;'>Session active</span>", unsafe_allow_html=True)
                else:
                    if st.button("🗑️ Supprimer", key=f"del_{username}", use_container_width=True):
                        del st.session_state.db['users'][username]
                        st.success(f"Compte '{username}' supprimé.")
                        st.rerun()
            st.markdown("<hr style='border:1px solid #f8fafc; margin: 10px 0;'>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
