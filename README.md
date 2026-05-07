# Plano de Laboratórios Práticos – AWS Certified Cloud Practitioner (CLF‑C02)

Sequência de laboratórios práticos para um grupo de estudo que está se preparando para o exame **AWS Certified Cloud Practitioner (CLF‑C02)**.  
Os labs foram pensados para cobrir, de forma prática, a maior parte dos domínios do exame, usando recursos simples (muitos dentro do Free Tier).

---

## Visão geral dos laboratórios

- **Lab 0 – Preparação de conta e boas práticas básicas**
- **Lab 1 – Aplicação web simples em EC2 + S3**
- **Lab 2 – Versão serverless da mesma API (API Gateway + Lambda + S3)**
- **Lab 3 – Observabilidade, logs e segurança**
- **Lab 4 – Custos, modelos de preço e otimização**
- **Lab 5 – Integração assíncrona (SNS, SQS, EventBridge)**

Cada lab pode ser feito em 1–2 horas de estudo em grupo.

---

## Lab 0 – Preparação de conta e boas práticas básicas

**Objetivo:**  
Praticar conceitos de responsabilidade compartilhada, IAM básico, segurança da conta e noções de billing/custos.

### Atividades

1. **Organização da conta AWS do laboratório**
   - Decidir se o grupo usará:
     - Contas individuais (cada participante com sua própria conta Free Tier); ou
     - Uma conta “mãe” com subcontas via AWS Organizations (mesmo que apenas conceitual).
   - Discutir:
     - O que é responsabilidade da AWS (segurança da nuvem: datacenter, hardware, etc.).
     - O que é responsabilidade do cliente (segurança na nuvem: usuários, permissões, dados, etc.).

2. **Proteger o usuário root**
   - Ativar **MFA** no usuário root.
   - Guardar as credenciais do root em local seguro (e combinar que não será usado no dia a dia).
   - Criar um **usuário administrativo IAM** para uso diário, seguindo o princípio do menor privilégio.

3. **Criar grupos e usuários IAM**
   - Criar um grupo `Lab-Admins` com a política gerenciada `AdministratorAccess`.
   - Criar um grupo `Lab-ReadOnly` com a política gerenciada `ReadOnlyAccess`.
   - Criar 1 usuário por participante e atribuir a um dos grupos.
   - Testar na prática:
     - Usuário admin consegue criar EC2, S3 etc.
     - Usuário read‑only consegue apenas visualizar recursos.

4. **Configurar alertas de custo**
   - Habilitar **Cost Explorer**.
   - Criar um **AWS Budget** simples (por exemplo, USD 5/mês) com alerta por e‑mail.
   - Abrir a **AWS Pricing Calculator** e estimar o custo de:
     - Uma instância EC2 pequena (t2.micro/t3.micro).
     - Um bucket S3 com poucos GB.

### Domínios do exame reforçados

- **Domínio 2 – Segurança e conformidade**
  - Modelo de responsabilidade compartilhada.
  - IAM, princípio do menor privilégio, proteção da conta root.
- **Domínio 4 – Cobrança, preços e suporte**
  - Budgets, Cost Explorer, noções de preços.

---

## Lab 1 – Aplicação web simples em EC2 + S3

**Objetivo:**  
Praticar computação (EC2), rede básica (VPC, Security Groups), armazenamento (S3) e IAM (roles).

**Cenário:**  
Criar uma **API simples** em uma instância EC2 que lê e grava arquivos em um bucket S3.

### Atividades

1. **VPC e segurança básica**
   - Usar a **VPC default** (para simplificar) ou criar uma VPC simples com:
     - 1 subnet pública.
     - Internet Gateway.
   - Criar um **Security Group**:
     - Permitir HTTP (porta 80) de `0.0.0.0/0` (ou apenas do IP do aluno).
     - Permitir SSH (porta 22) apenas do IP do aluno.

