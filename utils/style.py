# src/style.py

def load_css():
  """Retorna o CSS completo do aplicativo como uma string."""
  return """
  <style>
    /* Importar fonte do Google */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

      /* Paleta Clean */
    :root {
        --primary-color: #6B7E7D;        /* Verde acinzentado */
        --secondary-color: #A8A8A8;      /* Cinza claro */
        --accent-color: #D4A574;         /* Salmão suave */
        --highlight-color: #B07A57;      /* Marrom suave */
        --success-color: #7FB069;        /* Verde suave */
        --warning-color: #E8B04B;        /* Amarelo suave */
        --error-color: #E85A4F;          /* Vermelho suave */
        --text-primary: #2F3E46;
        --text-secondary: #52796F;
        --background-light: #F8F9FA;
        --background-card: #FFFFFF;
        --border-color: #E8EFEE;
        --shadow: 0 2px 8px rgba(107, 126, 125, 0.08);
        --shadow-hover: 0 4px 16px rgba(107, 126, 125, 0.12);
        --border-radius: 12px;
    }

      /* Fonte global */
    .main * {
        font-family: 'Inter', sans-serif !important;
    }

      /* Header personalizado */
    .custom-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 2rem 1.5rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--shadow);
    }

      /* Cards de KPI clean */
    div[data-testid="stMetric"] {
        background: var(--background-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

      div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
        border-color: var(--primary-color);
    }

      div[data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    }

    /* ... (COLE O RESTO DO SEU CSS AQUI) ... */
    
    /* Mission card */
    .mission-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: var(--background-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
    }

    .mission-card:hover {
        border-color: var(--primary-color);
        box-shadow: var(--shadow);
    }

    /* Responsividade */
    @media (max-width: 768px) {
        .custom-header {
            padding: 1rem;
        }
    }
  </style>
  """