# 🍽️ Sistema de Gestão para Comércio/Restaurante

Projeto full-stack em desenvolvimento, simulando o ciclo de vida de um sistema corporativo real: da API transacional até engenharia de dados e análise de comportamento.

> **Status (10/10/2026):** Sprint 2/10 — núcleo da API REST, JWT e permissões **implementados e validados manualmente**. Testes automatizados, endurecimento de segurança e melhorias de modelagem seguem pendentes. Próxima sprint a confirmar pelo backlog original.

## 📌 Sobre o projeto

Sistema de gestão de cardápio e pedidos para restaurante, construído como portfólio técnico para vagas de Estágio/Júnior em **Back-end** e **Engenharia de Dados**. Dividido em três fases:

1. **Back-end & API** — API RESTful desacoplada, autenticação, cache e processamento assíncrono.
2. **Data Warehouse & BI** — pipeline ETL, modelagem dimensional (Star Schema) e dashboards.
3. **Big Data & Deploy** — processamento de dados de comportamento (clickstream) e publicação em produção.

## 🛠️ Stack

| Camada | Tecnologias / estado |
| --- | --- |
| Back-end | Python, Django, Django REST Framework — em uso |
| Autenticação | Simple JWT — implementado e testado manualmente |
| Banco (OLTP) | SQLite no desenvolvimento; PostgreSQL previsto para produção |
| Cache e filas | Redis, Celery — planejados |
| Dados (OLAP) | dbt, Metabase — planejados |
| Big Data | DuckDB ou Spark local — planejado |
| Testes | Thunder Client (manuais); pytest/testes automatizados pendentes |
| Deploy | Render/Railway, AWS S3 — planejados |

## 🗂️ Estrutura principal

```text
Django_restaurante/
├── cardapio/
│   ├── models.py        # Categoria, Produto, Pedido, ItemPedido
│   ├── serializers.py   # Campos e proteção de preco_congelado
│   ├── views.py         # ModelViewSets, perform_create
│   ├── permissions.py   # IsAdminOrReadOnly
│   └── tests.py         # Testes automatizados ainda pendentes
├── setup/
│   ├── settings.py      # DRF + JWT + configurações gerais
│   └── urls.py          # Router e endpoints JWT
├── DECISIONS.md         # ADRs e pendências
└── README.md
```

## 📋 Modelagem e regras atuais

- `Categoria` → múltiplos `Produto` (`ForeignKey`, atualmente `CASCADE`).
- `Pedido` → múltiplos `ItemPedido`.
- `ItemPedido` → `Produto`, com `preco_congelado` salvo por `perform_create()` na criação e protegido contra escrita direta pelo serializer.
- Status dos pedidos centralizados em `TextChoices`: Aguardando (`A`), Em preparo (`P`), Finalizado (`E`).
- **Limitação importante:** o uso atual de `CASCADE` pode apagar itens históricos quando um produto/categoria é excluído. A decisão conceitual de preservar histórico está no ADR-011, mas ainda não foi aplicada ao modelo.
- **Limitação importante:** mudar `produto` em `ItemPedido` por PATCH merece validação para não deixar `preco_congelado` inconsistente.

## 🔐 Autenticação e permissões

Autenticação via JWT; `IsAuthenticated` é a permissão global.

| Recurso | GET/HEAD/OPTIONS | POST/PUT/PATCH/DELETE |
| --- | --- | --- |
| `/categorias/`, `/produtos/` | Públicos | Usuário autenticado com `is_staff=True` |
| `/pedidos/`, `/itens_pedido/` | Usuário autenticado | Usuário autenticado |

> A política para pedidos **não identifica garçons**: qualquer usuário autenticado atende à regra atual. Permissão por cargo e posse do pedido são melhorias futuras.

Rotas JWT: `POST /api/token/` (access/refresh) e `POST /api/token/refresh/` (novo access com refresh válido). Use a barra final `/` nas rotas. Não exponha senhas ou tokens em documentação.

## ✅ Progresso

- [x] Modelos e relacionamentos do MVP
- [x] CRUD de categorias, produtos, pedidos e itens com `ModelViewSet` e `DefaultRouter`
- [x] `TextChoices` e campos explícitos nos serializers
- [x] `preco_congelado` criado no servidor e protegido contra escrita direta na API
- [x] Autenticação JWT via Simple JWT
- [x] Permissão global `IsAuthenticated` e permissão `IsAdminOrReadOnly`
- [x] Testes manuais de leitura/escrita, autenticação, autorização e exclusões via Thunder Client
- [ ] Testes automatizados e validações adicionais de domínio
- [ ] Preservação do histórico de itens (revisão de `CASCADE`/`PROTECT`)
- [ ] Bloqueio de produtos indisponíveis em novos itens e atualização de item
- [ ] Rotacionar e externalizar `SECRET_KEY` antes de exposição/deploy
- [ ] Cache Redis e tarefas assíncronas Celery
- [ ] Pipeline ETL/modelagem dimensional e dashboards
- [ ] Deploy e processamento de eventos de comportamento

## 📖 Decisões de arquitetura e próximos passos

Consulte [`DECISIONS.md`](./DECISIONS.md) para ADR-001 a ADR-011, incluindo a matriz de permissões validada e a decisão **ainda não implementada** de preservar histórico. A ordem da próxima sprint deve respeitar o backlog original.

## 👤 Autor

**Giovane Ponciano Vicente**  
[LinkedIn](https://linkedin.com/in/giovane-vicente) · [GitHub](https://github.com/giponvi)
