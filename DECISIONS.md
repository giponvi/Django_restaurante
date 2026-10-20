# DECISIONS.md — Sistema de Gestão para Comércio/Restaurante

Registro de decisões arquiteturais e de implementação. Cada entrada documenta contexto, decisão, alternativas e consequências. **Implementado**, **decidido, não implementado** e **pendente** são estados diferentes.

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
**Alternativas consideradas:** stack AWS completa (EC2, RDS) — descartado por exigir mais tempo de configuração de infraestrutura sem ganho proporcional de aprendizado para o nível júnior-alvo.
**Consequências:** CI/CD mais simples; menor exposição a conceitos de infraestrutura AWS além do S3 básico.

### ADR-004 — UPX mantido como MVP mínimo, sem expansão ativa
**Contexto:** projeto acadêmico paralelo em Java 17/Spring Boot/JPA, majoritariamente gerado com apoio de IA. Dúvida inicial sobre recriar todo o roadmap em Java após concluir as 10 sprints em Python.
**Decisão:** não investir tempo ativo aprofundando o UPX. Escopo fechado como MVP mínimo: cadastro de usuários, resolução de questões com validação simples, Java puro + MySQL + HTML/CSS.
**Alternativas consideradas:** repetir as 10 sprints completas em Java/Spring — descartado (ver ADR-001).
**Consequências:** antes de expor no GitHub como peça de portfólio, é necessária uma passada de leitura ativa do código gerado, para conseguir defender as decisões de arquitetura (ex.: uso de DTOs, camada de serviço) em entrevista técnica. Prazo de entrega: semana de 16/11/2026 (grade acadêmica).

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
**Consequências:** o campo é protegido de alterações diretas pela API via serializer. **Limitação descoberta após a implementação:** um PATCH que troca o campo `produto` não recalcula o preço, podendo gerar combinação inconsistente produto/preço. Exige decisão e teste específicos; `read_only_fields` não substitui a validação dessa regra.

### ADR-009 — Nomenclatura de rotas em snake_case (`itens_pedido`)
**Contexto:** a rota inicial estava registrada como `itemPedido` (camelCase), inconsistente com o padrão das demais rotas (`categorias`, `produtos`, `pedidos`).
**Decisão:** padronização para `itens_pedido`, seguindo convenção REST comum (plural, snake_case), igual ao padrão já usado no projeto To-Do paralelo.
**Alternativas consideradas:** manter camelCase — descartado por quebrar consistência com o restante da API.
**Consequências:** nenhuma funcional; apenas consistência e legibilidade da API para quem for consumi-la.

### ADR-010 — JWT e matriz de permissões da API
**Estado:** IMPLEMENTADO; verificado manualmente com Thunder Client.
**Contexto:** proteger operações de modificação do cardápio e consultas/alterações de pedidos sem exigir login para consultar o cardápio.
**Decisão:** usar `djangorestframework-simplejwt`, `JWTAuthentication` e a permissão global `IsAuthenticated` em `setup/settings.py`; expor `/api/token/` e `/api/token/refresh/`. `CategoriaViewSet` e `ProdutoViewSet` usam a classe personalizada `IsAdminOrReadOnly` (`BasePermission`, `SAFE_METHODS`, `request.user.is_authenticated` e `request.user.is_staff`). `PedidoViewSet` e `ItemPedidoViewSet` herdam `IsAuthenticated` globalmente.

| Recursos | Consulta | Criação | Alteração/exclusão |
| --- | --- | --- | --- |
| Categorias e produtos | Público | `is_staff=True` autenticado | `is_staff=True` autenticado |
| Pedidos e itens | Autenticado | Autenticado | Autenticado |

**Alternativas consideradas:** uso direto de `IsAdminUser` em toda a view (bloquearia leitura pública); regras distintas com `get_permissions()` / `self.action`; grupos explícitos de garçons (adiados).
**Consequências:** implementação enxuta. `IsAuthenticated` **não** distingue garçons de clientes ou atribui posse de pedidos. `is_staff` é membro da equipe, não exclusivamente superusuário. `permission_classes` na view substitui a lista global daquela view.
**Evidências:** GET público de produtos `200`, POST anônimo `401`, POST administrativo `201`, POST comum `403`, PATCH/DELETE comum `403`, PATCH administrativo `200`; GET anônimo de pedidos `401`, GET comum `200`; testes adicionais de pedidos, itens, preços e exclusões foram executados manualmente. Não há suíte automatizada correspondente.
**Pendências:** confirmar políticas de validade/rotação dos tokens antes de produção; não afirmar que o refresh customizado está implementado só porque a rota existe.

