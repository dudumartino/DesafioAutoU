document.addEventListener('DOMContentLoaded', () => {

    const themeToggleButton = document.getElementById('themeToggleButton');
    const body = document.body;

    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
    } else {
        body.classList.remove('dark-mode');
    }

    themeToggleButton.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.setItem('theme', 'light');
        }
    });

    const localApiUrl = 'http://127.0.0.1:5000/classificar';
    const productionApiUrl = 'https://desafio-autou-backend.onrender.com/classificar';

    let apiUrl = localApiUrl; 
    if (window.location.hostname.includes('onrender.com')) {
        apiUrl = productionApiUrl;
        console.log("A executar em modo de Produção.");
    } else {
        console.log("A executar em modo Local. A ligar a " + localApiUrl);
    }

    const form = document.getElementById('classificationForm');
    const fileInput = document.getElementById('emailFile');
    const textInput = document.getElementById('emailText');
    
    const classifyButton = document.getElementById('classifyButton');
    const buttonText = classifyButton.querySelector('.btn-text');
    const spinner = classifyButton.querySelector('.spinner');

    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    
    const classificationSpan = document.getElementById('classification');
    const contentSpan = document.getElementById('content');
    const suggestedMessagePre = document.getElementById('suggestedMessage');
    
    const copyButton = document.getElementById('copyButton');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); 

        classifyButton.disabled = true;
        classifyButton.classList.add('loading');

        resultDiv.style.display = 'none';
        errorDiv.textContent = '';
        copyButton.style.display = 'none'; 

        const formData = new FormData();
        const file = fileInput.files[0];
        const text = textInput.value;

        if (file) {
            formData.append('file', file);
        } else if (text) {
            formData.append('email_text', text);
        } else {
            errorDiv.textContent = 'Por favor, envie um ficheiro ou insira um texto.';
            classifyButton.disabled = false;
            classifyButton.classList.remove('loading');
            return;
        }

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Erro desconhecido no servidor.');
            }

            classificationSpan.textContent = data.classificacao;
            contentSpan.textContent = data.conteudo;
            suggestedMessagePre.textContent = data.mensagem_sugerida;

            if (data.classificacao === 'Produtivo') {
                resultDiv.className = 'Produtivo';
            } else {
                resultDiv.className = 'Improdutivo';
            }
            
            resultDiv.style.display = 'block';
            copyButton.style.display = 'inline-block'; 
            
            copyButton.classList.remove('copied');

        } catch (error) {
            errorDiv.textContent = 'Erro: ' + error.message;
            console.error('Erro ao classificar:', error);
        } finally {
            classifyButton.disabled = false;
            classifyButton.classList.remove('loading');
            
            fileInput.value = null; 
            textInput.value = ''; 
        }
    });
    
    copyButton.addEventListener('click', () => {
        const textToCopy = suggestedMessagePre.textContent;
        
        navigator.clipboard.writeText(textToCopy).then(() => {
            copyButton.classList.add('copied');
            
            setTimeout(() => {
                copyButton.classList.remove('copied');
            }, 2000); 
        }).catch(err => {
            console.error('Erro ao copiar:', err);
            alert("Erro ao copiar texto."); 
        });
    });

});