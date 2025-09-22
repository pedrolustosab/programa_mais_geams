import streamlit as st
import pandas as pd
from datetime import date
import time
from utils.ui_components import create_custom_header, show_loading_message, create_success_animation
from utils.data_manager import load_data, save_data
from utils.config import logger

def show_page():
    """Exibe a página de gestão de heróis"""
    create_custom_header(
        "Gestão de Heróis",
        "Administração de heróis do programa",
        "🔑"
    )
    
    df_herois = load_data('hero')
    
    # Verifica se há herói sendo editado
    if 'hero_to_edit_id' in st.session_state:
        show_edit_hero_form(df_herois)
    else:
        show_add_hero_form(df_herois)
        show_heroes_list(df_herois)

def show_edit_hero_form(df_herois):
    """Formulário de edição de herói"""
    hero_id = st.session_state['hero_to_edit_id']
    hero_data = df_herois[df_herois['id_hero'] == hero_id].iloc[0]
    
    st.markdown(f"### ✏️ **Editando Herói: _{hero_data['hero_name']}_**")
    
    with st.form("edit_hero_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            hero_name = st.text_input("🛡️ Nome do Herói", value=hero_data['hero_name'])
        with col2:
            hero_team = st.text_input("👥 Time do Herói", value=hero_data['hero_team'])
        
        col_save, col_cancel = st.columns(2)
        
        with col_save:
            submitted = st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True)
        with col_cancel:
            cancel = st.form_submit_button("❌ Cancelar", type="secondary", use_container_width=True)
        
        if cancel:
            del st.session_state['hero_to_edit_id']
            st.rerun()
        
        if submitted:
            handle_hero_update(hero_id, hero_name, hero_team, df_herois)

def show_add_hero_form(df_herois):
    """Formulário de adição de novo herói"""
    with st.expander("➕ **Cadastrar Novo Herói**", expanded=df_herois.empty):
        with st.form("add_hero_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                hero_name = st.text_input("🛡️ Nome do Novo Herói", placeholder="Ex: João Silva")
            with col2:
                hero_team = st.text_input("👥 Time do Herói", placeholder="Ex: Desenvolvimento")
            
            if st.form_submit_button("🎯 Cadastrar Herói", type="primary", use_container_width=True):
                handle_hero_creation(hero_name, hero_team, df_herois)

def show_heroes_list(df_herois):
    """Lista de heróis existentes"""
    st.divider()
    st.markdown("### 🛡️ **Heróis Existentes**")
    
    if df_herois.empty:
        st.info("👤 Nenhum herói cadastrado ainda.")
    else:
        # Estatísticas rápidas
        show_hero_statistics(df_herois)
        
        # Filtro por time
        show_filtered_heroes(df_herois)

def show_hero_statistics(df_herois):
    """Mostra estatísticas dos heróis"""
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total de Heróis", len(df_herois))
    col2.metric("🏢 Times Únicos", df_herois['hero_team'].nunique())
    col3.metric("📅 Cadastros Hoje", len(df_herois[df_herois['start_date'] == date.today().strftime("%Y-%m-%d")]))

def show_filtered_heroes(df_herois):
    """Mostra heróis com filtro por time"""
    st.markdown("---")
    
    # Filtro por time
    all_teams = ['Todos'] + sorted(df_herois['hero_team'].unique().tolist())
    selected_team = st.selectbox("🏢 Filtrar por Time", all_teams)
    
    filtered_heroes = df_herois if selected_team == 'Todos' else df_herois[df_herois['hero_team'] == selected_team]
    
    for index, row in filtered_heroes.iterrows():
        with st.container(border=True):
            col_info, col_actions = st.columns([3, 1])
            
            with col_info:
                st.markdown(f"### 🛡️ **{row['hero_name']}**")
                st.markdown(f"**👥 Time:** {row['hero_team']}")
                st.caption(f"🆔 ID: {row['id_hero']} | 📅 Criado: {row.get('start_date', 'N/A')}")
            
            with col_actions:
                if st.button("✏️ Editar", key=f"edit_hero_{row['id_hero']}", use_container_width=True):
                    st.session_state['hero_to_edit_id'] = row['id_hero']
                    st.rerun()
                
                if st.button("🗑️ Excluir", key=f"del_hero_{row['id_hero']}", type="secondary", use_container_width=True):
                    handle_hero_deletion(index, row, df_herois)

def handle_hero_update(hero_id, hero_name, hero_team, df_herois):
    """Gerencia atualização de herói"""
    if not hero_name.strip() or not hero_team.strip():
        st.error("Nome e Time são obrigatórios!")
    else:
        if show_loading_message("Atualizando herói..."):
            df_herois.loc[df_herois['id_hero'] == hero_id, ['hero_name', 'hero_team', 'update_date']] = [
                hero_name.strip(), hero_team.strip(), date.today().strftime("%Y-%m-%d")
            ]
            if save_data('hero', df_herois):
                st.success("🎉 Herói atualizado com sucesso!")
                logger.info(f"Herói {hero_id} atualizado: {hero_name}")
                del st.session_state['hero_to_edit_id']
                time.sleep(1)
                st.rerun()

def handle_hero_creation(hero_name, hero_team, df_herois):
    """Gerencia criação de novo herói"""
    if not hero_name.strip() or not hero_team.strip():
        st.error("📝 Nome e Time são obrigatórios.")
    elif hero_name.strip().lower() in df_herois['hero_name'].str.strip().str.lower().values:
        st.error(f"⚠️ O nome '{hero_name}' já existe.")
    else:
        if show_loading_message("Cadastrando herói..."):
            new_id = (pd.to_numeric(df_herois['id_hero'], errors='coerce').max() + 1) if not df_herois.empty else 101
            today = date.today().strftime("%Y-%m-%d")
            new_row = {
                'id_hero': str(new_id), 
                'hero_name': hero_name.strip(), 
                'hero_team': hero_team.strip(), 
                'start_date': today, 
                'update_date': today
            }
            df_updated = pd.concat([df_herois, pd.DataFrame([new_row])], ignore_index=True)
            if save_data('hero', df_updated):
                st.success(f"🎉 Herói '{hero_name}' cadastrado com sucesso!")
                logger.info(f"Novo herói cadastrado: {hero_name} (ID: {new_id})")
                create_success_animation()
                time.sleep(1)
                st.rerun()

def handle_hero_deletion(index, row, df_herois):
    """Gerencia exclusão de herói"""
    if show_loading_message("Excluindo herói..."):
        df_herois.drop(index, inplace=True)
        if save_data('hero', df_herois):
            st.success("🗑️ Herói excluído!")
            logger.info(f"Herói excluído: {row['hero_name']} (ID: {row['id_hero']})")
            time.sleep(1)
            st.rerun()
