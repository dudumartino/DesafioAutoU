from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader
import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
try:
    client = openai.OpenAI()
    print("Cliente OpenAI inicializado com sucesso.")
except openai.OpenAIError as e:
    print("Erro ao inicializar o cliente OpenAI. Verifique sua chave API.")
    print(e)

app = Flask(__name__)

origins = [
    "https://desafio-autou-vuof.onrender.com",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "null"
]

CORS(app, resources={r"/*": {"origins": origins}}, supports_credentials=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route('/classificar', methods=['POST'])
def classify_endpoint():
    
    text = "" 

    try:
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            
            _, extension = os.path.splitext(file.filename)
            
            if extension.lower() == '.txt':
                text = file.read().decode('utf-8')
                
            elif extension.lower() == '.pdf':
                reader = PdfReader(file)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            else:
                return jsonify({'error': 'Formato de arquivo não suportado (apenas .txt e .pdf)'}), 400
        
        elif 'email_text' in request.form and request.form['email_text'].strip() != '':
            text = request.form['email_text']
        
        else:
             return jsonify({'error': 'Nenhum arquivo ou texto enviado'}), 400

        if not text.strip():
             return jsonify({'error': 'Nenhum texto para classificar (arquivo vazio?)'}), 400

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

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        json_response = response.choices[0].message.content
        
        return jsonify(json.loads(json_response))
            
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)