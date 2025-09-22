# Seu código main.py continua o mesmo, pois a correção
# é aplicada através da função apply_custom_styles()

import streamlit as st
import sys
from pathlib import Path

# Adicionar diretórios ao path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from utils.config import setup_page_config, apply_custom_styles
from utils.data_manager import initialize_session_state
from pages import (
    home, salao_herois, mapa_cristais, pergaminho_nomeacoes,
    aprovacao_nomeacao, admin_herois, admin_missoes
)

def main():
    # Configuração inicial
    setup_page_config()
    apply_custom_styles()  # Esta função agora oculta a navegação superior
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
            button_type = "primary" if st.session_state.get('current_page', 'Home') == name else "secondary"
            
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
    page_function()
    
    # Footer
    create_footer()

def create_footer():
    """Cria o footer da aplicação"""
    st.sidebar.markdown("---")
    from utils.config import APP_TITLE, DEBUG
    st.sidebar.markdown(f"{APP_TITLE} v2.0")
    

if __name__ == "__main__":
    main()