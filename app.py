import streamlit as st
import pandas as pd
import google.generativeai as genai
import altair as alt
from io import StringIO
import re

# Page configuration
st.set_page_config(page_title="BioAI", layout="wide")

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
        "title": "BioAI: Agrofloresta Inteligente",
        "description": "Esta ferramenta utiliza a IA do Google O Gemini para gerar uma Agrofloresta específica para o bioma Amazônico",
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
        "title": "BioAI: Agroforestería Inteligente",
        "description": "Esta herramienta utiliza la IA de Google O Gemini para generar una Agroforestería específica para el bioma Amazónico",
        "api_key": "Clave de API de Google Gemini",
        "gemini_model": "Elige o modelo Gemini",
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
        "chart_generation_warning": "No se pudo generar el gráfico a partir da resposta:"
    },
    "en": {
        "title": "BioAI: Smart Agroforestry",
        "description": "This tool uses Google's Gemini AI to generate a specific Agroforestry for the Amazon biome",
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

# Title and description
st.title(t["title"])
st.markdown(t["description"])


# API Key and Gemini Model selection
api_key = st.text_input(t["api_key"], type="password")
model_options = {
    "gemini-pro": "gemini-pro",
    "gemini-1.0-pro": "gemini-1.0-pro",
    "gemini-1.5-flash (Free Tier)": "gemini-1.5-flash",
    "gemini-1.5-pro": "gemini-1.5-pro"
}
gemini_model_display = st.selectbox(t["gemini_model"], list(model_options.keys()))
gemini_model = model_options[gemini_model_display]
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

        **Formato de Saída OBRIGATÓRIO (use CSV):**
        1.  **Parcerias Recomendadas:** Uma breve análise das parcerias de plantas.
        2.  **Cronograma de Cultivo:** Um bloco de código CSV com as colunas: `Atividade`, `Planta`, `Início`, `Fim`.
        3.  **Desenvolvimento dos Cultivos:** Um bloco de código CSV com as colunas: `Planta`, `Estágio`, `Duração (dias)`.
        4.  **Probabilidade de Rendimento:** Um bloco de código CSV com as colunas: `Planta`, `Probabilidade (%)`, `Fatores`.
        5.  **Previsão de Produção:** Um bloco de código CSV com as colunas: `Planta`, `Produção (kg/hectare)`.
        6.  **Regeneração do Solo:** Um bloco de código CSV com as colunas: `Indicador`, `Valor Inicial`, `Valor Final`.

        **Dados Adicionais:**
        *   Tamanho da área: {area_size} hectares
        *   Localização: {location}
        *   Tempo esperado de colheita: {harvest_time} meses

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
        # Use a more robust regex to find the CSV block, making the language identifier optional
        csv_match = re.search(r"Cronograma de Cultivo:\s*```(?:csv)?\s*\n(.*?)\n```", response_text, re.DOTALL)
        if not csv_match:
            st.warning(t["chart_warning"])
            return

        csv_data = csv_match.group(1)
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


def parse_and_display_development_chart(response_text):
    st.subheader("Desenvolvimento dos Cultivos")
    try:
        csv_match = re.search(r"Desenvolvimento dos Cultivos:\s*```(?:csv)?\s*\n(.*?)\n```", response_text, re.DOTALL)
        if not csv_match:
            st.warning("Não foi possível encontrar dados de desenvolvimento dos cultivos na resposta.")
            return

        csv_data = csv_match.group(1)
        df = pd.read_csv(StringIO(csv_data))

        if not all(col in df.columns for col in ["Planta", "Estágio", "Duração (dias)"]):
            st.warning("A tabela de desenvolvimento dos cultivos não tem as colunas esperadas.")
            return

        chart = alt.Chart(df).mark_bar().encode(
            x='sum(Duração (dias))',
            y='Planta',
            color='Estágio'
        ).properties(
            title="Fases de Desenvolvimento dos Cultivos"
        )
        st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.warning(f"Não foi possível gerar o gráfico de desenvolvimento: {e}")


def parse_and_display_yield_chart(response_text):
    st.subheader("Probabilidade de Rendimento")
    try:
        csv_match = re.search(r"Probabilidade de Rendimento:\s*```(?:csv)?\s*\n(.*?)\n```", response_text, re.DOTALL)
        if not csv_match:
            st.warning("Não foi possível encontrar dados de probabilidade de rendimento na resposta.")
            return

        csv_data = csv_match.group(1)
        df = pd.read_csv(StringIO(csv_data))

        if not all(col in df.columns for col in ["Planta", "Probabilidade (%)", "Fatores"]):
            st.warning("A tabela de probabilidade de rendimento não tem as colunas esperadas.")
            return

        chart = alt.Chart(df).mark_bar().encode(
            x='Probabilidade (%)',
            y='Planta',
            tooltip=['Fatores']
        ).properties(
            title="Probabilidade de Rendimento por Cultura"
        )
        st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.warning(f"Não foi possível gerar o gráfico de probabilidade de rendimento: {e}")


def parse_and_display_production_chart(response_text):
    st.subheader("Previsão de Produção")
    try:
        csv_match = re.search(r"Previsão de Produção:\s*```(?:csv)?\s*\n(.*?)\n```", response_text, re.DOTALL)
        if not csv_match:
            st.warning("Não foi possível encontrar dados de previsão de produção na resposta.")
            return

        csv_data = csv_match.group(1)
        df = pd.read_csv(StringIO(csv_data))

        if not all(col in df.columns for col in ["Planta", "Produção (kg/hectare)"]):
            st.warning("A tabela de previsão de produção não tem as colunas esperadas.")
            return

        chart = alt.Chart(df).mark_bar().encode(
            x='Produção (kg/hectare)',
            y='Planta'
        ).properties(
            title="Previsão de Produção por Cultura"
        )
        st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.warning(f"Não foi possível gerar o gráfico de previsão de produção: {e}")


def parse_and_display_soil_chart(response_text):
    st.subheader("Regeneração do Solo")
    try:
        csv_match = re.search(r"Regeneração do Solo:\s*```(?:csv)?\s*\n(.*?)\n```", response_text, re.DOTALL)
        if not csv_match:
            st.warning("Não foi possível encontrar dados de regeneração do solo na resposta.")
            return

        csv_data = csv_match.group(1)
        df = pd.read_csv(StringIO(csv_data))

        if not all(col in df.columns for col in ["Indicador", "Valor Inicial", "Valor Final"]):
            st.warning("A tabela de regeneração do solo não tem as colunas esperadas.")
            return

        df_melted = df.melt(id_vars=['Indicador'], value_vars=['Valor Inicial', 'Valor Final'],
                            var_name='Estágio', value_name='Valor')

        chart = alt.Chart(df_melted).mark_bar().encode(
            x='Indicador',
            y='Valor',
            color='Estágio'
        ).properties(
            title="Previsão de Regeneração do Solo"
        )
        st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.warning(f"Não foi possível gerar o gráfico de regeneração do solo: {e}")


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
                parse_and_display_development_chart(response_text)
                parse_and_display_yield_chart(response_text)
                parse_and_display_production_chart(response_text)
                parse_and_display_soil_chart(response_text)
