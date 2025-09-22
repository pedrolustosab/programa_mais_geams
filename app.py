import streamlit as st
import sys
from pathlib import Path

# Adicionar diretórios ao path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from utils.config import setup_page_config, apply_custom_styles
from utils.data_manager import initialize_session_state

# Importação alternativa mais robusta
try:
    from pages import (
        home, salao_herois, mapa_cristais, pergaminho_nomeacoes,
        aprovacao_nomeacao, admin_herois, admin_missoes
    )
except ImportError as e:
    st.error(f"Erro ao importar páginas: {e}")
    st.stop()

def main():
    """Função principal da aplicação"""
    # Configuração inicial
    setup_page_config()
    apply_custom_styles()
    initialize_session_state()
    
    # Sidebar de navegação
    create_navigation_sidebar()
    
    # Executar página selecionada
    execute_current_page()

def create_navigation_sidebar():
    """Cria a barra lateral de navegação"""
    st.sidebar.markdown("### 💎 **Navegação**")
    st.sidebar.divider()
    
    # Autenticação de administrador
    handle_admin_authentication()
    
    st.sidebar.divider()
    
    # Páginas disponíveis
    PAGES = {
        "Home": ("🏠", home.show_page, False),
        "Salão dos Heróis": ("⚔️", salao_herois.show_page, False),
        "Mapa dos Cristais": ("🗺️", mapa_cristais.show_page, False),
        "Pergaminho de Nomeações": ("📜", pergaminho_nomeacoes.show_page, False),
        "Aprovação da Nomeação": ("👑", aprovacao_nomeacao.show_page, True),
        "Gestão de Heróis": ("🔑", admin_herois.show_page, True),
        "Administração de Missões": ("🔑", admin_missoes.show_page, True),
    }
    
    # Criar botões de navegação
    for name, (icon, _, needs_admin) in PAGES.items():
        if not needs_admin or st.session_state.get('is_admin', False):
            current_page = st.session_state.get('current_page', 'Home')
            button_type = "primary" if current_page == name else "secondary"
            
            if st.sidebar.button(f"{icon} {name}", use_container_width=True, type=button_type):
                st.session_state.current_page = name
                st.rerun()

def handle_admin_authentication():
    """Gerencia a autenticação de administrador"""
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    
    password = st.sidebar.text_input("🔑 Senha de Administrador", type="password")
    
    from utils.config import ADMIN_PASSWORD
    if password == ADMIN_PASSWORD:
        st.session_state.is_admin = True
        st.sidebar.success("🔓 Acesso liberado!")
    elif password:
        st.sidebar.error("❌ Senha incorreta.")

def execute_current_page():
    """Executa a página selecionada"""
    PAGES = {
        "Home": home.show_page,
        "Salão dos Heróis": salao_herois.show_page,
        "Mapa dos Cristais": mapa_cristais.show_page,
        "Pergaminho de Nomeações": pergaminho_nomeacoes.show_page,
        "Aprovação da Nomeação": aprovacao_nomeacao.show_page,
        "Gestão de Heróis": admin_herois.show_page,
        "Administração de Missões": admin_missoes.show_page,
    }
    
    current_page = st.session_state.get('current_page', 'Home')
    page_function = PAGES.get(current_page, home.show_page)
    
    try:
        page_function()
    except Exception as e:
        st.error(f"Erro ao carregar a página: {e}")
        st.info("Redirecionando para a página inicial...")
        st.session_state.current_page = 'Home'
        home.show_page()
    
    # Footer
    create_footer()

def create_footer():
    """Cria o footer da aplicação"""
    st.sidebar.markdown("---")
    from utils.config import APP_TITLE, DEBUG
    st.sidebar.markdown(f"{APP_TITLE} v2.0")
    
    if DEBUG:
        import os
        st.sidebar.markdown("🔧 **Debug Mode**")
        st.sidebar.text(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")

if __name__ == "__main__":
    main()