2. **Criar a instância EC2**
   - Tipo: `t2.micro` ou `t3.micro` (Free Tier).
   - AMI: Amazon Linux 2 (ou similar).
   - Associar a instância ao Security Group criado.
   - Conectar via SSH (ou via Session Manager, se quiserem explorar o Systems Manager).

3. **Instalar uma API simples**
   - Na instância, instalar um servidor web simples, por exemplo:
     - Python + Flask, ou
     - Node.js + Express.
   - Criar uma API com endpoints como:
     - `GET /files` – lista objetos de um bucket S3.
     - `POST /files` – faz upload de um texto simples para o S3.
   - O código pode ser bem simples; o foco é entender o fluxo EC2 → S3.

4. **Criar bucket S3**
   - Criar um bucket com nome único (por exemplo, `lab-ec2-s3-grupoX`).
   - Habilitar **versionamento** (para discutir depois).
   - Manter o bucket **sem acesso público** (acesso apenas via API/SDK).

5. **Configurar IAM Role para EC2**
   - Criar uma **IAM Role** para EC2 com política mínima:
     - `s3:ListBucket` no bucket.
     - `s3:PutObject` no bucket.
   - Anexar a Role à instância EC2.
   - Testar a API:
     - `GET /files` deve listar o conteúdo do bucket.
     - `POST /files` deve criar um objeto no bucket.

6. **Alta disponibilidade conceitual (opcional)**
   - Discutir: se essa instância cair, o que acontece?
   - Criar um **Auto Scaling Group (ASG)** mínimo com 1–2 instâncias.
   - Criar um **Application Load Balancer (ALB)**:
     - Criar um Target Group apontando para as instâncias do ASG.
     - Configurar o ALB para encaminhar tráfego HTTP para o Target Group.
   - Acessar a API via DNS do ALB (em vez de IP da instância).

### Domínios do exame reforçados

- **Domínio 3 – Tecnologia e serviços da nuvem**
  - EC2, VPC, Security Groups, S3, Auto Scaling, Load Balancer.
- **Domínio 2 – Segurança e conformidade**
  - IAM Roles, princípio de menor privilégio.

---

## Lab 2 – Versão serverless da mesma API (API Gateway + Lambda + S3)

**Objetivo:**  
Comparar EC2 vs serverless, reforçar responsabilidade compartilhada, elasticidade e modelo de custos.

**Cenário:**  
Reimplementar a mesma API do Lab 1 usando **API Gateway + Lambda + S3**, sem gerenciar servidores.

### Atividades

1. **Bucket S3**
   - Reutilizar o bucket do Lab 1 ou criar um novo.
   - Manter sem acesso público direto.

2. **Criar função Lambda**
   - Escolher um runtime simples (Python, Node.js, etc.).
   - Implementar dois handlers:
     - `list_files` – lista objetos no bucket.
     - `upload_file` – grava um objeto simples (por exemplo, texto enviado no corpo da requisição).
   - Criar uma **IAM Role para Lambda** com permissões mínimas no bucket:
     - `s3:ListBucket`, `s3:GetObject`, `s3:PutObject`.

3. **Criar API REST com Amazon API Gateway**
   - Criar uma API REST.
   - Definir endpoints:
     - `GET /files` → integra com Lambda `list_files`.
     - `POST /files` → integra com Lambda `upload_file`.
   - Habilitar CORS se forem testar via navegador.
   - Fazer deploy em um stage (por exemplo, `dev`).

4. **Testar a API**
   - Usar o console do API Gateway, `curl` ou Postman para chamar:
     - `GET /files`
     - `POST /files`
   - Conferir se os objetos aparecem no S3.

5. **Comparar com a solução em EC2 (discussão em grupo)**
   - Quem gerencia o sistema operacional em cada caso?
   - Como funciona a elasticidade:
     - Auto Scaling (EC2) vs escalabilidade automática do Lambda.
   - Modelo de cobrança:
     - EC2: por hora (ou segundo) de instância.
     - Lambda: por invocação e tempo de execução.
   - Em que cenário cada abordagem faz mais sentido?

