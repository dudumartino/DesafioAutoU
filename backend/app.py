from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader # Usando a biblioteca 'pypdf' atualizada
import os
import openai # Importando a OpenAI
import json
from dotenv import load_dotenv # Para ler o .env

# --- 1. Carregar variáveis de ambiente ---
load_dotenv()
# A biblioteca da OpenAI (v1.0+) lê a chave 'OPENAI_API_KEY' 
# automaticamente do ambiente após o load_dotenv().
try:
    client = openai.OpenAI()
    print("Cliente OpenAI inicializado com sucesso.")
except openai.OpenAIError as e:
    print("Erro ao inicializar o cliente OpenAI. Verifique sua chave API.")
    print(e)
# ------------------------------------------

app = Flask(__name__)
CORS(app)

# Rota /classificar
@app.route('/classificar', methods=['POST'])
def classify_endpoint():
    
    text = "" # Variável para guardar o texto extraído

    try:
        # --- 2. Lógica para extrair o texto ---
        
        # Cenário 1: O usuário enviou um ARQUIVO
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            
            _, extension = os.path.splitext(file.filename)
            
            if extension.lower() == '.txt':
                text = file.read().decode('utf-8')
                
            elif extension.lower() == '.pdf':
                reader = PdfReader(file) # pypdf funciona aqui
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            else:
                return jsonify({'error': 'Formato de arquivo não suportado (apenas .txt e .pdf)'}), 400
        
        # Cenário 2: O usuário digitou TEXTO MANUALMENTE (Lógica Corrigida)
        elif 'email_text' in request.form:
            text = request.form['email_text'] # Apanha o texto, mesmo que seja ' '
        
        else:
             return jsonify({'error': 'Nenhum arquivo ou texto enviado'}), 400

        # Verificação movida para depois de apanhar o texto
        # Checa se o texto final está vazio (ex: PDF ou TXT em branco, ou ' ' manual)
        if not text.strip():
             return jsonify({'error': 'Nenhum texto para classificar (arquivo vazio?)'}), 400

        # --- 3. Lógica do GPT (PROMPT REFINADO) ---
        
        system_prompt = """
        Você é um assistente de e-mail profissional de uma empresa financeira.
        A sua tarefa é analisar o e-mail do utilizador e devolver um JSON com TRÊS chaves:
        1. "classificacao": ("Produtivo" ou "Improdutivo")
        2. "conteudo": Um resumo muito curto do tópico (máx 5 palavras. Ex: "Solicitação de reunião", "Felicitação de aniversário", "Documento irrelevante").
        3. "mensagem_sugerida": Uma resposta profissional para o e-mail.

        REGRAS PARA A MENSAGEM SUGERIDA:
        - REGRA 1 (Produtivo): Se for "Produtivo" (dúvidas, problemas, agendamentos), confirme o recebimento e diga que a equipa irá analisar.
            Ex: "Recebemos a sua solicitação sobre [Tópico]. A nossa equipa irá analisar e retornará em breve."
        - REGRA 2 (Improdutivo - Educado): Se for "Improdutivo" mas educado (ex: "Obrigado", "Feliz Natal"), gere uma resposta curta e educada.
            Ex: "Obrigado pela sua mensagem! Tenha um ótimo dia."
        - REGRA 3 (Improdutivo - Spam): Se for "Improdutivo" e for spam óbvio ou newsletter, a resposta deve ser "Nenhuma resposta necessária."
        - REGRA 4 (Improdutivo - Irrelevante): Se for "Improdutivo" e o conteúdo for aleatório (ex: um relatório da faculdade, um ficheiro enviado por engano), gere uma resposta profissional.
            Ex: "Recebemos o seu e-mail. O conteúdo não parece ser relevante para os nossos serviços. Caso tenha sido enviado por engano, por favor, ignore esta mensagem."

        Responda APENAS com o objeto JSON.
        """
        
        user_prompt = f"Por favor, classifique este e-mail:\n\n\"{text}\""

        # Chamada para a API da OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        json_response = response.choices[0].message.content
        
        return json_response
            
    except Exception as e:
        # Erro genérico
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

# if __name__ == '__main__':
#    app.run(debug=True, port=5000)