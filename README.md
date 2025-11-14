# Desafio AutoU: Classificador Inteligente de E-mails

Este projeto é uma aplicação web desenvolvida como parte do desafio prático de estágio da AutoU. O objetivo é criar uma ferramenta que utiliza Inteligência Artificial (OpenAI GPT) para automatizar a triagem e classificação de e-mails, otimizando o fluxo de trabalho de uma equipa.

A aplicação classifica os e-mails em categorias (Produtivo ou Improdutivo) com base no seu conteúdo e, em seguida, gera um resumo do tópico e uma resposta profissional sugerida, adequada ao contexto.

# Demonstração

links imagens

# Funcionalidades Principais

.Classificação por IA: Utiliza o modelo gpt-3.5-turbo da OpenAI para uma análise de contexto precisa.

.Entrada Múltipla: upload de arquivos .txt, arquivos .pdf e inserção manual de texto.

.Respostas Inteligentes: A IA gera três informações:
1.Classificação: Produtivo ou Improdutivo.
2.Conteúdo: Um resumo de uma linha (ex: "Solicitação de agendamento").
3.Mensagem Sugerida: Uma resposta profissional pronta a usar.

.Interface Moderna com: Modo Noturno, Botão "copiar", Feedback visual no carregamento da classificação e desgin personalizado com a cor da identidade visual da AutoU.

# Tecnologias Utilizadas

O projeto é dividido em duas partes principais:

.Backend:

Python 3

Flask: Para criar o servidor web e a API REST.

OpenAI: Para fazer as chamadas ao modelo GPT.

PyMuPDF (fitz): Para a extração de texto de arquivos .pdf.

python-dotenv: Para gestão segura das chaves de API.

CORS: Para permitir a comunicação entre o frontend e o backend.

.Frontend:

HTML5

CSS3

JavaScript (ES6+): Para a lógica do frontend, chamadas fetch à API e manipulação do DOM.

# Abordagem de PNL (Processamento de Linguagem Natural)

O desafio mencionava a utilização de técnicas clássicas de PNL, como remoção de stop words ou stemming. Esta aplicação não utiliza essas técnicas deliberadamente.

Motivo: As técnicas clássicas são projetadas para modelos de IA mais antigos, que não compreendiam o contexto. Esta aplicação utiliza um Modelo de Linguagem Grande (LLM) moderno (gpt-3.5-turbo), que depende da estrutura completa da frase, incluindo stop words, para entender com precisão a intenção, o tom e o contexto. A remoção dessas palavras iria, na verdade, degradar a performance da classificação e da geração de resposta.

# Como Testar a Aplicação

Existem duas formas de testar esta aplicação:

.Opção 1: Aplicação Online (Recomendado)

A aplicação está hospedada na plataforma Render e está pronta para uso imediato. Nenhuma instalação ou configuração de chave de API é necessária.

Link: [COLE AQUI O SEU LINK DO RENDER QUANDO ESTIVER PRONTO]

OBS: após alguns minutos de inatividade a API entra em modo de hibernação, ao ser requisitada novamente ela demora um pouco para "acordar", mas apenas na primeira vez e dura por volta de 30-60 segundos para voltar a funcionar.

.Opção 2: Guia de Instalação Local

Se preferir baixar o código e executá-lo na sua própria máquina, siga os passos abaixo:

.Pré-requisitos

Python 3.8 ou superior.

Uma Chave de API da OpenAI válida (com créditos ou método de pagamento configurado).

.Guia de Instalação

Clone o repositório:

git clone https://github.com/dudumartino/DesafioAutoU.git  
cd DesafioAutoU

Crie e ative um ambiente virtual:  
(Isto isola as dependências do projeto.)

.Criar o ambiente:  
python -m venv venv

Ativar no Windows:  
.\venv\Scripts\activate

Ativar no macOS/Linux:
source venv/bin/activate

.Instale as dependências do Backend:  
(Isto irá instalar Flask, OpenAI, PyMuPDF, etc.)

pip install -r backend/requirements.txt

.Configure a sua Chave de API:

Na pasta raiz do projeto (DesafioAutoU/), crie um ficheiro chamado .env.  
Abra este ficheiro e adicione a sua chave da OpenAI da seguinte forma:

OPENAI_API_KEY='sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

.Inicie o Servidor Backend:  
No terminal (com o venv ativo), execute:

python backend/app.py

Se tudo estiver correto, verá o servidor a rodar em http://127.0.0.1:5000.

Inicie o Frontend:

Vá ao arquivo index.html, dê um clique com botão direito e selecione "open with live server"

Isto abrirá a aplicação no seu navegador padrão.

Agora já pode testar a aplicação!
