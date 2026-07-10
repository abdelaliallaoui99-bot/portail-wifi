import streamlit as st
import random
import string
import pandas as pd
import io
import json
import os
import hashlib
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, time, date, timedelta

# Configuration de la page pour une expérience premium responsive
st.set_page_config(
    page_title="Serval S.A.S - Portail Wi-Fi Visiteurs",
    page_icon="📶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SÉCURITÉ : HACHAGE DES MOTS DE PASSE ---
def hash_password(raw_password):
    """Retourne le hachage SHA-256 d'un mot de passe (aucun mot de passe en clair n'est stocké)."""
    return hashlib.sha256(raw_password.encode('utf-8')).hexdigest()

def is_hashed(value):
    """Détecte si une valeur ressemble déjà à un hachage SHA-256 (64 caractères hexadécimaux)."""
    return isinstance(value, str) and len(value) == 64 and all(c in string.hexdigits for c in value)

# --- PERSISTANCE DE LA BASE DE DONNÉES EN JSON ---
def load_persistent_db():
    """Charge la base de données depuis un fichier JSON local s'il existe."""
    default_db = {
        'users': {
            'admin': {'password': hash_password('admin123'), 'role': 'admin', 'firstname': 'Administrateur', 'lastname': '', 'email': 'admin@serval.fr', 'active': True},
            'accueil': {'password': hash_password('accueil123'), 'role': 'accueil', 'firstname': 'Accueil', 'lastname': '', 'email': 'accueil@serval.fr', 'active': True}
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
                'date': '2026-07-09',
                'start_time': '09:00:00',
                'end_time': '11:00:00',
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
                'date': '2026-07-08',
                'start_time': '14:00:00',
                'end_time': '18:00:00',
                'duration': 4.0,
                'rgpd': True,
                'comments': 'Maintenance annuelle du serveur principal.',
                'wifi_user': 'serval_sart12',
                'wifi_pass': 'T7pQ9v8B'
            }
        ],
        'emails_sent': []
    }
    
    if not os.path.exists('database.json'):
        return default_db
    try:
        with open('database.json', 'r', encoding='utf-8') as f:
            db = json.load(f)
        # Migration automatique : hachage des mots de passe historiques stockés en clair
        for uname, udata in db.get('users', {}).items():
            if not is_hashed(udata.get('password', '')):
                udata['password'] = hash_password(udata['password'])
        return db
    except Exception:
        return default_db

