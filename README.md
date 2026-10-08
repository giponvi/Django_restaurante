# 🍽️ Sistema de Gestão para Comércio/Restaurante

Projeto full-stack em desenvolvimento, simulando o ciclo de vida de um sistema corporativo real: da API transacional até engenharia de dados e análise de comportamento.

> **Status:** 🚧 Em desenvolvimento ativo — Sprint 2/10 (API REST, DRF & JWT)

## 📌 Sobre o Projeto

Sistema de gestão de cardápio e pedidos para restaurante, construído como portfólio técnico para vagas de Estágio/Júnior em **Back-end** e **Engenharia de Dados**. O projeto é dividido em três fases:

1. **Back-end & API** — API RESTful desacoplada, autenticação, cache e processamento assíncrono
2. **Data Warehouse & BI** — pipeline ETL, modelagem dimensional (Star Schema) e dashboards
3. **Big Data & Deploy** — processamento de dados de comportamento (clickstream) e publicação em produção

## 🛠️ Stack

| Camada | Tecnologias |
|---|---|
| Back-end | Python, Django, Django REST Framework |
| Autenticação | JWT (em implementação) |
| Banco (OLTP) | SQLite (dev) → PostgreSQL (prod) |
| Cache & Filas | Redis, Celery |
| Dados (OLAP) | dbt, Metabase |
| Big Data | DuckDB / Spark (local) |
| Testes | pytest, dbt tests |
| Deploy | Render / Railway, AWS S3 |

## 🗂️ Estrutura do Projeto

```
Django_restaurante/
├── cardapio/          # App principal: modelos, serializers, views da API
│   ├── models.py       # Categoria, Produto, Pedido, ItemPedido
│   ├── serializers.py  # Tradução Model ↔ JSON + validação
│   ├── views.py         # ModelViewSets + regras de negócio
├── setup/              # Configuração do projeto Django
│   └── urls.py          # Roteamento via DefaultRouter
└── DECISIONS.md        # Registro de decisões arquiteturais (ADR)
```

## 📋 Modelagem de Dados

- **Categoria** → agrupa múltiplos **Produtos** (1:N, CASCADE)
- **Pedido** → contém múltiplos **ItensPedido** (1:N)
- **ItemPedido** → vincula um Produto a um Pedido, com preço travado no momento da compra (`preco_congelado`), protegido contra alteração externa

## ✅ Progresso

- [x] Modelagem relacional completa
- [x] API REST com ModelViewSet + Router
- [x] Regra de negócio: preço congelado no momento do pedido
- [ ] Autenticação JWT
- [ ] Cache com Redis
- [ ] Processamento assíncrono com Celery
- [ ] Pipeline ETL + modelagem dimensional (dbt)
- [ ] Dashboards (Metabase)
- [ ] Testes automatizados (pytest)
- [ ] Deploy em produção
- [ ] Processamento de Big Data (clickstream)

## 📖 Decisões de Arquitetura

As decisões técnicas do projeto e o porquê de cada uma estão documentadas em [`DECISIONS.md`](./DECISIONS.md).

## 👤 Autor

**Giovane Ponciano Vicente**
[LinkedIn](https://linkedin.com/in/giovane-vicente) · [GitHub](https://github.com/giponvi)
