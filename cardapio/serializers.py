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

    def validate_produto(self, value):
        if self.instance is None:
            if not value.disponivel:
                raise serializers.ValidationError("Este produto está indisponível.")
        else:
            if value != self.instance.produto:
                raise serializers.ValidationError(
                    "Não é possível trocar o produto de um item. Apague o item e crie outro."
                )
        return value

    def validate_pedido(self, value):
        if value.status == Pedido.statusChoices.ENTREGUE:
            raise serializers.ValidationError("Este pedido já foi entregue e não aceita mais itens.")
        return value

    def validate(self, attrs):
        if self.instance is not None and self.instance.pedido.status == Pedido.statusChoices.ENTREGUE:
            raise serializers.ValidationError(
                "Este pedido já foi entregue e seus itens não podem ser alterados."
            )
        return attrs