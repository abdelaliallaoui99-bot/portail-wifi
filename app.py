import streamlit as st
import random
import string
from datetime import datetime, time, timedelta

# Configuration de la page
st.set_page_config(
    page_title="Portail Wi-Fi Visiteurs Premium",
    page_icon="📶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS Premium personnalisé
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
        color: white; border: none; border-radius: 8px;
        padding: 0.6rem 1.5rem; font-weight: 600; width: 100%;
    }
    .stButton>button:hover { opacity: 0.9; color: white; }
    .card {
        background: white; padding: 2rem; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
        margin-bottom: 1.5rem; border: 1px solid #e2e8f0;
    }
    .header-band {
        background: linear-gradient(135deg, #1e1b4b 0%, #4f46e5 100%);
        color: white; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;
    }
    .ticket {
        background: #fff; border: 2px dashed #cbd5e1; padding: 2rem;
        border-radius: 8px; font-family: 'Courier New', Courier, monospace;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); max-width: 450px; margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de la base de données locale en mémoire
if 'db' not in st.session_state:
    st.session_state.db = {
        'users': {
            'admin': {'password': 'admin123', 'role': 'admin', 'name': 'Administrateur'},
            'accueil': {'password': 'accueil123', 'role': 'user', 'name': 'Accueil Réception'}
        },
        'requests': [],
        'current_request': None
    }

# Gestion de la déconnexion
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_name = None

# ÉCRAN DE CONNEXION
if not st.session_state.logged_in:
    st.markdown("<div class='header-band'><h1>📶 Portail Wi-Fi Visiteurs</h1><p>Veuillez vous connecter pour gérer les accès</p></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        username = st.text_input("Identifiant").strip()
        password = st.text_input("Mot de passe", type="password")
        
        # Aide intelligente pour l'orthographe d'accueil
        if "acceuil" in username.lower():
            st.warning("⚠️ Attention à l'orthographe : écrivez bien 'accueil' (le 'u' avant le 'e').")
            
        if st.button("Se connecter"):
            users = st.session_state.db['users']
            if username in users and users[username]['password'] == password:
                st.session_state.logged_in = True
                st.session_state.user_role = users[username]['role']
                st.session_state.user_name = users[username]['name']
                st.rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect.")
    with col2:
        st.markdown("""
        <div style="background-color: #f1f5f9; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #4f46e5;">
            <h4 style="margin-top:0;">💡 Comptes de Démonstration</h4>
            <ul>
                <li><b>Admin :</b> admin / admin123</li>
                <li><b>Accueil :</b> accueil / accueil123</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # BARRE LATÉRALE DE NAVIGATION
    with st.sidebar:
        st.markdown(f"### 🟢 Connecté : {st.session_state.user_name}")
        st.markdown("---")
        
        menu_options = ["Déclaration d'accès", "Récapitulatif & Ticket", "Tableau de bord"]
        if st.session_state.user_role == "admin":
            menu_options.append("Gestions des comptes")
            
        choice = st.radio("Navigation", menu_options)
        st.markdown("---")
        if st.button("Déconnexion"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.user_name = None
            st.rerun()

    # 1. FORMULAIRE DE DÉCLARATION
    if choice == "Déclaration d'accès":
        st.markdown("<div class='header-band'><h2>📝 Nouvelle Déclaration d'Accès</h2><p>Renseignez les informations du visiteur</p></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        with st.form("visitor_form"):
            c1, c2 = st.columns(2)
            with c1:
                nom = st.text_input("Nom du visiteur *")
                prenom = st.text_input("Prénom du visiteur *")
                email = st.text_input("E-mail du visiteur *")
            with c2:
                hote = st.text_input("Personne visitée / Hôte *")
                societe = st.text_input("Société / Organisation")
                motif = st.selectbox("Motif de la visite *", ["Réunion", "Maintenance", "Entretien", "Autre"])
            
            c3, c4 = st.columns(2)
            with c3:
                heure_debut = st.time_input("Heure de début", time(9, 0))
            with c4:
                heure_fin = st.time_input("Heure de fin", time(11, 0))
                
            rgpd = st.checkbox(" J'accepte les conditions de gestion des données personnelles (RGPD obligatoire) *")
            
            submit = st.form_submit_button("Calculer et vérifier la demande")
            
            if submit:
                if not (nom and prenom and email and hote and rgpd):
                    st.error("❌ Veuillez remplir tous les champs obligatoires et accepter le RGPD.")
                else:
                    # Calcul de la durée
                    t1 = datetime.combine(datetime.today(), heure_debut)
                    t2 = datetime.combine(datetime.today(), heure_fin)
                    duree = max(0.5, min(7.0, (t2 - t1).seconds / 3600))
                    
                    # Génération des codes simulés
                    wifi_user = f"wifi_{nom.lower()[:4]}{random.randint(10,99)}"
                    wifi_pass = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
                    
                    st.session_state.db['current_request'] = {
                        'nom': nom, 'prenom': prenom, 'email': email, 'hote': hote,
                        'societe': societe, 'motif': motif, 'debut': str(heure_debut)[:5],
                        'fin': str(heure_fin)[:5], 'duree': duree, 'wifi_user': wifi_user,
                        'wifi_pass': wifi_pass
                    }
                    st.success("✅ Demande prête ! Rendez-vous dans l'onglet 'Récapitulatif & Ticket' pour générer les accès.")
        st.markdown("</div>", unsafe_allow_html=True)

    # 2. RÉCAPITULATIF & TICKET
    elif choice == "Récapitulatif & Ticket":
        st.markdown("<div class='header-band'><h2>🎫 Récapitulatif & Ticket Wi-Fi</h2><p>Validez la demande et générez le ticket</p></div>", unsafe_allow_html=True)
        
        req = st.session_state.db['current_request']
        if not req:
            st.info("💡 Aucune demande en cours. Veuillez remplir le formulaire de déclaration d'accès d'abord.")
        else:
            col_left, col_right = st.columns([1, 1])
            with col_left:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("Résumé des données")
                st.write(f"**Visiteur :** {req['prenom']} {req['nom']}")
                st.write(f"**E-mail :** {req['email']}")
                st.write(f"**Hôte :** {req['hote']}")
                st.write(f"**Durée calculée :** {req['duree']} h (max 7 h)")
                
                if st.button("Confirmer et Générer le Ticket"):
                    # Sauvegarde définitive dans l'historique
                    st.session_state.db['requests'].append(req)
                    st.session_state.success_ticket = True
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col_right:
                if st.session_state.get('success_ticket', False):
                    st.markdown(f"""
                    <div class="ticket">
                        <h3 style="text-align:center; margin-top:0; color:#1e1b4b;">TICKET ACCÈS WI-FI</h3>
                        <p style="text-align:center; color:#64748b;">-------------------------</p>
                        <p><b>Visiteur :</b> {req['prenom'].upper()} {req['nom'].upper()}</p>
                        <p><b>Société :</b> {req['societe'] if req['societe'] else 'N/A'}</p>
                        <p><b>Valable le :</b> {datetime.today().strftime('%d/%m/%Y')}</p>
                        <p><b>Horaires :</b> {req['debut']} - {req['fin']} ({req['duree']}h)</p>
                        <p style="text-align:center; color:#64748b;">-------------------------</p>
                        <p style="font-size:1.1rem; text-align:center; background:#f1f5f9; padding:0.5rem; border-radius:4px;">
                            <b>ID :</b> <code style="color:#4f46e5;">{req['wifi_user']}</code><br>
                            <b>Clé :</b> <code style="color:#06b6d4;">{req['wifi_pass']}</code>
                        </p>
                        <p style="text-align:center; color:#64748b;">-------------------------</p>
                        <p style="font-size:0.75rem; text-align:center; color:#94a3b8;">Simulation d'envoi d'e-mail effectuée avec succès.</p>
                    </div>
                    """, unsafe_allow_html=True)

    # 3. TABLEAU DE BORD
    elif choice == "Tableau de bord":
        st.markdown("<div class='header-band'><h2>📊 Tableau de Bord des Accès</h2><p>Historique et suivi en temps réel de l'activité</p></div>", unsafe_allow_html=True)
        
        reqs = st.session_state.db['requests']
        
        # KPIs en haut
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.markdown(f"<div class='card' style='text-align:center;'><h3>Demandes du jour</h3><h1 style='color:#4f46e5;'>{len(reqs)}</h1></div>", unsafe_allow_html=True)
        with kpi2:
            total_hours = sum([r['duree'] for r in reqs])
            st.markdown(f"<div class='card' style='text-align:center;'><h3>Heures cumulées</h3><h1 style='color:#06b6d4;'>{total_hours} h</h1></div>", unsafe_allow_html=True)
        with kpi3:
            st.markdown(f"<div class='card' style='text-align:center;'><h3>Statut système</h3><h1 style='color:#10b981;'>Actif</h1></div>", unsafe_allow_html=True)
            
        # Table de données
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Historique complet des connexions")
        if not reqs:
            st.write("Aucun accès enregistré pour le moment.")
        else:
            import pandas as pd
            df = pd.DataFrame(reqs)[['nom', 'prenom', 'email', 'hote', 'debut', 'fin', 'duree', 'wifi_user']]
            df.columns = ['Nom', 'Prénom', 'E-mail', 'Hôte / Accompagnant', 'Début', 'Fin', 'Durée (h)', 'Identifiant Wi-Fi']
            st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 4. GESTION DES COMPTES (ADMIN ONLY)
    elif choice == "Gestions des comptes":
        st.markdown("<div class='header-band'><h2>⚙️ Gestion des Comptes Utilisateurs</h2><p>Réservé aux administrateurs du système</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Comptes actifs configurés")
        for u, data in st.session_state.db['users'].items():
            st.write(f"👤 **{data['name']}** — Identifiant : `{u}` | Rôle : `{data['role']}`")
        st.markdown("</div>", unsafe_allow_html=True)
