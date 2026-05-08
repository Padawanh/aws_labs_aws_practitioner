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