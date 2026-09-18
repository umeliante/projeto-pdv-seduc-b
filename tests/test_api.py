from app.models import categoria
from app.models.produto import Produto
from app.models.categoria import Categoria


#Teste para verificar se a tela funciona!
def test_listar_produtos_retorna_200(client):

    resposta = client.get("/produtos/")

    # 200 = ok, a página carregou sem erro.

    assert resposta.status_code == 200


# Teste a tela de produto sem login 
def test_listar_produtos_sem_login():
    from fastapi.testclient import TestClient
    from app.main import app

    client_sem_login = TestClient(app)

    resposta = client_sem_login.get("/produtos/")

    assert resposta.status_code == 401


# Teste pagína lista o produto criado com sucesso!
def test_verificar_produto_criado_com_sucesso(client, db_session_test):

    # Criar uma categoria de teste
    categoria = Categoria(nome="Bonés")
    db_session_test.add(categoria)
    db_session_test.commit()

    # Criar um produto para teste 
    produto = Produto(
        nome="Boné Aba Reta",
        preco=29.99,
        estoque_atual=50,
        categoria_id=categoria.id
    )
    db_session_test.add(produto)
    db_session_test.commit()

    # Fazer a requisição para listar os produtos
    resposta = client.get("/produtos/")

    # Testar se existe o produto na listagem de produtos
    assert "Boné Aba Reta" in resposta.text


# Testar a busca retorna somente os produtos filtrados
def test_listar_produtos_filtrados_por_busca(client, db_session_test):
    # Criar produtos para teste 
    produto1 = Produto(
        nome="Camisa Nike",
        preco=29.99,
        estoque_atual=500,
    )
    produto2 = Produto(
        nome="Caneca Harry Potter",
        preco=139.99,
        estoque_atual=60,
    )
    db_session_test.add(produto1)
    db_session_test.add(produto2)
    db_session_test.commit()

    # Fazer a requisição para listar os produtos filtrados
    resposta = client.get("/produtos", params={"busca": "Harry"})

    # Testar se existe o produto filtrado na listagem de produtos
    assert "Caneca Harry Potter" in resposta.text
    assert "Camisa Nike" not in resposta.text

# Exercício = verificar se a busca da rota cliente funciona.
def test_verificar_busca_clientes(client, db_session_test):
    from app.models.cliente import Cliente

    cliente = Cliente(nome="Danilo", matricula="123456")
    db_session_test.add(cliente)
    db_session_test.commit()

    resposta = client.get("/clientes", params={"busca": "Danilo"}) 

    assert "Danilo" in resposta.text