### Domínios do exame reforçados

- **Domínio 3 – Tecnologia e serviços da nuvem**
  - Lambda, API Gateway, S3, IAM.
- **Domínio 1 – Conceitos da nuvem**
  - Benefícios da nuvem, elasticidade, agilidade.
- **Domínio 4 – Cobrança, preços e suporte**
  - Comparação de modelos de custo (EC2 vs Lambda).

---

## Lab 3 – Observabilidade, logs e segurança

**Objetivo:**  
Mostrar como monitorar, auditar e aumentar a segurança do ambiente.

### Atividades

1. **CloudWatch Logs**
   - Garantir que a função Lambda do Lab 2 esteja enviando logs para **CloudWatch Logs** (isso é padrão).
   - Gerar algumas chamadas na API.
   - Navegar até os log groups e streams para ver:
     - Logs de sucesso.
     - Logs de erro (forçar algum erro propositalmente).

2. **CloudWatch Metrics e Alarms**
   - No API Gateway ou Lambda, observar as métricas (invocações, erros, latência).
   - Criar um **alarme do CloudWatch**:
     - Exemplo: se a métrica `5XXError` do API Gateway for maior que 1 em 5 minutos.
   - Configurar o alarme para enviar notificação via **SNS** (e‑mail).

3. **CloudTrail**
   - Verificar se o **AWS CloudTrail** está habilitado.
   - Executar algumas ações no console (por exemplo, criar/deletar um recurso simples).
   - No CloudTrail:
     - Localizar os eventos correspondentes.
     - Ver quem executou (usuário/role), de onde e quando.
   - Discutir:
     - Diferença entre **CloudWatch** (monitoramento operacional) e **CloudTrail** (auditoria de chamadas de API).

4. **Trusted Advisor e Security Hub (visão geral)**
   - Acessar o **AWS Trusted Advisor**:
     - Ver recomendações básicas (MFA no root, portas abertas, etc.).
   - Opcional: habilitar **AWS Security Hub** em modo de avaliação e ver alguns findings (se o grupo quiser ir além).

### Domínios do exame reforçados

- **Domínio 2 – Segurança e conformidade**
  - Logs, auditoria, governança, serviços de segurança.
- **Domínio 3 – Tecnologia e serviços da nuvem**
  - CloudWatch, CloudTrail, Trusted Advisor.

---

## Lab 4 – Custos, modelos de preço e otimização

**Objetivo:**  
Conectar a arquitetura criada nos labs anteriores com os conceitos de cobrança, preços e otimização de custos.

### Atividades

1. **Explorar Cost Explorer**
   - Após alguns dias de uso dos labs, abrir o **AWS Cost Explorer**.
   - Ver:
     - Quais serviços estão gerando custo (S3, EC2, Lambda, API Gateway, etc.).
     - Custo por serviço, por região e por período.

2. **Tags de alocação de custos**
   - Definir uma convenção de tags, por exemplo:
     - `Project=StudyGroup`
     - `Env=Lab`
   - Aplicar tags em:
     - EC2, S3, Lambda, API Gateway, etc.
   - Ver como essas tags aparecem nos relatórios de custo (Cost Explorer / Cost and Usage Reports).

3. **Comparar modelos de compra de computação**
   - Usar a **AWS Pricing Calculator** para simular:
     - EC2 On‑Demand vs Reserved Instances vs Savings Plans.
     - Armazenamento S3 Standard vs S3 Standard‑IA vs S3 Glacier.
   - Discutir:
     - Quando faz sentido usar instância reservada?
     - Quando usar classes de armazenamento mais baratas (e com quais trade‑offs)?

4. **Planos de suporte da AWS**
   - Ler a descrição dos planos de suporte:
     - Basic, Developer, Business, Enterprise On‑Ramp, Enterprise.
   - Discutir:
     - Qual plano faz sentido para um pequeno projeto/lab?
     - Diferenças de SLA e tipos de suporte (e‑mail, telefone, TAM, etc.).

