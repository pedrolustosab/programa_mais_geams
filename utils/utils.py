# src/utils.py

import streamlit as st
import pandas as pd
from datetime import date
import time
from pathlib import Path
import os
import base64
import logging
from dotenv import load_dotenv

# --- CARREGAR VARIÁVEIS DE AMBIENTE ---
load_dotenv()

# --- CONSTANTES GLOBAIS ---
# O .parent.parent é necessário porque este arquivo está em 'src/'
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data"
ANEXOS_DIR = BASE_DIR / "anexos"
ANEXOS_DIR.mkdir(exist_ok=True)
DATA_PATH.mkdir(exist_ok=True)

DATA_FILES = {
    "hero": {"path": DATA_PATH / "dim_hero.csv", "cols": ['id_hero', 'hero_name', 'hero_team', 'start_date', 'update_date']},
    "map": {"path": DATA_PATH / "dim_map.csv", "cols": ['id_mission', 'mission_name', 'mission_discribe', 'GemsAwarded', 'id_pillar', 'pillar', 'start_date', 'update_date']},
    "nomination": {"path": DATA_PATH / "fact_nomeacao.csv", "cols": ['id_nomeacao', 'data_submissao', 'id_nomeador', 'id_nomeado', 'id_missao', 'justificativa', 'status', 'caminho_anexo']},
}

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
CACHE_TTL = 300
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# --- LOGGING ---
logger = logging.getLogger(__name__)
# (Adicione sua configuração de logging completa aqui se desejar)

# --- FUNÇÕES DE COMPONENTES DE UI ---
def create_custom_header(title, subtitle="", icon="💎"):
    st.markdown(f"""
    <div class="custom-header">
        <h1 style="margin: 0; font-size: 2.5rem;">{icon} {title}</h1>
        {f'<p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logger.error(f"Erro ao converter imagem para base64: {e}")
        return ""

def get_pillar_image_path(pillar_name):
    if not pillar_name or pd.isna(pillar_name):
        return None
    image_filename = f"{pillar_name.strip().lower().replace(' ', '_')}.png"
    image_path = BASE_DIR / "assets" / "pillar_icons" / image_filename
    return str(image_path) if image_path.exists() else None

def display_pillar_icon(pillar_name, size="40px"):
    image_path = get_pillar_image_path(pillar_name)
    if image_path:
        base64_image = get_image_base64(image_path)
        return f'<img src="data:image/png;base64,{base64_image}" class="pillar-icon" style="width: {size}; height: {size};">'
    return f'<div style="width: {size}; height: {size}; background: var(--accent-color); border-radius: 8px; ...">🏛️</div>'

def show_loading_message(message="Processando..."):
    with st.spinner(message):
        time.sleep(0.3)
        return True

def create_success_animation():
    st.balloons()

# --- FUNÇÕES DE LÓGICA DE DADOS ---
@st.cache_data(ttl=CACHE_TTL)
def load_data(file_key):
    # (Cole sua função load_data completa aqui)
    config = DATA_FILES.get(file_key)
    file_path, columns = config["path"], config["cols"]

    if not file_path.exists():
      logger.info(f"Criando arquivo {file_path.name}")
      df = pd.DataFrame(columns=columns)
      df.to_csv(file_path, index=False, sep=';')
      return df

    try:
      df = pd.read_csv(file_path, sep=';', dtype=str)
      return df.astype(str)
    except (pd.errors.EmptyDataError, FileNotFoundError):
      return pd.DataFrame(columns=columns)


def save_data(file_key, df):
    # (Cole sua função save_data completa aqui)
    file_path = DATA_FILES.get(file_key)["path"]
    try:
        df.to_csv(file_path, index=False, sep=';')
        st.cache_data.clear() # Limpa o cache para recarregar os dados
        return True
    except Exception as e:
        st.error(f"Falha ao salvar dados em {file_path.name}: {e}")
        return False

@st.cache_data(ttl=CACHE_TTL)
def get_dashboard_data():
    # (Cole sua função get_dashboard_data completa aqui)
    df_heroes = load_data('hero')
    df_missions = load_data('map')
    df_nominations = load_data('nomination')

    if df_nominations.empty or df_missions.empty or df_heroes.empty:
      return pd.DataFrame()

    df_missions['GemsAwarded'] = pd.to_numeric(df_missions['GemsAwarded'], errors='coerce').fillna(0)
    df_nominations['data_submissao'] = pd.to_datetime(df_nominations['data_submissao'], errors='coerce')

    approved = df_nominations[df_nominations['status'].str.strip().str.lower() == 'aprovado'].copy()
    if approved.empty:
      return pd.DataFrame()

    data = approved.merge(df_heroes, left_on='id_nomeado', right_on='id_hero', suffixes=('_nomeado', '_hero'))
    data = data.rename(columns={'hero_name': 'Herói', 'hero_team': 'Time'})
    data = data.merge(df_heroes, left_on='id_nomeador', right_on='id_hero', suffixes=('', '_nomeador'))
    data = data.rename(columns={'hero_name': 'Nomeador'})
    data = data.merge(df_missions, left_on='id_missao', right_on='id_mission')

    return data[['data_submissao', 'Herói', 'Time', 'Nomeador', 'mission_name', 'pillar', 'GemsAwarded', 'justificativa']]