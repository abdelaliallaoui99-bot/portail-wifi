import streamlit as st
import time
import random

# Configuration de la page
st.set_page_config(
    page_title="Serval S.A.S - Portail Wi-Fi Visiteurs",
    page_icon="📶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Style CSS épuré et charte officielle
st.markdown("""
<style>
    :root {
        --serval-green: #004737;
        --serval-orange: #e05326;
        --serval-light: #f4f7f6;
    }
    
    .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    
    /* En-tête Serval avec vrai logo recréé */
    .header-container {
        background-color: var(--serval-green);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border-bottom: 5px solid var(--serval-orange);
        display: flex;
        align-items: center;
        gap: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Logo officiel Serval dessiné en pur CSS */
    .logo-serval {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-width: 90px;
    }
    .logo-icon {
        position: relative;
        width: 40px;
        height: 45px;
    }
    .logo-curve-1 {
        position: absolute;
        width: 30px;
        height: 30px;
        border: 7px solid white;
        border-color: white transparent transparent white;
        border-radius: 50% 0 50% 50%;
        transform: rotate(-45deg);
        top: 0;
    }
    .logo-curve-2 {
        position: absolute;
        width: 30px;
        height: 30px;
        border: 7px solid white;
        border-color: transparent white white transparent;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        bottom: 0;
    }
    .logo-word {
        color: white;
        font-weight: bold;
        font-size: 1.3rem;
        font-family: sans-serif;
        margin-top: 0.2rem;
        letter-spacing: 0.5px;
    }
    
    .header-text-block {
        flex-grow: 1;
    }
    .header-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    .header-subtitle {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Blocs minimalistes */
    .content-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid var(--serval-green);
    }
    .content-title {
        color: var(--serval-green);
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Chiffres clés condensés */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    .stat-card {
        background: var(--serval-light);
        padding: 0.8rem;
        border-radius: 6px;
        text-align: center;
        border-bottom: 3px solid var(--serval-orange);
    }
    .stat-number {
        color: var(--serval-green);
        font-size: 1.3rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #475569;
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

if 'connected' not in st.session_state:
    st.session_state.connected = False
    st.session_state.role = None

# --- PAGE 1 : ACCUEIL & CONNEXION NETTOYÉE ---
if not st.session_state.connected:
    
    # En-tête avec le logo fidèle
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
            <div class="header-title">Serval S.A.S</div>
            <div class="header-subtitle">Portail de Gestion des Accès Wi-Fi Visiteurs</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Disposition équilibrée en 2 colonnes
    col_left, col_right = st.columns([1.3, 1.7], gap="large")
    
    with col_left:
        st.markdown('<div class="content-box" style="border-left-color:#e05326;">', unsafe_allow_html=True)
        st.markdown('<div class="content-title">🔑 Connexion Sécurisée</div>', unsafe_allow_html=True)
        
        identifiant = st.text_input("Identifiant", placeholder="accueil")
        mot_de_pass = st.text_input("Mot de passe", type="password", placeholder="••••••••")
        
        if st.button("Se connecter", use_container_width=True):
            if identifiant == "admin" and mot_de_pass == "accueil123":
                st.session_state.connected = True
                st.session_state.role = "Administrateur"
                st.rerun()
            elif identifiant == "accueil" and mot_de_pass == "accueil123":
                st.session_state.connected = True
                st.session_state.role = "Accueil"
                st.rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_right:
        st.markdown("""
        <div class="content-box">
            <div class="content-title">🌱 Serval, partenaire des éleveurs de demain</div>
            <p style="font-size: 0.9rem; margin-bottom: 0;">
            <b>Expert de la nutrition des jeunes animaux</b><br>
            Fabricant français d’aliment d’allaitement et de solutions nutritionnelles de haute qualité pour jeunes animaux depuis plus de 60 ans.
            </p>
        </div>
        
        <div class="content-box">
            <div class="content-title">🛡️ Traçabilité & Sécurité Informatique</div>
            <p style="font-size: 0.9rem; margin-bottom: 0;">
            Chaque ticket d'accès Wi-Fi généré est temporaire, tracé conformément aux réglementations, et transmis de manière éco-conçue directement par e-mail.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    # Chiffres clés déplacés et épurés tout en bas sur toute la largeur
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

# --- PAGE 2 : APPLICATION CONNECTÉE ---
else:
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.markdown(f"<h3 style='color:#004737; margin:0;'>🟢 Session active : {st.session_state.role} (Serval S.A.S)</h3>", unsafe_allow_html=True)
    with col_logout:
        if st.button("Se déconnecter", type="primary", use_container_width=True):
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
        email = st.text_input("Adresse E-mail du visiteur")

    if st.button("Confirmer et Générer le Ticket", type="primary"):
        if nom_visiteur and societe and email:
            with st.spinner("Génération..."):
                time.sleep(1)
            prefix = "".join(nom_visiteur.lower().split())[:4]
            wifi_id = f"serval_{prefix}{random.randint(10,99)}"
            wifi_key = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=8))
            
            st.success("Ticket créé avec succès !")
            st.markdown(f"""
            <div style="background-color: #ffffff; border: 2px dashed #004737; padding: 2rem; border-radius: 8px; max-width: 450px; margin: 1.5rem auto; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                <h3 style="text-align: center; color: #004737; margin-top: 0; letter-spacing:1px;">TICKET ACCÈS WI-FI</h3>
                <p style="text-align: center; color: #64748b;">-------------------------------------</p>
                <p style="margin:0.4rem 0;"><b>Visiteur :</b> {nom_visiteur}</p>
                <p style="margin:0.4rem 0;"><b>Société :</b> {societe}</p>
                <p style="margin:0.4rem 0;"><b>Horaires :</b> Validité {duree} heures</p>
                <div style="background-color: #f4f7f6; padding: 1rem; border-radius: 6px; margin: 1rem 0; border-left: 4px solid #e05326;">
                    <p style="margin: 0.2rem 0;"><b>ID Réseau :</b> <code style="color:#004737; font-size:1.1rem;">{wifi_id}</code></p>
                    <p style="margin: 0.2rem 0;"><b>Clé Wi-Fi :</b> <code style="color:#e05326; font-size:1.1rem;">{wifi_key}</code></p>
                </div>
                <p style="font-size: 0.85rem; color: #16a34a; text-align: center; font-style: italic; margin-bottom:0;">Simulation d'envoi complétée vers {email}.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Veuillez remplir tous les champs.")
