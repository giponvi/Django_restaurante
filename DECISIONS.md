# DECISIONS.md — Sistema de Gestão para Comércio/Restaurante

Registro de decisões arquiteturais e de implementação do projeto. Cada entrada documenta o contexto, a decisão tomada, alternativas consideradas e as consequências — para que qualquer pessoa (incluindo eu mesmo, no futuro) entenda o *porquê*, não só o *o quê*.

Formato: `ADR-XXX` (Architecture/Implementation Decision Record), em ordem cronológica.

---

## Camada Macro — Arquitetura do Projeto

### ADR-001 — Stack principal: Python, Django, DRF
**Contexto:** escolha da linguagem/framework principal do projeto, pensando em especialização profunda (perfil T-Shaped) para maximizar empregabilidade em vagas Júnior de Back-end e Dados.
**Decisão:** Python como linguagem vertical de especialização; Django + Django REST Framework como stack de back-end.
**Alternativas consideradas:** Java/Spring Boot como stack principal (descartado — já coberto como prova de versatilidade via projeto acadêmico paralelo, o UPX).
**Consequências:** todo o roadmap de 10 sprints é construído em cima dessa escolha. Aprofundamento em Java fica condicionado a sinal real de mercado, avaliado só após iniciar candidaturas com portfólio Python pronto.

### ADR-002 — Processamento de Big Data local, não em cluster cloud
**Contexto:** a Sprint 10 (Big Data/Clickstream) poderia usar Spark em cluster cloud (AWS EMR, Databricks) ou processamento local.
**Decisão:** DuckDB ou Spark em modo local.
**Alternativas consideradas:** cluster Spark gerenciado na nuvem — descartado por custo financeiro e complexidade de infraestrutura desproporcionais ao estágio atual do portfólio.
**Consequências:** mantém a narrativa de "Big Data" em entrevista sem o custo de infraestrutura cloud completa; menor realismo de escala comparado a um cluster real, aceito como trade-off consciente.

### ADR-003 — Deploy em PaaS (Render/Railway), não AWS completo
**Contexto:** necessidade de hospedar a aplicação para a Fase de Deploy (Sprint 9).
**Decisão:** Render ou Railway para a API e banco; AWS S3 usado exclusivamente para armazenamento de arquivos de log de clickstream.
**Alternativas consideradas:** stack AWS completa (EC2, RDS) — descartada por exigir mais tempo de configuração de infraestrutura sem ganho proporcional de aprendizado para o nível júnior-alvo.
**Consequências:** CI/CD mais simples; menor exposição a conceitos de infraestrutura AWS além do S3 básico.

### ADR-004 — UPX mantido como MVP mínimo, sem expansão ativa
**Contexto:** projeto acadêmico paralelo em Java 17/Spring Boot/JPA, majoritariamente gerado com apoio de IA. Dúvida inicial sobre recriar todo o roadmap em Java após concluir as 10 sprints em Python.
**Decisão:** não investir tempo ativo aprofundando o UPX. Escopo fechado como MVP mínimo: cadastro de usuários, resolução de questões com validação simples, Java puro + MySQL + HTML/CSS.
**Alternativas consideradas:** repetir as 10 sprints completas em Java/Spring — descartado (ver ADR-001).
**Consequências:** antes de expor no GitHub como peça de portfólio, é necessária uma passada de leitura ativa do código gerado, para conseguir defender as decisões de arquitetura (ex: uso de DTOs, camada de serviço) em entrevista técnica. Prazo de entrega: semana de 16/11/2026 (grade acadêmica).

### ADR-005 — Front-end minimalista (HTML + Bootstrap puro)
**Contexto:** necessidade de alguma interface web para as Views do projeto principal.
**Decisão:** HTML + Bootstrap, sem framework reativo (React/Vue/Angular).
**Alternativas consideradas:** front-end reativo — descartado para manter foco total em back-end e engenharia de dados, que são as trilhas-alvo de empregabilidade.
**Consequências:** menor apelo visual do projeto, aceito como trade-off já que o público-alvo da avaliação (recrutador técnico de back-end/dados) prioriza arquitetura de API e dados sobre interface.