### ADR-011 — Preservação do histórico e indisponibilidade de produtos
**Estado:** DECISÃO CONCEITUAL TOMADA; NÃO IMPLEMENTADA.
**Contexto:** `Produto.categoria` e `ItemPedido.produto` usam `CASCADE`. Os testes mostraram que apagar categoria associada pode remover produtos e itens de pedidos históricos. `preco_congelado` por si só não preserva todos os dados de um item excluído.
**Decisão conceitual:** preservar pedidos históricos. Preferir retirar o produto de venda via `Produto.disponivel=False`, combinado com proteção contra exclusão física de produtos referenciados por itens (`on_delete=PROTECT` em `ItemPedido.produto`, sujeito a revisão das migrações e caminhos de exclusão). Rejeitar criação de novos itens com produtos indisponíveis no backend, incluindo substituição de produto por PATCH; interface futura poderá ocultar produtos indisponíveis, mas não é barreira de segurança.
**Alternativas consideradas:** manter `CASCADE`; `SET_NULL` com dados históricos independentes; snapshots do nome/preço do produto; exclusão lógica de produto.
**Consequências e pontos abertos:** definir regras para editar pedidos antigos, alterar produto e preço congelado, cancelar pedidos e excluir categorias. `PROTECT` impede apagar produto referenciado, mas não substitui validação de disponibilidade. Considerar snapshot histórico do nome do produto e regras de auditoria para documentos comerciais. Não houve alterações nos models para essa decisão até a revisão de 10/10/2026.


## Camada de Código — Fase pré-Sprint 3 (higiene e configuração)

### ADR-012 — Segredos e configuração via variáveis de ambiente (`django-environ`)
**Estado:** IMPLEMENTADO para `SECRET_KEY` e `DEBUG`. `ALLOWED_HOSTS`, banco e demais configurações continuam fixos no código.
**Contexto:** a `SECRET_KEY` estava escrita em `setup/settings.py` e versionada no GitHub. A mesma chave assina sessões e, no padrão do Simple JWT, os tokens de autenticação.
**Decisão:** ler `SECRET_KEY` e `DEBUG` de um arquivo `.env` com `django-environ`. `SECRET_KEY` não tem valor padrão (se faltar, o Django falha ao iniciar com `ImproperlyConfigured`). `DEBUG` usa casting `bool` com padrão `False`. O `.env` fica fora do Git; o `.env.example`, com os nomes das variáveis e valores fictícios, é versionado para documentar o que precisa ser configurado. Uma chave nova foi gerada e a anterior foi aposentada.
**Alternativas consideradas:** `os.environ` puro (também falha alto, mas não lê o `.env` sozinho nem faz casting); `os.getenv` (devolve `None` ou exige um valor padrão, o que mascara a configuração ausente ou convida a deixar uma chave reserva no código); `python-dotenv` (carrega o `.env`, mas sem casting e sem tratamento de URLs de banco e cache).
**Consequências:** o projeto não sobe sem o `.env`, e o erro aponta a variável ausente. Sessões e tokens emitidos com a chave antiga deixaram de valer (novo login necessário). A chave antiga continua no histórico do Git, mas está aposentada e era a chave `django-insecure` gerada pelo `startproject`. O `django-environ` já está pronto para ler `DATABASE_URL` (PostgreSQL em produção) e `CACHE_URL` (Redis, Sprint 3). Com `DEBUG=False` e `ALLOWED_HOSTS` vazio o Django recusa as requisições (erro 400), por isso o `.env` local define `DEBUG=True`. O `.env.example` deve ser atualizado sempre que surgir uma variável nova.
**Pendências:** ler `ALLOWED_HOSTS` do ambiente; definir como a configuração será fornecida no deploy (Render/Railway).

