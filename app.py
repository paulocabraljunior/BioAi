import streamlit as st
import pandas as pd
import google.generativeai as genai
import altair as alt
from io import StringIO
import re

# Page configuration
st.set_page_config(page_title="BioAI", layout="wide")

# Title and description
st.title("BioAI: Cronograma de Cultivo Inteligente")
st.markdown("Esta ferramenta utiliza a IA do Google Gemini para gerar um cronograma de cultivo personalizado com base em suas necessidades.")

# Language selection
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🇧🇷 Português"):
        st.session_state.language = "pt"
with col2:
    if st.button("🇪🇸 Español"):
        st.session_state.language = "es"
with col3:
    if st.button("🇬🇧 English"):
        st.session_state.language = "en"

# Translations
translations = {
    "pt": {
        "api_key": "Chave da API do Google Gemini",
        "gemini_model": "Escolha o modelo Gemini",
        "area_size": "Tamanho da área (em hectares)",
        "location": "Localização (cidade/estado)",
        "harvest_time": "Tempo esperado de colheita (em meses)",
        "request": "Descreva sua solicitação",
        "generate_schedule": "Gerar Cronograma",
        "schedule_title": "Cronograma de Cultivo Gerado",
        "error_api_key": "Por favor, insira sua chave de API do Google Gemini.",
        "error_request": "Por favor, descreva sua solicitação.",
        "chart_title": "Visualização do Cronograma",
        "chart_warning": "Não foi possível encontrar uma tabela de cronograma na resposta.",
        "chart_columns_warning": "A tabela de cronograma na resposta não tem as colunas esperadas.",
        "chart_generation_warning": "Não foi possível gerar o gráfico a partir da resposta:"
    },
    "es": {
        "api_key": "Clave de API de Google Gemini",
        "gemini_model": "Elige el modelo Gemini",
        "area_size": "Tamaño del área (en hectáreas)",
        "location": "Ubicación (ciudad/estado)",
        "harvest_time": "Tiempo de cosecha esperado (en meses)",
        "request": "Describe tu solicitud",
        "generate_schedule": "Generar Calendario",
        "schedule_title": "Calendario de Cultivo Generado",
        "error_api_key": "Por favor, introduce tu clave de API de Google Gemini.",
        "error_request": "Por favor, describe tu solicitud.",
        "chart_title": "Visualización del Calendario",
        "chart_warning": "No se pudo encontrar una tabla de calendario en la respuesta.",
        "chart_columns_warning": "La tabla de calendario en la respuesta no tiene las columnas esperadas.",
        "chart_generation_warning": "No se pudo generar el gráfico a partir de la respuesta:"
    },
    "en": {
        "api_key": "Google Gemini API Key",
        "gemini_model": "Choose the Gemini model",
        "area_size": "Area size (in hectares)",
        "location": "Location (city/state)",
        "harvest_time": "Expected harvest time (in months)",
        "request": "Describe your request",
        "generate_schedule": "Generate Schedule",
        "schedule_title": "Generated Cultivation Schedule",
        "error_api_key": "Please enter your Google Gemini API key.",
        "error_request": "Please describe your request.",
        "chart_title": "Schedule Visualization",
        "chart_warning": "Could not find a schedule table in the response.",
        "chart_columns_warning": "The schedule table in the response does not have the expected columns.",
        "chart_generation_warning": "Could not generate the chart from the response:"
    }
}

# Set default language if not set
if "language" not in st.session_state:
    st.session_state.language = "pt"

# Get translated text
t = translations[st.session_state.language]


# API Key and Gemini Model selection
api_key = st.text_input(t["api_key"], type="password")
gemini_model = st.selectbox(t["gemini_model"], ["gemini-pro", "gemini-1.0-pro", "gemini-1.5-flash", "gemini-1.5-pro"])
area_size = st.text_input(t["area_size"])
location = st.text_input(t["location"])
harvest_time = st.text_input(t["harvest_time"])


# User request
user_request = st.text_area(t["request"])

# --- Main Logic ---

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv", sep=";")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar data.csv: {e}")
        return None

def generate_schedule(api_key, gemini_model, user_request, df, area_size, location, harvest_time):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(gemini_model)
        prompt = f"""
        **Instruções para o Modelo de Linguagem:**
        Você é um assistente de IA especializado em agrofloresta amazônica.

        **Tarefa:**
        Com base nos dados fornecidos e na solicitação do usuário, crie um cronograma de cultivo detalhado e sugira parcerias entre plantas.

        **Formato de Saída OBRIGATÓRIO (use Markdown):**
        1.  **Parcerias Recomendadas:** Uma breve análise das parcerias de plantas.
        2.  **Cronograma de Cultivo:** Uma tabela Markdown **EXATAMENTE** com as seguintes colunas: `Atividade`, `Planta`, `Início`, `Fim`.
            *   As datas de `Início` e `Fim` **DEVEM** estar no formato `YYYY-MM-DD`.
            *   **NÃO** inclua a linha de separador do Markdown (`|---|---|...`).

        **Dados Adicionais:**
        *   Tamanho da área: {area_size} hectares
        *   Localização: {location}
        *   Tempo esperado de colheita: {harvest_time} meses

        **Conjunto de Dados:**
        ```
        {df.to_string()}
        ```

        **Solicitação do Usuário:**
        ```
        {user_request}
        ```
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Ocorreu um erro na API Gemini: {e}")
        return None

def parse_and_display_chart(response_text):
    st.subheader(t["chart_title"])
    try:
        # Use regex to find the markdown table
        table_match = re.search(r"\| Atividade.*\|.*\n((?:\|.*\|.*\n)+)", response_text, re.MULTILINE)
        if not table_match:
            st.warning(t["chart_warning"])
            return

        table_str = table_match.group(1)
        # Clean up the table string by processing each line
        lines = table_str.strip().split('\n')
        csv_lines = ["Atividade,Planta,Início,Fim"]
        for line in lines:
            if line.strip():
                # Split by pipe, remove leading/trailing whitespace from each part, and join with commas
                parts = [part.strip() for part in line.split('|')]
                # Filter out empty parts that result from leading/trailing pipes
                parts = [part for part in parts if part]
                if len(parts) == 4:
                    csv_lines.append(",".join(parts))

        csv_data = "\n".join(csv_lines)
        schedule_df = pd.read_csv(StringIO(csv_data))

        # Data validation
        if not all(col in schedule_df.columns for col in ["Atividade", "Planta", "Início", "Fim"]):
            st.warning(t["chart_columns_warning"])
            return

        schedule_df["Início"] = pd.to_datetime(schedule_df["Início"])
        schedule_df["Fim"] = pd.to_datetime(schedule_df["Fim"])

        chart = alt.Chart(schedule_df).mark_bar().encode(
            x='Início',
            x2='Fim',
            y=alt.Y('Planta', sort=None),
            color=alt.Color('Atividade', scale=alt.Scale(scheme='category10'))
        ).properties(
            title=t["schedule_title"]
        )
        st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.warning(f"{t['chart_generation_warning']} {e}")


# --- Button Logic ---

if st.button(t["generate_schedule"]):
    if not api_key:
        st.error(t["error_api_key"])
    elif not user_request:
        st.error(t["error_request"])
    else:
        df = load_data()
        if df is not None:
            response_text = generate_schedule(api_key, gemini_model, user_request, df, area_size, location, harvest_time)
            if response_text:
                st.subheader(t["schedule_title"])
                st.markdown(response_text)
                parse_and_display_chart(response_text)
