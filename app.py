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

# Style CSS global unifié (Page 1 & Page 2)
st.markdown("""
<style>
    :root {
        --serval-green: #004737;
        --serval-orange: #e05326;
        --serval-light: #f4f7f6;
    }
    
    .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    
    /* En-tête Serval (Page 1) */
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
    
    /* En-tête de Session Active (Page 2) */
    .session-header {
        background-color: var(--serval-light);
        border-left: 5px solid var(--serval-green);
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
    
    /* Zone de Connexion Agrandie */
    .login-box {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        padding: 2.5rem 2rem;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        border-top: 4px solid var(--serval-orange);
        margin-top: 0.5rem;
    }
    
    /* Blocs d'information */
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
    }
    
    /* Chiffres clés */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-top: 1.5rem;
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
    
    /* Personnalisation des boutons Streamlit */
    div.stButton > button:first-child {
        background-color: var(--serval-orange);
        color: white;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #c24114;
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

if 'connected' not in st.session_state:
    st.session_state.connected = False
    st.session_state.role = None

# ==========================================
# --- PAGE 1 : ACCUEIL & CONNEXION SERVAL ---
# ==========================================
if not st.session_state.connected:
    
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
            <h2 style="margin:0; font-size:2rem; font-weight:700;">Serval S.A.S</h2>
            <div class="header-subtitle">Portail de Gestion des Accès Wi-Fi Visiteurs</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.4, 1.6], gap="large")
    
    with col_left:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h3 style="color:var(--serval-green); margin-top:0; margin-bottom:1.5rem;">🔑 Connexion Sécurisée</h3>', unsafe_allow_html=True)
        
        identifiant = st.text_input("Identifiant", placeholder="Ex: accueil")
        mot_de_pass = st.text_input("Mot de passe", type="password", placeholder="••••••••")
        
        st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)
        if st.button("Se connecter", use_container_width=True):
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
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_right:
        st.markdown("""
        <div class="content-box">
            <div class="content-title">🌱 Serval, partenaire des éleveurs de demain</div>
            <p style="font-size: 0.9rem; margin-bottom: 0; text-align: justify;">
            <b>Expert de la nutrition des jeunes animaux</b><br>
            Fabricant français d’aliment d’allaitement et de solutions nutritionnelles de haute qualité pour jeunes animaux depuis plus de 60 ans.
            </p>
        </div>
        
        <div class="content-box">
            <div class="content-title">🛡️ Traçabilité & Sécurité Informatique</div>
            <p style="font-size: 0.9rem; margin-bottom: 0; text-align: justify;">
            Chaque ticket d'accès Wi-Fi généré est temporaire, tracé conformément aux réglementations, et transmis de manière éco-conçue directement par e-mail.
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
# --- PAGE 2 : APPLICATION CONNECTÉE REスタイLE ---
# ==========================================
else:
    # Bandeau supérieur harmonisé
    st.markdown(f"""
    <div class="session-header">
        <h3 style="color:var(--serval-green); margin:0; font-weight:700;">🟢 Session active : {st.session_state.role} (Serval S.A.S)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton de déconnexion aligné à droite proprement
    col_space, col_logout = st.columns([4, 1])
    with col_logout:
        if st.button("Se déconnecter", use_container_width=True, key="logout_btn"):
            st.session_state.connected = False
            st.session_state.role = None
            st.rerun()
            
    st.markdown("<h2 style='color:var(--serval-green); font-weight:700; margin-top:0;'>📝 Générer un nouveau Ticket d'Accès Wi-Fi Visiteur</h2>", unsafe_allow_html=True)
    st.write("---")
    
    # Disposition exacte en deux colonnes comme sur tes captures d'écran
    col_f1, col_f2 = st.columns(2, gap="large")
    with col_f1:
        nom_visiteur = st.text_input("Nom & Prénom du Visiteur", placeholder="Ex: Jean Dupont")
        societe = st.text_input("Société / Organisme", placeholder="Ex: Entreprise XYZ")
    with col_f2:
        duree = st.slider("Durée de l'accès (en heures)", min_value=1.0, max_value=7.0, value=2.0, step=0.5)
        email = st.text_input("Adresse E-mail du visiteur (pour envoi automatique)", placeholder="exemple@domaine.com")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bouton de génération aux couleurs Serval
    if st.button("Confirmer et Générer le Ticket", key="submit_ticket"):
        if nom_visiteur and societe and email:
            with st.spinner("Génération du ticket sécurisé..."):
                time.sleep(1)
            prefix = "".join(nom_visiteur.lower().split())[:4]
            wifi_id = f"serval_{prefix}{random.randint(10,99)}"
            wifi_key = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=8))
            
            st.success("Ticket créé avec succès !")
            st.markdown(f"""
            <div style="background-color: #ffffff; border: 2px dashed var(--serval-green); padding: 2rem; border-radius: 8px; max-width: 480px; margin: 1.5rem auto; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                <h3 style="text-align: center; color: var(--serval-green); margin-top: 0; letter-spacing:1px; font-weight:700;">TICKET ACCÈS WI-FI SERVAL</h3>
                <p style="text-align: center; color: #64748b;">-------------------------------------</p>
                <p style="margin:0.4rem 0; color:#333;"><b>Visiteur :</b> {nom_visiteur}</p>
                <p style="margin:0.4rem 0; color:#333;"><b>Société :</b> {societe}</p>
                <p style="margin:0.4rem 0; color:#333;"><b>Horaires :</b> Validité {duree} heures</p>
                <div style="background-color: var(--serval-light); padding: 1rem; border-radius: 6px; margin: 1rem 0; border-left: 4px solid var(--serval-orange);">
                    <p style="margin: 0.2rem 0;"><b>ID Réseau :</b> <code style="color:var(--serval-green); font-size:1.1rem; font-weight:bold;">{wifi_id}</code></p>
                    <p style="margin: 0.2rem 0;"><b>Clé Wi-Fi :</b> <code style="color:var(--serval-orange); font-size:1.1rem; font-weight:bold;">{wifi_key}</code></p>
                </div>
                <p style="font-size: 0.85rem; color: #16a34a; text-align: center; font-style: italic; margin-bottom:0;">Simulation d'envoi complétée avec succès vers {email}.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Veuillez remplir tous les champs avant de valider.")