### ADR-013 — Artefatos locais e gerados fora do versionamento
**Estado:** IMPLEMENTADO.
**Contexto:** o repositório continha o `db.sqlite3` (usuários de teste com hashes de senha e dados de teste, alterado a cada execução) e as pastas `__pycache__` com 15 arquivos `.pyc`, que mudavam a cada execução e poluíam os commits.
**Decisão:** `db.sqlite3`, `.env`, `__pycache__/` e `*.pyc` ficam no `.gitignore`. Os arquivos que já estavam versionados foram retirados do índice do Git (`git rm --cached`) e continuam no disco. As migrations continuam versionadas.
**Alternativas consideradas:** versionar o banco de desenvolvimento (rejeitado: contém dados de usuários, gera conflitos e incha o histórico).
**Consequências:** quem clonar o projeto precisa criar o banco (`migrate`) e um superusuário, e passa a ser necessário um script ou fixtures com dados de exemplo, alinhado à população sintética planejada para testes e BI. Versões antigas desses arquivos permanecem no histórico (aceitável para um banco de estudo; as senhas de teste não devem ser reutilizadas). O `.gitignore` precisa estar em UTF-8: em UTF-16 o Git ignora as regras sem avisar, o que apareceu aqui como `.env` listado entre os arquivos não rastreados.

### ADR-014 — Restabelecer a configuração `MAILERS` no início da Sprint 3
**Estado:** DECIDIDO; NÃO IMPLEMENTADO.
**Contexto:** o `settings.py` gerado pelo `startproject` do Django 6.1 inclui `MAILERS` (backend de e-mail que imprime no console em desenvolvimento), que substitui o `EMAIL_BACKEND` clássico. O bloco foi removido por engano durante uma limpeza, sob a suposição de que não era uma configuração válida; a documentação oficial do Django 6.1 (guia de migração para mailers) confirma que é.
**Decisão:** restaurar o bloco padrão no início da Sprint 3.
**Consequências:** o projeto ainda não envia e-mail, então não há impacto funcional hoje; a restauração evita depender do comportamento antigo. Se um dia houver um provedor real de e-mail, as credenciais devem vir de variáveis de ambiente (ADR-012).

---

## Pendências e melhorias propostas — sem implementação nesta revisão

### Prioridade alta / antes de qualquer ambiente público
1. **Segredos e configuração (parcialmente resolvido, ver ADR-012):** `SECRET_KEY` e `DEBUG` agora vêm do ambiente. Pendentes: ler `ALLOWED_HOSTS` (e, em produção, o banco) de variáveis de ambiente; definir como a configuração será fornecida no deploy; manter `DEBUG=False` fora do desenvolvimento; evitar versionar tokens e bancos de teste com dados privados.
2. **Histórico do pedido:** aplicar e testar ADR-011 com migrações seguras, considerando as exclusões em cascata que partem de Categoria e Produto.
3. **Disponibilidade:** validação server-side nos serializers/serviços para bloquear `POST` de produto indisponível e `PATCH` que troca o produto para um indisponível. Avaliar a semântica de alteração de itens históricos.
4. **Preço congelado:** decidir se a troca do `produto` de um ItemPedido existente será proibida ou terá tratamento especial de preço. Testar PATCH, PUT e criação.
5. **Validação de quantidade e preço:** impedir `quantidade<=0`, revisar regras para `preco` não negativo e consistência de status; não presumir que o campo `IntegerField` aplica sozinho a regra comercial.

### Qualidade e evolução
6. Criar testes automatizados (autenticação, acessos permitidos/negados, validações, cascatas/PROTECT, regressão de preço e indisponibilidade). O arquivo `cardapio/tests.py` permanece essencialmente vazio.
7. Distinguir garçom de qualquer autenticado (grupos/perfis) e, se o escopo exigir, vincular `Pedido` a usuário; hoje `nome_cliente` é apenas texto e `Pedido.objects.all()` retorna todos aos autenticados.
8. API do cardápio: decidir se leituras públicas retornam apenas produtos disponíveis e categorias ativas; oferecer consulta administrativa separada quando conveniente.
9. Rever endpoints que permitem operações destrutivas e considerar exclusão lógica/status/cancelamento; documentar regras para notas e histórico sem presumir requisitos legais específicos.
10. Atualizar documentação após mudanças de código, comparar SHA/commit ao revisar pelo conector GitHub; indexação pode não refletir imediatamente o último commit.
11. Manter população de dados sintéticos para testes e futuro BI; decidir fonte e metodologia antes do pipeline de dados.

## Fechamento da Sprint 2
**Estado em 10/10/2026:** escopo de CRUD/DRF, JWT e permissões concluído e **validado manualmente**, conforme registros e capturas no Thunder Client; **não é certificação de produção**. ADR-011 e itens de melhoria listados acima ficam para planejamento e implementação posterior. Próxima sprint e cronograma devem ser confirmados com o backlog original (mantido fora deste documento).
