from django.shortcuts import render
from rest_framework import viewsets
from .models import Categoria, Produto, Pedido, ItemPedido
from .serializers import CategoriaSerializer, ProdutoSerializer, PedidoSerializer, ItemPedidoSerializer
from .permissions import IsAdminOrReadOnly



class CategoriaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
class ProdutoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    
class ItemPedidoViewSet(viewsets.ModelViewSet):
    queryset = ItemPedido.objects.all()
    serializer_class = ItemPedidoSerializer

    def perform_create(self, serializer):
        produto_escolhido = serializer.validated_data.get('produto')
        serializer.save(preco_congelado=produto_escolhido.preco)