def save_persistent_db(db):
    """Sauvegarde de manière persistante la base de données en format JSON."""
    serializable_db = {
        'users': db['users'],
        'requests': [],
        'emails_sent': db['emails_sent']
    }
    # Conversion des types complexes date et time en chaînes de caractères
    for r in db['requests']:
        r_copy = r.copy()
        if isinstance(r_copy['date'], (date, datetime)):
            r_copy['date'] = r_copy['date'].strftime('%Y-%m-%d')
        if isinstance(r_copy['start_time'], time):
            r_copy['start_time'] = r_copy['start_time'].strftime('%H:%M:%S')
        if isinstance(r_copy['end_time'], time):
            r_copy['end_time'] = r_copy['end_time'].strftime('%H:%M:%S')
        serializable_db['requests'].append(r_copy)
        
    try:
        with open('database.json', 'w', encoding='utf-8') as f:
            json.dump(serializable_db, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Erreur d'écriture de la base de données : {e}")

def get_parsed_db():
    """Récupère la base de données avec conversion des chaînes en objets date et time."""
    db_raw = load_persistent_db()
    parsed_requests = []
    for r in db_raw['requests']:
        r_copy = r.copy()
        if isinstance(r_copy['date'], str):
            r_copy['date'] = datetime.strptime(r_copy['date'], '%Y-%m-%d').date()
        if isinstance(r_copy['start_time'], str):
            parts = r_copy['start_time'].split(':')
            r_copy['start_time'] = time(int(parts[0]), int(parts[1]))
        if isinstance(r_copy['end_time'], str):
            parts = r_copy['end_time'].split(':')
            r_copy['end_time'] = time(int(parts[0]), int(parts[1]))
        parsed_requests.append(r_copy)
    db_raw['requests'] = parsed_requests
    return db_raw

# Chargement de la base de données
if 'db' not in st.session_state:
    st.session_state.db = get_parsed_db()

# Variables d'état de session utilisateur
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
if 'last_email_status' not in st.session_state:
    st.session_state.last_email_status = None

# Variables de réinitialisation de formulaire
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
    .custom-badge-scheduled {
        background-color: #fef9c3;
        color: #a16207;
        padding: 4px 10px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }
    .custom-badge-revoked {
        background-color: #f1f5f9;
        color: #475569;
        padding: 4px 10px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
        text-decoration: line-through;
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

# --- FONCTIONS DE BASE ---
def check_login(username, password):
    """Vérifie l'exactitude des comptes conformément à la spécification."""
    users = st.session_state.db['users']
    if username in users:
        if users[username]['password'] == hash_password(password):
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

def get_visit_status(record):
    """Calcule le statut de validité de la session Wi-Fi (Programmé / En cours / Terminé / Révoqué)."""
    if record.get('revoked'):
        return "Révoqué"

    now = datetime.now()
    today = now.date()
    current_time = now.time()
    visit_date = record['date']
    start_time = record['start_time']
    end_time = record['end_time']

    if visit_date > today:
        return "Programmé"
    elif visit_date < today:
        return "Terminé"
    else:
        if current_time < start_time:
            return "Programmé"
        elif current_time > end_time:
            return "Terminé"
        else:
            return "En cours"

def send_email_smtp(to_address, subject, body):
    """
    Envoie un e-mail réel via SMTP si les identifiants sont configurés dans st.secrets.
    Configuration attendue dans .streamlit/secrets.toml :
        [smtp]
        server = "smtp.gmail.com"
        port = 587
        user = "votre_compte@gmail.com"
        password = "mot_de_passe_application"
        sender_name = "Serval S.A.S - Portail Wi-Fi"
    Si aucune configuration n'est présente, l'e-mail est simplement journalisé (mode simulation),
    ce qui permet de tester l'application sans compte SMTP.
    """
    if "smtp" not in st.secrets:
        return False, "simulation"
    try:
        cfg = st.secrets["smtp"]
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = f"{cfg.get('sender_name', 'Serval S.A.S')} <{cfg['user']}>"
        msg["To"] = to_address

        with smtplib.SMTP(cfg["server"], int(cfg.get("port", 587))) as server:
            server.starttls()
            server.login(cfg["user"], cfg["password"])
            server.sendmail(cfg["user"], [to_address], msg.as_string())
        return True, "envoyé"
    except Exception as e:
        return False, str(e)


def generate_wifi_credentials(lastname):
    """Génère de manière sécurisée des identifiants Wi-Fi uniques."""
    clean_name = "".join(x for x in lastname.lower() if x.isalnum())[:4]
    random_num = random.randint(10, 99)
    wifi_user = f"serval_{clean_name}{random_num}"
    characters = string.ascii_uppercase + string.digits
    wifi_pass = "".join(random.choice(characters) for _ in range(8))
    return wifi_user, wifi_pass

def render_visitors_table(visitors_list):
    """Génère une table HTML propre, robuste et élégante aux couleurs de Serval sans aucun espace en début de ligne."""
    if not visitors_list:
        return '<div style="padding: 20px; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; color: #64748b; text-align: center; font-style: italic;">Aucune connexion Wi-Fi enregistrée.</div>'
    
    rows_html = ""
    for r in visitors_list:
        status_calc = get_visit_status(r)
        badge_map = {
            'En cours': '<span class="custom-badge-active">🟢 En cours</span>',
            'Programmé': '<span class="custom-badge-scheduled">🕒 Programmé</span>',
            'Révoqué': '<span class="custom-badge-revoked">⛔ Révoqué</span>',
            'Terminé': '<span class="custom-badge-expired">⚪ Terminé</span>',
        }
        status_badge = badge_map.get(status_calc, badge_map['Terminé'])
        rows_html += f"""<tr style="border-bottom: 1px solid #e2e8f0; font-size: 13px;">
<td style="padding: 12px; font-weight: bold; color: #004737;">#{r['id']:03d}</td>
<td style="padding: 12px;"><b>{r['visitor_lastname'].upper()}</b> {r['visitor_firstname']}<br><span style="font-size:11px; color:#64748b;">{r['visitor_email']}</span></td>
<td style="padding: 12px;">{r['company']}</td>
<td style="padding: 12px;">{r['host']}</td>
<td style="padding: 12px;"><span style="background-color:#f4f7f6; padding:3px 8px; border-radius:4px; font-size:11px;">{r['reason']}</span></td>
<td style="padding: 12px;">Le {r['date'].strftime('%d/%m/%Y')}<br><span style="font-size:11px; font-weight:600; color:#e05326;">({r['duration']} h)</span></td>
<td style="padding: 12px; font-family: monospace; font-size:11px; color:#334155;">ID: {r['wifi_user']}<br>Clé: *********</td>
<td style="padding: 12px;">{status_badge}</td>
</tr>"""
    
    full_table = f"""<div style="overflow-x: auto; margin-top: 10px; margin-bottom: 25px;">
<table style="width: 100%; border-collapse: collapse; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; font-family: 'Plus Jakarta Sans', sans-serif;">
<thead>
<tr style="background-color: #f8fafc; border-bottom: 2px solid #e2e8f0; text-align: left; font-size: 13px;">
<th style="padding: 12px; font-weight: 700; color: #475569;">ID</th>
<th style="padding: 12px; font-weight: 700; color: #475569;">Visiteur</th>
<th style="padding: 12px; font-weight: 700; color: #475569;">Société</th>
<th style="padding: 12px; font-weight: 700; color: #475569;">Personne visitée</th>
<th style="padding: 12px; font-weight: 700; color: #475569;">Motif</th>
<th style="padding: 12px; font-weight: 700; color: #475569;">Date &amp; Durée</th>
<th style="padding: 12px; font-weight: 700; color: #475569;">Compte Wi-Fi</th>
<th style="padding: 12px; font-weight: 700; color: #475569;">Statut</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>
</div>"""
    
    # Nettoyage ultime et strict de l'indentation de chaque ligne pour empêcher Streamlit d'interpréter le code comme du texte brut
    clean_table = "\n".join([line.strip() for line in full_table.split("\n")])
    return clean_table


# ==========================================
# --- ÉCRAN 1 : CONNEXION (PAGE ACCUEIL) ---
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
    # En-tête de session dynamique
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

    # Barre de Navigation d'onglets réactifs (Page 3 d'origine supprimée, Navigation directe)
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
        else:
            st.write("")
    with nav_col4:
        if st.button("🚪 Se déconnecter", use_container_width=True, key="nav_logout"):
            logout()

    st.markdown("<br>", unsafe_allow_html=True)


    # ==========================================
    # --- PAGE 2 : FORMULAIRE DE DÉCLARATION ---
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
            # Champ texte libre pour le motif de visite (Saisie textuelle)
            reason = st.text_input("Motif de la visite *", placeholder="Ex: Réunion, Maintenance, Entretien...", key="f_reason")
            host = st.text_input("Personne visitée (Nom et prénom) *", placeholder="Ex: Yanis Talbi", key="f_host")
            # Modification de l'affichage de la date au format JJ/MM/AAAA pour la saisie
            visit_date = st.date_input("Date de visite *", date.today(), format="DD/MM/YYYY", key="f_date")
            
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
            st.session_state.last_generated_ticket = None
            st.rerun()

        # Navigation vers l'historique
        if voir_tab_btn:
            st.session_state.current_page = "Historique"
            st.session_state.last_generated_ticket = None
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
                    wifi_user, wifi_pass = generate_wifi_credentials(visitor_lastname)
                    
                    existing_ids = [r['id'] for r in st.session_state.db['requests']]
                    new_id = (max(existing_ids) + 1) if existing_ids else 1
                    final_record = {
                        'id': new_id,
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
                        'wifi_pass': wifi_pass,
                        'revoked': False,
                        'created_by': st.session_state.username
                    }
                    
                    # Enregistrement direct dans le registre
                    st.session_state.db['requests'].append(final_record)
                    save_persistent_db(st.session_state.db) # Sauvegarde définitive persistante en JSON !
                    
                    # E-mail automatique réglementaire contenant les identifiants Wi-Fi
                    email_body = f"""Bonjour {visitor_firstname},

Votre accès Wi-Fi visiteur chez Serval S.A.S a été activé.

Nom : {visitor_firstname} {visitor_lastname}
Société : {company}
Personne visitée : {host}
Motif : {reason}
Date de visite : {visit_date.strftime('%d/%m/%Y')}
Horaires d'accès : {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')} ({round(duration_hours, 1)} h)

Identifiants réseau Wi-Fi-Visiteurs :
Identifiant : {wifi_user}
Clé d'accès : {wifi_pass}

Cet accès est strictement temporaire et sera automatiquement désactivé à l'heure de fin indiquée
ci-dessus, conformément à la politique de sécurité informatique de Serval S.A.S. Merci de ne pas
partager ces identifiants.

Serval vous souhaite la bienvenue, bonne visite.

Cordialement,
Service informatique - Serval S.A.S
Sainte-Eanne, France"""

                    email_sent_ok, email_status = send_email_smtp(
                        visitor_email,
                        "🔑 Votre accès Wi-Fi Serval S.A.S",
                        email_body
                    )

                    st.session_state.db['emails_sent'].append({
                        'to': visitor_email,
                        'subject': "🔑 Votre accès Wifi Serval S.A.S",
                        'body': email_body,
                        'time': datetime.now().strftime('%H:%M:%S'),
                        'status': email_status
                    })
                    save_persistent_db(st.session_state.db)

                    # Fix de la syntaxe de stockage du ticket
                    st.session_state.last_generated_ticket = final_record
                    st.session_state.last_email_status = (email_sent_ok, email_status)
                    st.rerun()
                    
        # Affichage du ticket Wi-Fi premium si généré (directement sous le formulaire)
        if st.session_state.last_generated_ticket is not None:
            t = st.session_state.last_generated_ticket
            email_ok, email_status = st.session_state.last_email_status or (False, "simulation")
            if email_ok:
                email_note = "L'accès réseau est actif et l'e-mail contenant les identifiants a été envoyé au visiteur."
            elif email_status == "simulation":
                email_note = "L'accès réseau est actif. ⚠️ Aucun serveur SMTP n'est configuré : l'e-mail n'a pas été réellement envoyé (mode simulation, consultez st.secrets)."
            else:
                email_note = f"L'accès réseau est actif, mais l'envoi de l'e-mail a échoué ({email_status})."
            st.markdown(f'<div class="custom-success-banner"><i class="fa-solid fa-circle-check" style="font-size:22px;"></i> Activation réussie ! {email_note}</div>', unsafe_allow_html=True)
            
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
                            <span class="ticket-info-value">#00{t['id']}</span>
                        </div>
                        <div class="ticket-info-row">
                            <span class="ticket-info-label">Visiteur</span>
                            <span class="ticket-info-value">{t['visitor_firstname']} {t['visitor_lastname'].upper()}</span>
                        </div>
                        <div class="ticket-info-row">
                            <span class="ticket-info-label">Société</span>
                            <span class="ticket-info-value">{t['company']}</span>
                        </div>
                        <div class="ticket-info-row">
                            <span class="ticket-info-label">Validité</span>
                            <span class="ticket-info-value">Le {t['date'].strftime('%d/%m/%Y')}</span>
                        </div>
                        <div class="ticket-info-row">
                            <span class="ticket-info-label">Horaires</span>
                            <span class="ticket-info-value">{t['start_time'].strftime('%H:%M')} - {t['end_time'].strftime('%H:%M')} ({t['duration']}h)</span>
                        </div>
                        <div class="ticket-credentials-box">
                            <div class="creds-title">🔑 Identifiants Wi-Fi</div>
                            <div class="creds-user">ID : <span>{t['wifi_user']}</span></div>
                            <div class="creds-pass" style="color:#e05326;">Clé : <span>*********</span></div>
                        </div>
                        <div style="text-align: center; margin-top: 15px; font-size: 10px; color: #94a3b8; font-style: italic;">
                            Par mesure de sécurité, la clé Wi-Fi a été envoyée par mail à {t['visitor_email']}.
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


    # ==========================================
    # --- PAGE 3 : HISTORIQUE DES CONNEXIONS ---
    # ==========================================
    elif st.session_state.current_page == "Historique":
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="margin-top:0;"><i class="fa-solid fa-clock-rotate-left"></i> Historique des connexions</h2>', unsafe_allow_html=True)
        st.write("Consultez et suivez la traçabilité des accès réseau.")
        st.markdown("<br>", unsafe_allow_html=True)

        # Rechargement à jour pour garantir l'affichage sans perte
        st.session_state.db = get_parsed_db()
        requests_list = st.session_state.db['requests']
        today_date = date.today()

        # Séparation de l'historique en deux listes distinctes
        today_visitors = [r for r in requests_list if r['date'] == today_date]
        past_visitors = [r for r in requests_list if r['date'] < today_date]
        future_visitors = [r for r in requests_list if r['date'] > today_date]
        other_visitors = past_visitors + future_visitors

        # Outils de recherche de l'administrateur
        if st.session_state.user_role == 'admin':
            st.markdown("<h4>🔍 Outils de recherche de l'administrateur</h4>", unsafe_allow_html=True)
            col_search1, col_search2 = st.columns(2)
            with col_search1:
                search_name = st.text_input("Filtrer par nom / prénom / société...", "").lower()
            with col_search2:
                search_host = st.text_input("Filtrer par personne visitée...", "").lower()

            # Application des filtres si requis
            if search_name:
                today_visitors = [r for r in today_visitors if search_name in r['visitor_lastname'].lower() or search_name in r['visitor_firstname'].lower() or search_name in r['company'].lower()]
                other_visitors = [r for r in other_visitors if search_name in r['visitor_lastname'].lower() or search_name in r['visitor_firstname'].lower() or search_name in r['company'].lower()]
            if search_host:
                today_visitors = [r for r in today_visitors if search_host in r['host'].lower()]
                other_visitors = [r for r in other_visitors if search_host in r['host'].lower()]

            # Exportation CSV conforme
            st.markdown("<br>", unsafe_allow_html=True)
            col_exp, _ = st.columns([1.2, 2.8])
            with col_exp:
                if requests_list:
                    df = pd.DataFrame(requests_list)
                    # Masquage de la clé dans l'export pour conformité DSI
                    if 'wifi_pass' in df.columns:
                        df['wifi_pass'] = "*********"
                    csv_io = io.StringIO()
                    df.to_csv(csv_io, index=False, sep=';', encoding='utf-8')
                    st.download_button(
                        label="📥 Exporter en CSV",
                        data=csv_io.getvalue(),
                        file_name=f"export_wifi_visiteurs_{datetime.now().strftime('%d_%m_%Y')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key="btn_csv_export"
                    )
            # Révocation anticipée d'un accès actif (sécurité DSI)
            revocable = [r for r in requests_list if not r.get('revoked') and get_visit_status(r) in ('En cours', 'Programmé')]
            if revocable:
                st.markdown("<h4>⛔ Révoquer un accès Wi-Fi avant son terme</h4>", unsafe_allow_html=True)
                rev_options = {f"#{r['id']:03d} — {r['visitor_firstname']} {r['visitor_lastname'].upper()} ({r['company']})": r['id'] for r in revocable}
                col_rev1, col_rev2 = st.columns([3, 1])
                with col_rev1:
                    rev_choice = st.selectbox("Sélectionner une session active", list(rev_options.keys()), key="rev_select")
                with col_rev2:
                    st.write("")
                    st.write("")
                    if st.button("Révoquer l'accès", use_container_width=True, key="btn_revoke"):
                        target_id = rev_options[rev_choice]
                        for r in st.session_state.db['requests']:
                            if r['id'] == target_id:
                                r['revoked'] = True
                        save_persistent_db(st.session_state.db)
                        st.success(f"L'accès #{target_id:03d} a été révoqué immédiatement.")
                        st.rerun()

            st.markdown("<hr style='border:1px solid #f1f5f9; margin: 20px 0;'>", unsafe_allow_html=True)

        # Section 1 : Connexions du jour
        st.markdown("<h3>📅 Connexions de ce jour (Aujourd\'hui)</h3>", unsafe_allow_html=True)
        # render_visitors_table applique maintenant le strip-line strict pour qu'il soit rendu à 100% comme tableau HTML et non comme code textuel
        st.markdown(render_visitors_table(today_visitors), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Section 2 : Connexions précédentes
        st.markdown("<h3>📅 Connexions précédentes (Historique)</h3>", unsafe_allow_html=True)
        st.markdown(render_visitors_table(other_visitors), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


    # ==========================================
    # --- ÉCRAN 5 : GESTION DES COMPTES (ADMIN) ---
    # ==========================================
    elif st.session_state.current_page == "Gestion des comptes" and st.session_state.user_role == 'admin':
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        # Modification stricte : Suppression du mot "Écran 5" du titre de l'onglet
        st.markdown('<h2 style="margin-top:0;"><i class="fa-solid fa-users-gear"></i> Gestion des comptes</h2>', unsafe_allow_html=True)
        st.write("Gérez les habilitations et les accès des agents d'accueil et des administrateurs du portail.")
        st.markdown("<br>", unsafe_allow_html=True)

        # 1. Création de compte
        st.markdown("<h4>➕ Créer un nouveau compte utilisateur</h4>", unsafe_allow_html=True)
        c_col1, c_col2, c_col3 = st.columns(3)
        with c_col1:
            new_id = st.text_input("Identifiant *", placeholder="Ex: martin_a")
            new_email = st.text_input("E-mail", placeholder="Ex: a.martin@serval.fr")
        with c_col2:
            new_pwd = st.text_input("Mot de passe *", type="password", placeholder="••••••••")
            new_role = st.selectbox("Rôle du compte *", ["accueil", "admin"])
        with c_col3:
            new_first = st.text_input("Prénom *", placeholder="Ex: Albert")
            new_last = st.text_input("Nom *", placeholder="Ex: Martin")

        if st.button("Créer le compte utilisateur", use_container_width=True):
            if not new_id or not new_pwd or not new_first or not new_last:
                st.error("Les champs marqués d'un astérisque (*) sont obligatoires.")
            elif new_id in st.session_state.db['users']:
                st.error("Cet identifiant est déjà utilisé par un autre utilisateur.")
            elif len(new_pwd) < 6:
                st.error("Le mot de passe doit contenir au moins 6 caractères.")
            else:
                st.session_state.db['users'][new_id] = {
                    'password': hash_password(new_pwd),
                    'role': new_role,
                    'firstname': new_first,
                    'lastname': new_last,
                    'email': new_email,
                    'active': True
                }
                save_persistent_db(st.session_state.db)
                st.success(f"Le compte utilisateur '{new_id}' a été créé avec succès !")
                st.rerun()

        st.markdown("<hr style='border:1px solid #f1f5f9; margin: 30px 0;'>", unsafe_allow_html=True)

        # 2. Liste des comptes et modifications interactives
        st.markdown("<h4>📋 Comptes utilisateurs enregistrés</h4>", unsafe_allow_html=True)

        users_db = st.session_state.db['users']

        for username, data in list(users_db.items()):
            col_info, col_role, col_pwd, col_action = st.columns([2, 1.3, 2, 1.2])
            with col_info:
                st.markdown(f"👤 **{data['firstname']} {data['lastname']}** (`{username}`)")
                st.markdown(f"<small style='color:#64748b;'>{data.get('email', '—')}</small>", unsafe_allow_html=True)
            with col_role:
                if username == st.session_state.username:
                    role_label = "🔥 ADMINISTRATEUR" if data['role'] == 'admin' else "📋 ACCUEIL / SÉCURITÉ"
                    st.markdown(f"<small style='color: #4f46e5; font-weight:bold;'>{role_label}</small>", unsafe_allow_html=True)
                    st.caption("Actif")
                else:
                    role_index = 0 if data['role'] == 'accueil' else 1
                    new_role_val = st.selectbox("Rôle", ["accueil", "admin"], index=role_index, key=f"role_{username}", label_visibility="collapsed")
                    if new_role_val != data['role']:
                        st.session_state.db['users'][username]['role'] = new_role_val
                        save_persistent_db(st.session_state.db)
                        st.toast(f"Rôle de '{username}' mis à jour !")
                        st.rerun()
                    active_val = st.checkbox("Compte actif", value=data.get('active', True), key=f"active_{username}")
                    if active_val != data.get('active', True):
                        st.session_state.db['users'][username]['active'] = active_val
                        save_persistent_db(st.session_state.db)
                        st.toast(f"Statut de '{username}' mis à jour !")
                        st.rerun()
            with col_pwd:
                temp_new_pwd = st.text_input("Nouveau mot de passe", value="", type="password", placeholder="Laisser vide pour ne pas changer", key=f"pwd_field_{username}")
                if temp_new_pwd:
                    if len(temp_new_pwd) < 6:
                        st.caption(":red[Min. 6 caractères]")
                    else:
                        st.session_state.db['users'][username]['password'] = hash_password(temp_new_pwd)
                        save_persistent_db(st.session_state.db)
                        st.toast(f"Mot de passe de '{username}' mis à jour !")
            with col_action:
                if username == st.session_state.username:
                    st.markdown("<span style='color: #94a3b8; font-size:12px; font-style:italic;'>Session active</span>", unsafe_allow_html=True)
                else:
                    if st.button("🗑️ Supprimer", key=f"del_{username}", use_container_width=True):
                        del st.session_state.db['users'][username]
                        save_persistent_db(st.session_state.db)
                        st.success(f"Compte '{username}' supprimé.")
                        st.rerun()
            st.markdown("<hr style='border:1px solid #f8fafc; margin: 10px 0;'>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
