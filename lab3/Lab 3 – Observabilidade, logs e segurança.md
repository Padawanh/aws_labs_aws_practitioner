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
