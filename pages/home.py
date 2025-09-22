import streamlit as st
from utils.ui_components import create_custom_header, get_cover_image
from utils.config import APP_TITLE, APP_DESCRIPTION

def show_page():
    """Exibe a página inicial"""
    create_custom_header(
        f"Bem-vindo ao {APP_TITLE}!",
        APP_DESCRIPTION,
        "💎"
    )
    
    col1, col2 = st.columns([1, 1.5], gap="large")
    
    with col1:
        # Exibir imagem da capa
        cover_path = get_cover_image()
        if cover_path:
            st.image(cover_path, use_container_width=True, caption="Programa +GEMS")
        else:
            st.markdown("### 💎 **Programa +GEMS**")
            st.info("📸 Adicione uma imagem 'Capa.png' na pasta assets/ para exibir aqui.")
    
    with col2:
        st.markdown("### 🚀 **Como começar sua jornada?**")
        
        tabs = st.tabs(["📍 Explorar", "🏆 Reconhecer", "📊 Acompanhar"])
        
        with tabs[0]:
            st.markdown("""
            **🗺️ Mapa dos Cristais**
            - Descubra todas as missões disponíveis
            - Veja as recompensas em GEMS
            - Explore os diferentes pilares de atuação
            """)
            if st.button("Ir para o Mapa 🗺️", use_container_width=True):
                st.session_state.current_page = "Mapa dos Cristais"
                st.rerun()
        
        with tabs[1]:
            st.markdown("""
            **📜 Pergaminho de Nomeações**
            - Indique colegas que fizeram feitos heroicos
            - Justifique suas nomeações
            - Anexe evidências do reconhecimento
            """)
            if st.button("Fazer Nomeação 📜", use_container_width=True):
                st.session_state.current_page = "Pergaminho de Nomeações"
                st.rerun()
        
        with tabs[2]:
            st.markdown("""
            **⚔️ Salão dos Heróis**
            - Veja o ranking dos participantes
            - Acompanhe as conquistas recentes
            - Analise estatísticas do programa
            """)
            if st.button("Ver Ranking ⚔️", use_container_width=True):
                st.session_state.current_page = "Salão dos Heróis"
                st.rerun()
    
    # Objetivo do Programa
    st.markdown("### 🎯 **Objetivo do Programa**")
    with st.container():
        st.info("Reconhecer e recompensar contribuições excepcionais através de um sistema de gamificação divertido e motivador.", icon="ℹ️")
