import streamlit as st
import pandas as pd
import google.generativeai as genai
import altair as alt
import json
import csv
from google.ai.generativelanguage_v1beta.types import content

# Page configuration
st.set_page_config(page_title="BioAI", layout="wide")

# --- Language & Translations ---

if "language" not in st.session_state:
    st.session_state.language = "pt"

col1, col2, col3 = st.sidebar.columns(3)
with col1:
    if st.button("🇧🇷"): st.session_state.language = "pt"
with col2:
    if st.button("🇪🇸"): st.session_state.language = "es"
with col3:
    if st.button("🇬🇧"): st.session_state.language = "en"

translations = {
    "pt": {
        "title": "BioAI: Agrofloresta Inteligente",
        "description": "Agente especialista em sistemas agroflorestais amazônicos.",
        "api_key": "Chave da API do Google Gemini",
        "gemini_model": "Modelo Gemini",
        "context_data": "Dados do Projeto",
        "area_size": "Área (hectares)",
        "location": "Localização",
        "harvest_time": "Tempo (meses)",
        "intro_msg": "Olá! Sou seu assistente especialista em Agrofloresta. Posso gerar cronogramas, analisar parcerias de plantas, criar tabelas e ajudar na gestão da implantação. Como posso ajudar hoje?",
        "placeholder": "Ex: Crie um cronograma para plantar mandioca e açaí...",
        "sidebar_title": "Configurações & Contexto",
        "manage_tab": "Gerenciar Implantação",
        "manage_empty": "Nenhum plano de implantação criado ainda. Peça ao agente para criar um checklist.",
        "error_api_key": "⚠️ Insira a chave da API para começar."
    },
    "es": {
        "title": "BioAI: Agroforestería Inteligente",
        "description": "Agente especialista en sistemas agroforestales amazónicos.",
        "api_key": "Clave API Google Gemini",
        "gemini_model": "Modelo Gemini",
        "context_data": "Datos del Proyecto",
        "area_size": "Área (hectáreas)",
        "location": "Ubicación",
        "harvest_time": "Tiempo (meses)",
        "intro_msg": "¡Hola! Soy tu asistente especialista en Agroforestería. Puedo generar calendarios, analizar asociaciones de plantas, crear tablas y ayudar en la gestión de la implementación. ¿Cómo puedo ayudar hoy?",
        "placeholder": "Ej: Crea un calendario para plantar yuca y açaí...",
        "sidebar_title": "Configuración y Contexto",
        "manage_tab": "Gestionar Implementación",
        "manage_empty": "Aún no se ha creado ningún plan de implementación. Pídele al agente que cree una lista de verificación.",
        "error_api_key": "⚠️ Ingrese la clave API para comenzar."
    },
    "en": {
        "title": "BioAI: Smart Agroforestry",
        "description": "Specialist agent in Amazonian agroforestry systems.",
        "api_key": "Google Gemini API Key",
        "gemini_model": "Gemini Model",
        "context_data": "Project Data",
        "area_size": "Area (hectares)",
        "location": "Location",
        "harvest_time": "Time (months)",
        "intro_msg": "Hello! I am your Agroforestry specialist assistant. I can generate schedules, analyze plant partnerships, create tables, and help manage implementation. How can I help you today?",
        "placeholder": "Ex: Create a schedule for planting cassava and acai...",
        "sidebar_title": "Settings & Context",
        "manage_tab": "Manage Implementation",
        "manage_empty": "No implementation plan created yet. Ask the agent to create a checklist.",
        "error_api_key": "⚠️ Enter API Key to start."
    }
}

t = translations[st.session_state.language]

# --- Sidebar Inputs ---

