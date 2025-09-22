"""
Módulo de páginas do Programa +GEMS
Organiza todas as páginas da aplicação
"""

# Importar todos os módulos de páginas
from . import home
from . import salao_herois
from . import mapa_cristais
from . import pergaminho_nomeacoes
from . import aprovacao_nomeacao
from . import admin_herois
from . import admin_missoes

# Disponibilizar para importação externa
__all__ = [
    'home',
    'salao_herois', 
    'mapa_cristais',
    'pergaminho_nomeacoes',
    'aprovacao_nomeacao',
    'admin_herois',
    'admin_missoes'
]
