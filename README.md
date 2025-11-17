# BioAI: Assistente de Agrofloresta Inteligente

**Projeto de Finalização do Curso de Inteligência Artificial para Projetos Sustentáveis - Guardiões da Amazônia - I2A2**

## Visão Geral

O BioAI é uma aplicação web de código aberto projetada para apoiar o planejamento e manejo de sistemas agroflorestais, com um foco especial na rica biodiversidade da Amazônia. Utilizando o poder dos modelos de linguagem avançados do Google, como o **Gemini**, esta ferramenta capacita agricultores, comunidades locais e pesquisadores a criar ecossistemas sustentáveis e produtivos.

A aplicação foi desenvolvida para ser uma ferramenta de apoio à regeneração de áreas degradadas, como margens de igarapés, contribuindo para a economia local e gerando segurança alimentar para a comunidade.

## Funcionalidades Principais

*   **Geração de Cronograma com IA:** Crie cronogramas de cultivo detalhados e personalizados com base em suas necessidades, no tamanho da área, na localização e no tempo de colheita esperado.
*   **Análises Preditivas:** Além do cronograma, o BioAI é capaz de gerar análises gráficas sobre:
    *   **Desenvolvimento dos Cultivos:** Acompanhe as fases de crescimento de cada planta.
    *   **Probabilidade de Rendimento:** Obtenha estimativas sobre a produtividade da sua colheita.
    *   **Previsão de Produção:** Calcule a produção esperada com base na área plantada.
    *   **Regeneração do Solo:** Receba uma previsão sobre a melhoria da saúde do solo com base nos cultivos selecionados.
*   **Sugestões de Parceria de Plantas:** Receba recomendações inteligentes sobre quais plantas crescem bem juntas, otimizando o uso da terra e promovendo um ecossistema saudável e resiliente.
*   **Visualização Interativa:** Visualize seu cronograma de cultivo em um gráfico de Gantt interativo, facilitando o acompanhamento das atividades ao longo do tempo.
*   **Compatibilidade com Gemini Free Tier:** A ferramenta é totalmente funcional com o nível gratuito da API do Google Gemini, tornando-a acessível a todos.
*   **Suporte Multilíngue:** A interface está disponível em português, espanhol e inglês.

## Como Executar o Projeto Localmente

Siga estas instruções para configurar e executar o BioAI em seu ambiente de desenvolvimento local.

### Pré-requisitos

*   Python 3.8 ou superior
*   `pip` (gerenciador de pacotes do Python)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/paulocabraljunior/BioAi.git
    cd BioAi
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3.  **Instale as dependências:**
    O arquivo `requirements.txt` contém todas as bibliotecas necessárias com suas versões exatas para garantir a estabilidade.
    ```bash
    pip install -r requirements.txt
    ```

### Execução

1.  **Execute o aplicativo Streamlit:**
    Navegue até o diretório do projeto e execute o seguinte comando no seu terminal:
    ```bash
    streamlit run app.py
    ```

2.  **Acesse no navegador:**
    Após executar o comando, o Streamlit fornecerá um URL local (geralmente `http://localhost:8501`) que você pode abrir em seu navegador para interagir com o aplicativo.

## Arquitetura do Código

O projeto é construído como um aplicativo de página única usando o Streamlit.

*   **`app.py`:** O arquivo principal que contém toda a lógica da aplicação, desde a interface do usuário até a comunicação com a API do Gemini.
*   **`data.csv`:** Um arquivo CSV que contém o conjunto de dados de plantas amazônicas, servindo como base de conhecimento para a IA.
*   **`requirements.txt`:** Lista todas as dependências do projeto com suas versões fixadas, garantindo uma instalação consistente.
