from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from cardapio.views import CategoriaViewSet,ProdutoViewSet,PedidoViewSet,ItemPedidoViewSet

router = routers.DefaultRouter()

router.register(r'categorias',CategoriaViewSet)
router.register(r'produtos',ProdutoViewSet)
router.register(r'pedidos',PedidoViewSet)
router.register(r'itens_pedido',ItemPedidoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
