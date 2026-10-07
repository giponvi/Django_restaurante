from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    disponivel = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    class statusChoices(models.TextChoices):
        AGUARDANDO = 'A'
        PREPARANDO = 'P'
        ENTREGUE = 'E'
    nome_cliente = models.CharField(max_length = 150)
    data_criacao = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length = 1, choices = statusChoices, default = statusChoices.AGUARDANDO)

    def __str__(self):
        return self.nome_cliente

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete = models.CASCADE, related_name = 'itens_pedido')
    produto = models.ForeignKey(Produto, on_delete = models.CASCADE, related_name = 'produtos_pedido')
    quantidade = models.IntegerField()
    preco_congelado = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"