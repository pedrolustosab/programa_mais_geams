import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Carregar variáveis de ambiente
load_dotenv()

# Configurações globais
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = Path(os.getenv("DATA_PATH", str(BASE_DIR / "data")))
ASSETS_PATH = Path(os.getenv("ASSETS_PATH", str(BASE_DIR / "assets")))
ANEXOS_DIR = Path(os.getenv("ANEXOS_PATH", str(BASE_DIR / "anexos")))

# Criar diretórios se não existirem
DATA_PATH.mkdir(exist_ok=True)
ASSETS_PATH.mkdir(exist_ok=True)
ANEXOS_DIR.mkdir(exist_ok=True)

# Variáveis de aplicação
APP_TITLE = os.getenv("APP_TITLE", "Programa +GEMS")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Forje sua lenda, Herói!")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Configuração de cores
PRIMARY_COLOR = os.getenv("STREAMLIT_THEME_PRIMARY_COLOR", "#6B7E7D")
BACKGROUND_COLOR = os.getenv("STREAMLIT_THEME_BACKGROUND_COLOR", "#FFFFFF")

def apply_custom_styles():
    # Seu CSS customizado existente pode vir aqui
    
    # CSS para ocultar o cabeçalho, o menu e a navegação de páginas
    hide_elements_style = """
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        /* Oculta a barra de navegação de múltiplas páginas gerada pelo Streamlit */
        div[data-testid="stSidebarNav"] {display: none;}
        </style>
    """
    st.markdown(hide_elements_style, unsafe_allow_html=True)

# Configuração de logging
def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = os.getenv("LOG_FILE", "gems_program.log")
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ] if DEBUG else [logging.FileHandler(log_file)]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def setup_page_config():
    """Configura a página do Streamlit"""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="💎",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': f"# {APP_TITLE}\n*{APP_DESCRIPTION}*"
        }
    )

def apply_custom_styles():
    """Aplica estilos CSS customizados"""
    st.markdown(f"""
    <style>
        /* Importar fonte do Google */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Paleta Clean */
        :root {{
            --primary-color: {PRIMARY_COLOR};
            --secondary-color: #A8A8A8;
            --accent-color: #D4A574;
            --highlight-color: #B07A57;
            --success-color: #7FB069;
            --warning-color: #E8B04B;
            --error-color: #E85A4F;
            --text-primary: #2F3E46;
            --text-secondary: #52796F;
            --background-light: #F8F9FA;
            --background-card: {BACKGROUND_COLOR};
            --border-color: #E8EFEE;
            --shadow: 0 2px 8px rgba(107, 126, 125, 0.08);
            --shadow-hover: 0 4px 16px rgba(107, 126, 125, 0.12);
            --border-radius: 12px;
        }}
        
        /* Fonte global */
        .main * {{
            font-family: 'Inter', sans-serif !important;
        }}
        
        /* Header personalizado */
        .custom-header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem 1.5rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: var(--shadow);
        }}
        
        /* Cards de KPI clean */
        div[data-testid="stMetric"] {{
            background: var(--background-card);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        div[data-testid="stMetric"]:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
            border-color: var(--primary-color);
        }}
        
        div[data-testid="stMetric"]::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        }}
        
        /* Feed item com imagem */
        .feed-item {{
            background: var(--background-card);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 1rem;
            margin-bottom: 0.75rem;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        
        .feed-item:hover {{
            transform: translateX(4px);
            box-shadow: var(--shadow);
            border-color: var(--primary-color);
        }}
        
        .pillar-icon {{
            width: 40px;
            height: 40px;
            border-radius: 8px;
            object-fit: cover;
            flex-shrink: 0;
        }}
        
        /* Mission card */
        .mission-card {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            background: var(--background-card);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            margin-bottom: 0.5rem;
            transition: all 0.3s ease;
        }}
        
        .mission-card:hover {{
            border-color: var(--primary-color);
            box-shadow: var(--shadow);
        }}
        
        /* Botões clean */
        .stButton > button[kind="primary"] {{
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            font-weight: 500;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
            box-shadow: var(--shadow);
        }}
        
        .stButton > button[kind="primary"]:hover {{
            background: var(--highlight-color);
            transform: translateY(-1px);
            box-shadow: var(--shadow-hover);
        }}
    </style>
    """, unsafe_allow_html=True)

# Arquivos de dados
DATA_FILES = {
    "hero": {
        "path": DATA_PATH / "dim_hero.csv",
        "cols": ['id_hero', 'hero_name', 'hero_team', 'start_date', 'update_date']
    },
    "map": {
        "path": DATA_PATH / "dim_map.csv", 
        "cols": ['id_mission', 'mission_name', 'mission_discribe', 'GemsAwarded', 'id_pillar', 'pillar', 'start_date', 'update_date']
    },
    "nomination": {
        "path": DATA_PATH / "fact_nomeacao.csv",
        "cols": ['id_nomeacao', 'data_submissao', 'id_nomeador', 'id_nomeado', 'id_missao', 'justificativa', 'status', 'caminho_anexo']
    },
}
