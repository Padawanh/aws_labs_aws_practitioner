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
