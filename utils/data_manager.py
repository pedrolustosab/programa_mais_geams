import streamlit as st
import pandas as pd
from pathlib import Path
import logging
from .config import DATA_FILES, CACHE_TTL

logger = logging.getLogger(__name__)

def initialize_session_state():
    """Inicializa variáveis de sessão necessárias"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False

@st.cache_data(ttl=CACHE_TTL)
def load_data(file_key):
    """Carrega dados dos arquivos CSV com cache"""
    config = DATA_FILES.get(file_key)
    if not config:
        logger.error(f"Configuração não encontrada para: {file_key}")
        return pd.DataFrame()
    
    file_path, columns = config["path"], config["cols"]
    
    if not file_path.exists():
        logger.info(f"Criando arquivo {file_path.name}")
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False, sep=';')
        return df
    
    try:
        df = pd.read_csv(file_path, sep=';', dtype=str)
        for col in columns:
            if col not in df.columns:
                df[col] = pd.NA
        logger.debug(f"Dados carregados de {file_path.name}: {len(df)} registros")
        return df.astype(str)
        
    except (pd.errors.EmptyDataError, FileNotFoundError):
        logger.warning(f"Arquivo {file_path.name} vazio ou não encontrado")
        return pd.DataFrame(columns=columns)
    except Exception as e:
        logger.error(f"Erro crítico ao carregar {file_path.name}: {e}")
        st.error(f"Erro crítico ao carregar {file_path.name}: {e}")
        return pd.DataFrame(columns=columns)

def save_data(file_key, df):
    """Salva dados em arquivo CSV"""
    file_path = DATA_FILES.get(file_key)["path"]
    try:
        df.to_csv(file_path, index=False, sep=';')
        st.cache_data.clear()
        logger.info(f"Dados salvos em {file_path.name}: {len(df)} registros")
        return True
    except Exception as e:
        logger.error(f"Falha ao salvar dados em {file_path.name}: {e}")
        st.error(f"Falha ao salvar dados em {file_path.name}: {e}")
        return False

@st.cache_data(ttl=CACHE_TTL)
def get_dashboard_data():
    """Prepara dados para o dashboard com melhor performance"""
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
    
    return data[[
        'data_submissao', 'Herói', 'Time', 'Nomeador', 'mission_name', 
        'pillar', 'GemsAwarded', 'justificativa'
    ]]