---

## Camada de Código — Sprint 2 (API REST, DRF)

### ADR-006 — `TextChoices` em vez de lista manual de tuplas para `status`
**Contexto:** o campo `status` de `Pedido` precisava de um conjunto fixo de valores possíveis (Aguardando, Em preparo, Finalizado).
**Decisão:** uso de `models.TextChoices` (classe interna `statusChoices`), com valor e rótulo explícitos por opção (`AGUARDANDO = 'A', 'Aguardando'`).
**Alternativas consideradas:** lista manual de tuplas (`opcoes = [('A', 'Aguardando'), ...]`) — versão inicial do código, substituída por ser menos legível e mais propensa a erro de digitação espalhado pelo código.
**Consequências:** código mais legível, valores centralizados numa única classe, rótulo customizável independente do nome do atributo Python.

### ADR-007 — `fields` explícitos nos Serializers, nunca `'__all__'`
**Contexto:** versão inicial dos Serializers usava `fields = '__all__'` em 3 dos 4 serializers, expondo automaticamente qualquer campo futuro do Model sem controle.
**Decisão:** toda classe `Meta` declara a lista explícita de campos, incluindo sempre o `id`.
**Alternativas consideradas:** `'__all__'` — descartado por risco de exposição não controlada de dados em caso de novo campo adicionado ao Model no futuro.
**Consequências:** qualquer novo campo de Model exige decisão consciente de inclusão no Serializer antes de ser exposto pela API — comportamento seguro por padrão (secure by default).

### ADR-008 — `preco_congelado`: `read_only_fields` + cálculo via `perform_create`
**Contexto:** o preço do item de pedido precisa ser travado no momento da compra, sem poder ser manipulado pelo cliente via payload da requisição (criação ou atualização).
**Decisão:** campo `preco_congelado` declarado em `read_only_fields` no `ItemPedidoSerializer` (bloqueia escrita externa, tanto em `POST` quanto em `PATCH`/`PUT`) **combinado com** sobrescrita de `perform_create` no `ItemPedidoViewSet`, que busca o preço real do `Produto` relacionado e o injeta no momento do salvamento.
**Alternativas consideradas:** confiar apenas no `perform_create` sem `read_only_fields` — rejeitado por deixar a rota de atualização (`perform_update`, não sobrescrita) vulnerável a manipulação do preço via `PATCH`.
**Consequências:** o campo é protegido em todas as operações de escrita, não apenas na criação. O valor só pode ser definido pelo servidor, nunca pelo cliente.

### ADR-009 — Nomenclatura de rotas em snake_case (`itens_pedido`)
**Contexto:** a rota inicial estava registrada como `itemPedido` (camelCase), inconsistente com o padrão das demais rotas (`categorias`, `produtos`, `pedidos`).
**Decisão:** padronização para `itens_pedido`, seguindo convenção REST comum (plural, snake_case), igual ao padrão já usado no projeto To-Do paralelo.
**Alternativas consideradas:** manter camelCase — descartado por quebrar consistência com o restante da API.
**Consequências:** nenhuma funcional; apenas consistência e legibilidade da API para quem for consumi-la.

---

## Pendente de Decisão (em aberto)

- **População do banco de dados para testes/demonstração:** planejado para mais à frente no roadmap — usar dados reais da internet ou gerados sinteticamente, como base para montagem de dashboard em Power BI (complementar ao Metabase já previsto na Sprint 7).
- **Autenticação JWT (Sprint 2, em andamento):** ainda não implementada. Decisões sobre biblioteca (`djangorestframework-simplejwt`), tempo de vida de access/refresh tokens e `permission_classes` por rota serão registradas aqui assim que definidas.

---

*Última atualização: Sprint 2 em andamento (período 28/09–11/10/2026). Próxima revisão prevista após a implementação de JWT.*
