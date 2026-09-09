from app.models.produto import Produto

#Função para verificar o estoque baixo!
def test_verificar_estoque_baixo_quando_estoque_e_zero():
    produto1 = Produto(nome="Camisa P", estoque=0)

    assert produto1.estoque_baixo is True