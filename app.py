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

# Style CSS pour coller à la charte serval.fr
st.markdown("""
<style>
    :root {
        --serval-green: #004737;
        --serval-orange: #e05326;
        --serval-light: #f4f7f6;
    }
    
    .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    
    /* Bannière En-tête avec Logo intégré */
    .header-container {
        background-color: var(--serval-green);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border-bottom: 5px solid var(--serval-orange);
        display: flex;
        align-items: center;
        gap: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Logo Serval en CSS */
    .logo-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-width: 110px;
        height: 90px;
    }
    .logo-s {
        font-size: 2.5rem;
        font-weight: bold;
        line-height: 1;
        background: linear-gradient(180deg, #d32f2f 0%, #e05326 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Georgia', serif;
        transform: skewX(-10deg);
    }
    .logo-text {
        color: #004737;
        font-weight: bold;
        font-size: 1.1rem;
        font-family: sans-serif;
        margin-top: 0.2rem;
    }
    
    .header-text-block {
        flex-grow: 1;
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.3rem;
    }
    
    /* Blocs de contenu */
    .content-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    .content-title {
        color: var(--serval-green);
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--serval-light);
        padding-bottom: 0.5rem;
    }
    
    /* Chiffres clés */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    .stat-card {
        background: var(--serval-light);
        padding: 1rem;
        border-radius: 6px;
        text-align: center;
        border-top: 3px solid var(--serval-orange);
    }
    .stat-number {
        color: var(--serval-green);
        font-size: 1.5rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #475569;
    }
    
    .serval-footer {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

if 'connected' not in st.session_state:
    st.session_state.connected = False
    st.session_state.role = None

# --- PAGE 1 : ÉCRAN D'ACCUEIL & CONNEXION ---
if not st.session_state.connected:
    
    # En-tête avec Logo et Titre
    st.markdown("""
    <div class="header-container">
        <div class="logo-container">
            <div class="logo-s">S</div>
            <div class="logo-text">serval</div>
        </div>
        <div class="header-text-block">
            <div class="header-title">Serval S.A.S</div>
            <div class="header-subtitle">Portail de Gestion des Accès Wi-Fi Visiteurs & Partenaires</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Organisation en 3 colonnes pour enrichir le visuel
    col_left, col_mid, col_right = st.columns([1.1, 1.0, 0.9], gap="medium")
    
    with col_left:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.subheader("🔑 Connexion Sécurisée")
        st.write("Réservé au personnel de l'accueil et administrateurs.")
        
        identifiant = st.text_input("Identifiant", placeholder="Ex: accueil")
        mot_de_pass = st.text_input("Mot de passe", type="password", placeholder="••••••••")
        
        if st.button("Se connecter", use_container_width=True):
            if identifiant == "admin" and mot_de_pass == "accueil123": # Correction automatique de la faute
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
        
        # Section Actualités pour remplir le bas de la colonne de gauche
        st.markdown("""
        <div class="content-box">
            <div class="content-title">📢 Actualités Serval</div>
            <small style="color: #e05326;"><b>News - 4 juin 2026</b></small><br>
            <b>Salon de l'Agriculture</b><br>
            Retrouvez notre équipe aux Côtes d'Armor les 13 et 14 juin 2026.<br><br>
            <small style="color: #e05326;"><b>News - 1 avril 2026</b></small><br>
            <b>Servatec Excell</b><br>
            La nouvelle référence riche en protéines laitières pour un sevrage réussi.
        </div>
        """, unsafe_allow_html=True)
        
    with col_mid:
        st.markdown("""
        <div class="content-box">
            <div class="content-title">🌱 Serval, partenaire des éleveurs de demain</div>
            <p><b>Expert de la nutrition des jeunes animaux</b></p>
            <p style="font-size: 0.9rem; text-align: justify;">
            Serval S.A.S est un fabricant français d’aliment d’allaitement et de solutions nutritionnelles pour jeunes animaux depuis plus de 60 ans. 
            Grâce à notre expertise dans le choix des matières premières laitières (poudre de lait, lactosérum) et dans la réalité du terrain, 
            l’équipe vous propose un accompagnement adapté à chaque besoin (veaux laitiers, allaitants, agneaux, chevreaux, bufflons...).
            </p>
        </div>
        
        <div class="content-box">
            <div class="content-title">📊 Serval en un coup d'œil</div>
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-number">+ 100 M€</div>
                    <div class="stat-label">Chiffre d'affaires</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">+ 1M</div>
                    <div class="stat-label">Animaux nourris / an</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">4</div>
                    <div class="stat-label">Usines dans le monde</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">+ 100</div>
                    <div class="stat-label">Collaborateurs</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_right:
        st.markdown("""
        <div class="content-box">
            <div class="content-title">🥩 Notre Filière Viande</div>
            <p style="font-size: 0.9rem; text-align: justify;">
            En partenariat avec 150 éleveurs, le groupe produit plus de 50 000 veaux sélectionnés, nés, élevés et abattus en France 
            selon des cahiers des charges stricts respectant le bien-être animal et l’environnement.
            </p>
        </div>
        
        <div class="content-box">
            <div class="content-title">🛡️ Traçabilité & Sécurité QSE</div>
            <p style="font-size: 0.9rem; text-align: justify;">
            Chaque code d'accès Wi-Fi généré sur ce portail est strictement temporaire, tracé, et soumis aux réglementations RGPD. 
            L'envoi des tickets est dématérialisé par e-mail afin de respecter nos engagements de réduction du papier.
            </p>
            <hr style="margin: 0.8rem 0; border: none; border-top: 1px solid #e2e8f0;">
            <small>📍 <b>Siège social :</b> La Creuse, 79800 SAINTE-EANNE<br>📞 <b>DSI / Contact :</b> +33 (0)5 49 06 28 28</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="serval-footer">
        Mentions légales - Politique de confidentialité - © 2026 Serval S.A.S - 🍃 Site Internet éco-conçu
    </div>
    """, unsafe_allow_html=True)

# --- PAGE 2 : GENERATION DE TICKETS ---
else:
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.markdown(f"<h2 style='color:#004737;'>🟢 Session active : {st.session_state.role} (Serval S.A.S)</h2>", unsafe_allow_html=True)
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
        email = st.text_input("Adresse E-mail du visiteur")

    if st.button("Confirmer et Générer le Ticket", type="primary"):
        if nom_visiteur and societe and email:
            with st.spinner("Génération des identifiants sécurisés Serval..."):
                time.sleep(1.5)
            prefix = "".join(nom_visiteur.lower().split())[:4]
            wifi_id = f"serval_{prefix}{random.randint(10,99)}"
            wifi_key = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=8))
            
            st.success("Ticket créé avec succès !")
            st.markdown(f"""
            <div style="background-color: #ffffff; border: 2px dashed #004737; padding: 2rem; border-radius: 8px; max-width: 500px; margin: 1.5rem auto; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                <div style="text-align:center; margin-bottom:1rem;">
                    <span style="background:#004737; color:white; padding:0.4rem 1rem; font-weight:bold; border-radius:4px;">Serval S.A.S</span>
                </div>
                <h3 style="text-align: center; color: #004737; margin-top: 0; letter-spacing:1px;">TICKET ACCÈS WI-FI</h3>
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
