import streamlit as st
import pandas as pd  # <- Adicionar esta linha
import base64
from pathlib import Path
import time
from .config import ASSETS_PATH, logger

def create_custom_header(title, subtitle="", icon="💎"):
    """Cria um header customizado e atraente"""
    st.markdown(f"""
    <div class="custom-header">
        <h1 style="margin: 0; font-size: 2.5rem;">{icon} {title}</h1>
        {f'<p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def get_pillar_image_path(pillar_name):
    """Busca o caminho da imagem do pilar baseada no nome"""
    if not pillar_name or pd.isna(pillar_name):
        return None
    
    # Normalizar nome do arquivo
    image_filename = f"{pillar_name.strip().lower().replace(' ', '_').replace('ç', 'c').replace('ã', 'a')}.png"
    image_path = ASSETS_PATH / "pillar_icons" / image_filename
    
    if image_path.exists():
        return str(image_path)
    
    logger.warning(f"Imagem do pilar não encontrada: {image_path}")
    return None

def get_image_base64(image_path):
    """Converte imagem para base64"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logger.error(f"Erro ao converter imagem para base64: {e}")
        return ""

def display_pillar_icon(pillar_name, size="40px"):
    """Exibe o ícone do pilar com fallback"""
    image_path = get_pillar_image_path(pillar_name)
    
    if image_path:
        try:
            base64_str = get_image_base64(image_path)
            if base64_str:
                return f'<img src="data:image/png;base64,{base64_str}" class="pillar-icon" style="width: {size}; height: {size};">'
        except Exception as e:
            logger.error(f"Erro ao exibir ícone do pilar {pillar_name}: {e}")
    
    # Fallback para emoji/ícone padrão
    return f'<div style="width: {size}; height: {size}; background: var(--accent-color); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px;">🏛️</div>'

def get_cover_image():
    """Busca a imagem da capa"""
    cover_path = ASSETS_PATH / "Capa.png"
    if cover_path.exists():
        return str(cover_path)
    return None

def show_loading_message(message="Processando..."):
    """Mostra uma mensagem de loading melhorada"""
    with st.spinner(message):
        time.sleep(0.3)
    return True

def create_success_animation():
    """Cria animação de sucesso"""
    st.balloons()
    time.sleep(1)
    st.success("🎉 Ação concluída com sucesso!")