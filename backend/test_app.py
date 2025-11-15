import pytest
import io
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_no_data_error(client):
    response = client.post('/classificar', data={})
    assert response.status_code == 400
    assert b"Nenhum arquivo ou texto enviado" in response.data

def test_unsupported_file_error(client):
    data = {
        'file': (io.BytesIO(b"dummy zip data"), 'teste.zip')
    }
    response = client.post('/classificar', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b"apenas .txt e .pdf" in response.data

def test_empty_text_error(client):
    data = {
        'email_text': '   '
    }
    response = client.post('/classificar', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    
    assert b"Nenhum arquivo ou texto enviado" in response.data

def test_classify_manual_text_success(client, mocker):
    class MockMessage:
        content = '{"classificacao": "Produtivo", "conteudo": "Teste", "mensagem_sugerida": "Resposta de teste"}'
    class MockChoice:
        message = MockMessage()
    class MockResponse:
        choices = [MockChoice()]
    
    fake_openai_response = MockResponse()
    
    mocker.patch(
        'app.client.chat.completions.create', 
        return_value=fake_openai_response
    )
    
    data = {
        'email_text': 'Este e um e-mail de teste produtivo'
    }
    response = client.post('/classificar', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    assert b"Produtivo" in response.data
    assert b"Resposta de teste" in response.data
    
def test_classify_txt_file_success(client, mocker):
    class MockMessage:
        content = '{"classificacao": "Improdutivo", "conteudo": "Spam", "mensagem_sugerida": "Ignorar"}'
    class MockChoice:
        message = MockMessage()
    class MockResponse:
        choices = [MockChoice()]
    
    fake_openai_response = MockResponse()
    
    mocker.patch(
        'app.client.chat.completions.create', 
        return_value=fake_openai_response
    )
    
    data = {
        'file': (io.BytesIO(b"Clique aqui para ganhar!"), 'spam.txt')
    }
    
    response = client.post('/classificar', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    assert b"Improdutivo" in response.data
    assert b"Ignorar" in response.data