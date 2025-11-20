# BioAI: Assistente de Agrofloresta Inteligente / Smart Agroforestry Assistant

**Projeto de Finalização do Curso de Inteligência Artificial para Projetos Sustentáveis - Guardiões da Amazônia - I2A2**

## Visão Geral / Overview

### Português
O BioAI é uma aplicação web de código aberto projetada para apoiar o planejamento e manejo de sistemas agroflorestais, com um foco especial na biodiversidade da Amazônia. Utilizando o poder dos modelos de linguagem avançados do Google (**Gemini**), esta ferramenta atua como um agente especialista que capacita agricultores e pesquisadores a criar ecossistemas sustentáveis.

### English
BioAI is an open-source web application designed to support the planning and management of agroforestry systems, with a special focus on Amazonian biodiversity. Using the power of Google's advanced language models (**Gemini**), this tool acts as a specialist agent that empowers farmers and researchers to create sustainable ecosystems.

---

## Funcionalidades e Ferramentas do Agente / Agent Features and Tools

O sistema opera através de uma interface de chat onde um Agente Inteligente interage com o usuário. O Agente possui acesso a diversas ferramentas ("Tools") para gerar visualizações e gerenciar o projeto.

The system operates through a chat interface where an Intelligent Agent interacts with the user. The Agent has access to several "Tools" to generate visualizations and manage the project.

### 1. Interface de Chat Multilíngue / Multilingual Chat Interface
- **PT:** O agente se apresenta e interage na língua selecionada (Português, Espanhol ou Inglês) através das bandeiras na barra lateral.
- **EN:** The agent introduces itself and interacts in the selected language (Portuguese, Spanish, or English) via the flags in the sidebar.

### 2. Ferramentas de Visualização / Visualization Tools

O agente pode invocar as seguintes funções automaticamente para gerar gráficos:
The agent can automatically invoke the following functions to generate charts:

*   **`plot_cultivation_schedule`**
    *   **PT:** Gera um gráfico de Gantt detalhado mostrando o cronograma de atividades (plantio, manejo, colheita) para cada planta ao longo do tempo.
    *   **EN:** Generates a detailed Gantt chart showing the schedule of activities (planting, management, harvest) for each plant over time.

*   **`plot_yield_probability`**
    *   **PT:** Gera um gráfico de barras exibindo a probabilidade de sucesso (%) de cada cultura, incluindo fatores de risco ou benefício no *tooltip*.
    *   **EN:** Generates a bar chart displaying the success probability (%) of each crop, including risk or benefit factors in the *tooltip*.

*   **`plot_production_forecast`**
    *   **PT:** Gera um gráfico estimando a produção em kg/hectare para as culturas selecionadas.
    *   **EN:** Generates a chart estimating production in kg/hectare for the selected crops.

### 3. Gestão de Implantação / Implementation Management

*   **`create_implementation_checklist`**
    *   **PT:** O agente pode criar uma lista de tarefas (checklist) para a implantação do sistema agroflorestal. Esta lista aparece na **Barra Lateral** (Sidebar) na aba "Gerenciar Implantação", onde o usuário pode marcar os itens conforme são concluídos.
    *   **EN:** The agent can create a task list (checklist) for the implementation of the agroforestry system. This list appears in the **Sidebar** under the "Manage Implementation" tab, where the user can check off items as they are completed.

---

## Como Executar / How to Run

### Pré-requisitos / Prerequisites
*   Python 3.10+
*   Google Gemini API Key

### Instalação / Installation

1.  **Clone o repositório / Clone the repository:**
    ```bash
    git clone https://github.com/paulocabraljunior/BioAi.git
    cd BioAi
    ```

2.  **Instale as dependências / Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação / Run the application:**
    ```bash
    streamlit run app.py
    ```

## Estrutura do Projeto / Project Structure

*   **`app.py`:** Aplicação principal Streamlit contendo a lógica do Chat e definições das Tools.
*   **`data.csv`:** Base de dados com informações sobre plantas amazônicas.
