# BioAI: Assistente de Agrofloresta Inteligente

**Projeto de Finalização do Curso de Inteligência Artificial para Projetos Sustentáveis - Guardiões da Amazônia - I2A2**

## Visão Geral

O BioAI é uma aplicação web desenvolvida para auxiliar no planejamento e manejo de sistemas agroflorestais, com foco especial na biodiversidade amazônica. Utilizando o poder dos modelos de linguagem avançados do Google (Gemini), esta ferramenta gera cronogramas de cultivo personalizados, sugere parcerias benéficas entre plantas e fornece visualizações interativas para facilitar o acompanhamento.

Uma Ferramenta para Apoiar a regeneração das margens de igarapés contribuindo com a economia local e gerando fartura para a comunidade.

## Funcionalidades Principais

*   **Geração de Cronograma com IA:** Utilize o Google Gemini para criar cronogramas de cultivo detalhados com base em suas necessidades e nas características das plantas amazônicas.
*   **Sugestões de Parceria de Plantas:** Receba recomendações inteligentes sobre quais plantas crescem bem juntas, otimizando o uso da terra e promovendo um ecossistema saudável.
*   **Visualização Interativa:** Visualize seu cronograma de cultivo em um gráfico de Gantt interativo, facilitando o acompanhamento das atividades ao longo do tempo.
*   **Suporte Multilíngue:** A interface está disponível em português, espanhol e inglês, tornando-a acessível a um público global.
*   **Configuração Flexível:** Insira sua própria chave de API do Google Gemini e escolha o modelo que melhor se adapta às suas necessidades.

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

2.  **Instale as dependências:**
    Crie e ative um ambiente virtual (recomendado) e instale as bibliotecas necessárias.
    ```bash
    pip install streamlit pandas google-generativeai altair
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

O projeto é construído como um aplicativo de página única usando o Streamlit, com a seguinte estrutura:

*   **`app.py`:** Este é o arquivo principal que contém toda a lógica do aplicativo.
    *   **Interface do Usuário (UI):** O código configura o título, a descrição, os botões de seleção de idioma e os campos de entrada para a chave da API e a solicitação do usuário.
    *   **Lógica de Negócios:** Inclui funções para:
        *   Carregar e armazenar em cache os dados das plantas do arquivo `data.csv`.
        *   Construir um prompt detalhado para a API Gemini, incorporando os dados e a solicitação do usuário.
        *   Chamar a API Gemini para gerar o cronograma e as sugestões.
        *   Analisar a resposta do modelo e converter a tabela de cronograma em um DataFrame do Pandas.
        *   Gerar e exibir um gráfico de Gantt interativo usando a biblioteca Altair.
*   **`data.csv`:** Um arquivo CSV delimitado por ponto e vírgula que contém o conjunto de dados de plantas amazônicas, incluindo nomes, ciclos de vida, parceiras recomendadas e outras informações relevantes.
