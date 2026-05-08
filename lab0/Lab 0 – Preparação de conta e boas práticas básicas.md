## Lab 0 – Preparação de conta e boas práticas básicas

**Objetivo:**  
Praticar conceitos de responsabilidade compartilhada, IAM básico, segurança da conta e noções de billing/custos.

### Atividades

1. **Organização da conta AWS do laboratório**
   - Decidir se o grupo usará:
     - Contas individuais (cada participante com sua própria conta Free Tier); ou
     - Uma conta "mãe" com subcontas via AWS Organizations (mesmo que apenas conceitual).
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