### Domínios do exame reforçados

- **Domínio 4 – Cobrança, preços e suporte**
  - Modelos de preços, orçamentos, tags de custo, planos de suporte.
- **Domínio 1 – Conceitos da nuvem**
  - Aspectos econômicos da nuvem, custo variável vs fixo.

---

## Lab 5 – Integração assíncrona (SNS, SQS, EventBridge)

**Objetivo:**  
Praticar serviços de integração de aplicações e arquitetura orientada a eventos.

**Cenário:**  
Quando um arquivo é enviado para o S3, um processamento assíncrono é disparado via SNS/SQS/Lambda.

### Atividades

1. **Evento S3 → SNS**
   - No bucket S3 (dos labs anteriores ou um novo):
     - Configurar um **evento de criação de objeto** (`PUT`) para publicar em um **SNS Topic**.
   - Criar um tópico SNS (por exemplo, `lab-s3-events`).
   - Criar uma assinatura de e‑mail:
     - Confirmar a inscrição.
     - Fazer upload de um arquivo no S3 e verificar se o e‑mail é recebido.

2. **SNS → SQS**
   - Criar uma fila **SQS** (por exemplo, `lab-s3-queue`).
   - Configurar o tópico SNS para publicar mensagens nessa fila.
   - Fazer upload de arquivos no S3 e verificar se as mensagens aparecem na fila.

3. **SQS → Lambda (processamento assíncrono)**
   - Criar uma **função Lambda** que:
     - Seja disparada por eventos da fila SQS.
     - Leia a mensagem e escreva um log no CloudWatch (por exemplo, nome do arquivo enviado).
   - Testar o fluxo completo:
     - Upload no S3 → evento no SNS → mensagem na SQS → Lambda processa.

4. **EventBridge (opcional)**
   - Criar uma regra no **Amazon EventBridge**:
     - Disparar uma Lambda em um horário específico (cron) ou
     - Reagir a um evento de outro serviço (por exemplo, mudança de estado de instância EC2).
   - Discutir:
     - Diferença entre SNS (pub/sub), SQS (fila) e EventBridge (event bus).

### Domínios do exame reforçados

- **Domínio 3 – Tecnologia e serviços da nuvem**
  - Serviços de integração de aplicações: SNS, SQS, EventBridge.
- **Domínio 1 – Conceitos da nuvem**
  - Arquiteturas desacopladas, escalabilidade, resiliência.

---

## Sugestão de uso no grupo de estudo

Para cada encontro do grupo:

1. **10–15 minutos – Revisão teórica**
   - Ver no blueprint do exame (guia oficial) quais domínios e tarefas o lab cobre.
   - Relacionar os serviços usados com as seções:
     - Domínio 1: Conceitos da nuvem.
     - Domínio 2: Segurança e conformidade.
     - Domínio 3: Tecnologia e serviços.
     - Domínio 4: Cobrança, preços e suporte.

2. **45–60 minutos – Mão na massa (lab)**
   - Fazer o lab em dupla ou trio.
   - Um participante compartilha a tela e os outros ajudam.

3. **15–20 minutos – Discussão**
   - Quais serviços apareceram?
   - Como isso poderia ser cobrado em uma questão teórica?
   - Quais boas práticas de segurança e custo foram aplicadas?

---

## Próximos passos

Se quiserem aprofundar, vocês podem:

- Criar uma **“apostila” detalhada** para cada lab, com:
  - Passo a passo com prints de tela.
  - Comandos exatos (por exemplo, para instalar a API em EC2).
  - Espaço para anotações dos participantes.
- Transformar alguns labs em **desafios**:
  - Entregar apenas o objetivo (ex.: “crie uma API serverless que salve dados no S3”) e deixar o grupo decidir quais serviços usar.