with st.sidebar:
    st.title(t["sidebar_title"])
    api_key = st.text_input(t["api_key"], type="password")
    # Updated model map to include specific versions to avoid 404 errors
    model_map = {
        "gemini-1.5-flash (Free Tier)": "gemini-1.5-flash-latest",
        "gemini-1.5-flash-001": "gemini-1.5-flash-001",
        "gemini-1.5-pro": "gemini-1.5-pro-latest",
        "gemini-1.5-pro-001": "gemini-1.5-pro-001",
        "gemini-1.0-pro": "gemini-1.0-pro"
    }

    selected_model_label = st.selectbox(
        t["gemini_model"],
        list(model_map.keys()),
        index=0
    )
    gemini_model_name = model_map[selected_model_label]

    # Debug tool to list available models
    if st.button("🔍 Check Available Models (Debug)"):
        if not api_key:
            st.error(t["error_api_key"])
        else:
            try:
                genai.configure(api_key=api_key)
                models = list(genai.list_models())
                model_names = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
                st.success(f"Available Models: {model_names}")
            except Exception as e:
                st.error(f"Error listing models: {e}")

    st.subheader(t["context_data"])
    area_size = st.text_input(t["area_size"], value="1.0")
    location = st.text_input(t["location"], value="Amazonas")
    harvest_time = st.text_input(t["harvest_time"], value="12")

    st.divider()
    st.markdown("### " + t["manage_tab"])
    if "implementation_plan" in st.session_state and not st.session_state.implementation_plan.empty:
        edited_df = st.data_editor(
            st.session_state.implementation_plan,
            num_rows="dynamic",
            key="editor"
        )
        st.session_state.implementation_plan = edited_df
    else:
        st.info(t["manage_empty"])

# --- Data Loading ---

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv", sep=";", quoting=csv.QUOTE_ALL)
        return df
    except Exception as e:
        return None

df_data = load_data()

# --- Tools Definition ---

def plot_cultivation_schedule(events: list[dict]):
    """
    Generates a Gantt chart for the cultivation schedule.
    Args:
        events: List of dicts, each containing 'activity' (str), 'plant' (str), 'start_date' (str YYYY-MM-DD), 'end_date' (str YYYY-MM-DD).
    """
    return json.dumps(events)

def plot_yield_probability(data: list[dict]):
    """
    Generates a bar chart for yield probability.
    Args:
        data: List of dicts with 'plant' (str), 'probability' (int 0-100), 'factors' (str).
    """
    return json.dumps(data)

def plot_production_forecast(data: list[dict]):
    """
    Generates a chart for production forecast.
    Args:
        data: List of dicts with 'plant' (str), 'production_kg_ha' (float).
    """
    return json.dumps(data)

def create_implementation_checklist(tasks: list[str]):
    """
    Creates an interactive checklist for the implementation plan which is displayed in the sidebar.
    Args:
        tasks: List of strings describing the tasks to be done.
    """
    # Update session state directly as a side effect, but return JSON for the log
    df = pd.DataFrame({"Task": tasks, "Done": [False] * len(tasks)})
    # We can't easily update session state from a tool running in a vacuum if using parallel threads,
    # but in Streamlit/Gemini sync execution, this works if we handle it in the loop.
    # For now, return data.
    return json.dumps(tasks)

tools_map = {
    "plot_cultivation_schedule": plot_cultivation_schedule,
    "plot_yield_probability": plot_yield_probability,
    "plot_production_forecast": plot_production_forecast,
    "create_implementation_checklist": create_implementation_checklist
}

available_tools = [plot_cultivation_schedule, plot_yield_probability, plot_production_forecast, create_implementation_checklist]

# --- Main UI ---

st.title(t["title"])
st.caption(t["description"])

# Initialize Chat History
if "history" not in st.session_state:
    st.session_state.history = []
    # Add initial system greeting
    st.session_state.history.append(
        content.Content(role="model", parts=[content.Part(text=t["intro_msg"])])
    )

# Helper to Render History
def render_chart(tool_name, data_json):
    try:
        data = json.loads(data_json)

        if tool_name == "plot_cultivation_schedule":
            df = pd.DataFrame(data)
            df['start_date'] = pd.to_datetime(df['start_date'])
            df['end_date'] = pd.to_datetime(df['end_date'])
            c = alt.Chart(df).mark_bar().encode(
                x='start_date', x2='end_date', y='plant', color='activity'
            ).properties(title="Cronograma")
            st.altair_chart(c, use_container_width=True)

        elif tool_name == "plot_yield_probability":
            df = pd.DataFrame(data)
            c = alt.Chart(df).mark_bar().encode(
                x='probability', y='plant', tooltip='factors'
            ).properties(title="Probabilidade de Rendimento (%)")
            st.altair_chart(c, use_container_width=True)

        elif tool_name == "plot_production_forecast":
            df = pd.DataFrame(data)
            c = alt.Chart(df).mark_bar().encode(
                x='production_kg_ha', y='plant'
            ).properties(title="Produção Estimada (kg/ha)")
            st.altair_chart(c, use_container_width=True)

        elif tool_name == "create_implementation_checklist":
            st.success("Checklist created! Check the Sidebar to manage it.")
            # Also update the sidebar state if not already done
            if "implementation_plan" not in st.session_state or st.session_state.implementation_plan.empty:
                 st.session_state.implementation_plan = pd.DataFrame({"Task": data, "Done": [False]*len(data)})

    except Exception as e:
        st.error(f"Error rendering chart: {e}")

