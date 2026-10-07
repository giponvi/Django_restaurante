from rest_framework import serializers
from .models import Categoria, Produto, Pedido, ItemPedido


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'disponivel', 'categoria']

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['id', 'nome_cliente','data_criacao', 'status']
        
class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ['id', 'pedido', 'produto', 'quantidade', 'preco_congelado']
        read_only_fields = ['preco_congelado']