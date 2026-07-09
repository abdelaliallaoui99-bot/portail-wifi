import streamlit as st
import time
import random

# Configuration de la page
st.set_page_config(
    page_title="Serval - Portail Wi-Fi Visiteurs",
    page_icon="📶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Style CSS personnalisé basé sur la charte officielle de serval.fr
st.markdown("""
<style>
    /* Couleurs principales Serval */
    :root {
        --serval-green: #004737;
        --serval-orange: #e05326;
        --serval-light: #f4f7f6;
    }
    
    /* Nettoyage du style par défaut de Streamlit */
    .reportview-container { background: #ffffff; }
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    
    /* En-tête Serval */
    .header-container {
        background-color: var(--serval-green);
        color: white;
        padding: 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border-bottom: 5px solid var(--serval-orange);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Cartes d'information QSE */
    .qse-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid var(--serval-green);
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .qse-title {
        color: var(--serval-green);
        font-weight: bold;
        margin-top: 0;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Pied de page Eco-conçu */
    .serval-footer {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 4rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de la session pour la connexion
if 'connected' not in st.session_state:
    st.session_state.connected = False
    st.session_state.role = None

# --- PAGE 1 : ÉCRAN DE CONNEXION SERVAL ---
if not st.session_state.connected:
    
    # 1. Bannière En-tête
    st.markdown("""
    <div class="header-container">
        <div class="header-title">serval</div>
        <div class="header-subtitle">Portail de Gestion des Accès Wi-Fi Visiteurs & Partenaires</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Corps de la page en 2 colonnes pour bien remplir l'espace
    col1, col2 = st.columns([1.2, 1.8], gap="large")
    
    with col1:
        st.subheader("🔑 Espace Sécurisé")
        st.write("Veuillez vous authentifier pour accéder au panneau de configuration des tickets d'accès.")
        
        # Formulaire de connexion
        identifiant = st.text_input("Identifiant", placeholder="Ex: accueil")
        mot_de_pass = st.text_input("Mot de passe", type="password", placeholder="••••••••")
        
        if st.button("Se connecter", use_container_width=True):
            # Les comptes de démo fonctionnent toujours discrètement ici
            if identifiant == "admin" and mot_de_pass == "admin123":
                st.session_state.connected = True
                st.session_state.role = "Administrateur"
                st.rerun()
            elif identifiant == "accueil" and mot_de_pass == "accueil123":
                st.session_state.connected = True
                st.session_state.role = "Accueil"
                st.rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect.")
                
    with col2:
        st.subheader("📋 Consignes de Sécurité & Politique Réseau")
        
        st.markdown("""
        <div class="qse-card">
            <div class="qse-title">🛡️ Sécurité Informatique & Traçabilité</div>
            Conformément à la législation en vigueur, chaque accès visiteur généré est strictement nominal, 
            temporaire (limité à la durée de la visite) et fait l'objet d'un archivage automatique des journaux de connexion.
        </div>
        
        <div class="qse-card">
            <div class="qse-title">🌱 Engagement RSE & Éco-conception</div>
            Ce portail est optimisé pour consommer un minimum de ressources serveurs. L'envoi des tickets d'accès 
            est dématérialisé par e-mail afin de limiter l'impression papier inutile au sein de nos sites.
        </div>
        
        <div class="qse-card">
            <div class="qse-title">🤝 Serval, partenaire des éleveurs de demain</div>
            Besoin d'assistance technique ou d'un accès étendu pour un audit ? Contactez le service DSI 
            ou le responsable Sécurité/QSE du site de Sainte-Eanne.
        </div>
        """, unsafe_allow_html=True)

    # 3. Footer officiel
    st.markdown("""
    <div class="serval-footer">
        Mentions légales - Politique de confidentialité - © 2026 Serval S.A.S - 🍃 Site Internet éco-conçu
    </div>
    """, unsafe_allow_html=True)

# --- PAGE 2 : APPLICATION CONNECTÉE (GESTION DES TICKETS) ---
else:
    # Bouton de déconnexion en haut à droite
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.markdown(f"<h2 style='color:#004737;'>🟢 Session active : {st.session_state.role}</h2>", unsafe_allow_html=True)
    with col_logout:
        if st.button("Se déconnecter", type="primary"):
            st.session_state.connected = False
            st.session_state.role = None
            st.rerun()
            
    st.divider()
    
    st.subheader("📝 Générer un nouveau Ticket d'Accès Wi-Fi Visiteur")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        nom_visiteur = st.text_input("Nom & Prénom du Visiteur")
        societe = st.text_input("Société / Organisme")
    with col_f2:
        duree = st.slider("Durée de l'accès (en heures)", min_value=1.0, max_value=7.0, value=2.0, step=0.5)
        email = st.text_input("Adresse E-mail du visiteur (pour envoi automatique)")

    if st.button("Confirmer et Générer le Ticket", type="primary"):
        if nom_visiteur and societe and email:
            with st.spinner("Génération des identifiants sécurisés Serval..."):
                time.sleep(1.5)
                
            # Génération des codes
            prefix = "".join(nom_visiteur.lower().split())[:4]
            wifi_id = f"serval_{prefix}{random.randint(10,99)}"
            wifi_key = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=8))
            
            st.success("Ticket créé avec succès !")
            
            # Affichage du ticket final
            st.markdown(f"""
            <div style="background-color: #ffffff; border: 2px dashed #004737; padding: 2rem; border-radius: 8px; max-width: 500px; margin: 1.5rem auto; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                <h3 style="text-align: center; color: #004737; margin-top: 0; letter-spacing:1px;">TICKET ACCÈS WI-FI SERVAL</h3>
                <p style="text-align: center; color: #64748b;">-------------------------------------</p>
                <p><b>Visiteur :</b> {nom_visiteur}</p>
                <p><b>Société :</b> {societe}</p>
                <p><b>Horaires :</b> Validité {duree} heures</p>
                <div style="background-color: #f4f7f6; padding: 1rem; border-radius: 6px; margin: 1rem 0; border-left: 4px solid #e05326;">
                    <p style="margin: 0.2rem 0;"><b>ID Réseau :</b> <code style="color:#004737; font-size:1.1rem;">{wifi_id}</code></p>
                    <p style="margin: 0.2rem 0;"><b>Clé Wi-Fi :</b> <code style="color:#e05326; font-size:1.1rem;">{wifi_key}</code></p>
                </div>
                <p style="font-size: 0.85rem; color: #16a34a; text-align: center; font-style: italic;">Simulation d'envoi d'e-mail effectuée avec succès à {email}.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Veuillez remplir tous les champs du formulaire avant de valider.")