# Display Chat
for msg in st.session_state.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        for part in msg.parts:
            if part.text:
                st.markdown(part.text)
            if part.function_call:
                with st.expander(f"🤖 Using tool: {part.function_call.name}"):
                    st.code(part.function_call.args)
            if part.function_response:
                # Render the result of the tool
                render_chart(part.function_response.name, part.function_response.response["result"])

# Input Area
if prompt := st.chat_input(t["placeholder"]):
    if not api_key:
        st.error(t["error_api_key"])
        st.stop()

    # Add User Message
    user_msg = content.Content(role="user", parts=[content.Part(text=prompt)])
    st.session_state.history.append(user_msg)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        try:
            genai.configure(api_key=api_key)
            # Map display name to ID if needed, or use direct
            # User handles specific model ID in sidebar

            model = genai.GenerativeModel(
                model_name=gemini_model_name,
                tools=available_tools,
                system_instruction=f"""
                Você é um especialista em agrofloresta.
                Use os dados fornecidos abaixo para ajudar o usuário.
                Sempre use as tools disponíveis para visualizar dados (gráficos e checklists) quando solicitado ou quando apropriado para enriquecer a resposta.

                Dados do Contexto:
                - Área: {area_size} ha
                - Local: {location}
                - Tempo: {harvest_time} meses

                Dataset de Plantas:
                {df_data.to_string() if df_data is not None else 'N/A'}
                """
            )

            chat = model.start_chat(history=st.session_state.history)

            # Send message with automatic function calling disabled to handle manual rendering?
            # No, let's try automatic. But automatic execution doesn't return the INTERMEDIATE steps easily for rendering *during* the loop in Streamlit unless we control the loop.
            # To properly render charts in the chat stream, we should manually handle the loop.

            response = chat.send_message(prompt, tool_config={'function_calling_config': 'AUTO'})

            # The response object contains the FINAL text, but `chat.history` contains the intermediate tool calls.
            # We need to extract the NEW messages from chat.history and append them to our session state history.

            # Problem: `chat.send_message` executes everything on the server side (if using newer library features) OR
            # returns a FunctionCall part if NOT using auto-execution.
            # Default behavior of `genai` Python SDK is NOT auto-execution unless enabled?
            # Wait, memory says "google-generativeai==0.8.5".
            # In 0.8.5, `enable_automatic_function_calling` is an option in `start_chat`.

            # If I use `enable_automatic_function_calling=True`, the SDK runs the function.
            # But my functions return JSON strings. The SDK sends that back to Gemini.
            # Gemini then generates text.
            # The intermediate "Plot this" step is HIDDEN from the `response.text`.
            # BUT, `chat.history` will have the record.

            # So:
            # 1. Run query.
            # 2. Update st.session_state.history with new items from chat.history.
            # 3. Re-render the NEW items immediately so the user sees the chart.

            # We need to identify which messages are new.
            old_len = len(st.session_state.history)
            st.session_state.history = chat.history

            # Now render the new messages
            for i in range(old_len, len(chat.history)):
                msg = chat.history[i]
                # Render model messages (text, function_calls) AND function messages (function_response)
                # Note: In some SDK versions, the function_response is in a separate message with role='function'
                # or contained within parts. We check all.

                # Determine role for UI grouping (user vs assistant)
                # Function responses are technical, usually hidden or shown as system/assistant data.
                # Here we group them with assistant or just render them.

                if msg.role == "user":
                    # We already rendered the user prompt above, but if the loop added more user-like messages (unlikely in auto-mode), ignore or handle.
                    continue

                # Render Model or Function parts
                for part in msg.parts:
                    if part.text:
                        st.markdown(part.text)
                    if part.function_call:
                        with st.expander(f"🤖 Using tool: {part.function_call.name}"):
                            st.code(part.function_call.args)
                    if part.function_response:
                            render_chart(part.function_response.name, part.function_response.response["result"])

        except Exception as e:
            st.error(f"Error: {e}")
