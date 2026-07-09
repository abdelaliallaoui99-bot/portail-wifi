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

# Style CSS de la Page 1 (Serval) et de la Page 2 (Bleu d'origine)
st.markdown("""
<style>
    :root {
        --serval-green: #004737;
        --serval-orange: #e05326;
        --serval-light: #f4f7f6;
    }
    
    .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    
    /* Page 1 : En-tête Serval */
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
    
    /* Page 1 : Logo Serval */
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
    
    /* Page 1 : Zone de Connexion Agrandie */
    .login-box {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        padding: 2.5rem 2rem;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        border-top: 4px solid var(--serval-orange);
        margin-top: 0.5rem;
    }
    
    /* Page 1 : Blocs d'information */
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
    
    /* Page 1 : Chiffres clés */
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
    
    /* Page 2 : Bandeau Bleu d'origine */
    .blue-header {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
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
        if st.button("Se connecter", use_container_width=True, type="primary"):
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
# --- PAGE 2 : VERSION ORIGINALE EN BLEU ---
# ==========================================
else:
    # Ligne d'état supérieure
    col_status, col_btn = st.columns([4, 1])
    with col_status:
        st.write(f"Session active : {st.session_state.role}")
    with col_btn:
        if st.button("Se déconnecter", use_container_width=True):
            st.session_state.connected = False
            st.session_state.role = None
            st.rerun()
            
    # Grand bandeau bleu d'origine
    st.markdown("""
    <div class="blue-header">
        <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">📶 Portail Wi-Fi Visiteurs</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Veuillez vous connecter pour gérer les accès</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulaire d'origine strict
    nom_visiteur = st.text_input("Nom & Prénom du Visiteur")
    societe = st.text_input("Société")
    duree = st.slider("Valable pour (heures)", 1, 7, 2)
    email = st.text_input("Courriel du Visiteur")

    if st.button("Se connecter", key="btn_orig_submit"):
        if nom_visiteur and societe and email:
            prefix = "".join(nom_visiteur.lower().split())[:4]
            wifi_id = f"wifi_{prefix}{random.randint(10,99)}"
            wifi_key = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=8))
            
            st.markdown(f"""
            <div style="border: 2px dashed #cccccc; padding: 20px; border-radius: 10px; max-width: 500px; margin: 20px auto; font-family: monospace; background-color: #ffffff;">
                <h2 style="text-align: center; margin-top: 0; color: #333333;">TICKET ACCÈS WI-FI</h2>
                <p style="text-align: center; color: #666666;">-------------------------</p>
                <p style="color: #333333;"><b>Visiteur :</b> {nom_visiteur.upper()}</p>
                <p style="color: #333333;"><b>Société :</b> {societe}</p>
                <p style="color: #333333;"><b>Valable le :</b> {time.strftime('%d/%m/%Y')}</p>
                <p style="color: #333333;"><b>Horaires :</b> {time.strftime('%H:%M')} - {time.strftime('%H:%M', time.localtime(time.time() + duree*3600))} ({float(duree)}h)</p>
                <p style="text-align: center; color: #666666;">-------------------------</p>
                <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; margin: 20px 0;">
                    <p style="margin: 5px 0; font-size: 16px; color: #333333;"><b>ID :</b> <span style="background-color: #e0e2e6; padding: 2px 6px; border-radius: 3px;">{wifi_id}</span></p>
                    <p style="margin: 5px 0; font-size: 16px; color: #333333;"><b>Clé :</b> <span style="background-color: #e0e2e6; padding: 2px 6px; border-radius: 3px; color: #ff4b4b; font-weight: bold;">{wifi_key}</span></p>
                </div>
                <p style="text-align: center; color: #666666;">-------------------------</p>
                <p style="font-size: 12px; color: #666666; text-align: center; font-style: italic;">Simulation d'envoi d'e-mail effectuée avec succès.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Veuillez remplir tous les champs.")
