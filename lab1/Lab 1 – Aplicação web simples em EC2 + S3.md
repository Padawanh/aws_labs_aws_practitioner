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
     - Python + Flask
   - Criar uma API com endpoints como:
     - `GET /files` – lista objetos de um bucket S3.
     - `POST /files` – faz upload de um texto simples para o S3.
   - O código pode ser bem simples; o foco é entender o fluxo EC2 → S3.

### Implementação da API (código pronto)

Código criado na pasta `lab1/api`:

- `app.py`: API Flask com endpoints:
  - `GET /health` – health check.
  - `GET /files` – lista objetos do bucket S3.
  - `POST /files` – envia texto para o S3.
- `requirements.txt`: dependências (`Flask` e `boto3`).

Formato esperado no `POST /files`:

```json
{
  "filename": "meu-arquivo.txt",
  "content": "texto para salvar no S3"
}
```

Se `filename` não for enviado, a API gera um nome automático.

### Como executar na EC2

1. Acesse a instância via SSH.
2. Na EC2 (Amazon Linux 2), instale Python e crie o ambiente virtual:

```bash
sudo yum update -y
sudo yum install -y python3

cd ~/aws_labs_aws_practitioner/lab1/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Defina variáveis de ambiente e inicie a API:

```bash
export BUCKET_NAME="SEU_BUCKET_UNICO"
export AWS_REGION="us-east-1"
python app.py
```

A API sobe em `0.0.0.0:5000`.

### O que precisa estar pronto na AWS (infra manual)

- EC2 com Role IAM anexada contendo no mínimo:
  - `s3:ListBucket` no bucket.
  - `s3:PutObject` no bucket (ARN com `/*` para objetos).
- Bucket S3 já criado e sem acesso público.
- Security Group da EC2 com entrada liberada para `TCP 5000` a partir do IP da sua máquina local (ou faixa permitida no seu cenário de aula).

### Como testar do seu computador local

Use o IP público da EC2 no lugar de `<EC2_PUBLIC_IP>`.

#### Teste com curl

```bash
curl http://<EC2_PUBLIC_IP>:5000/health

curl http://<EC2_PUBLIC_IP>:5000/files

curl -X POST http://<EC2_PUBLIC_IP>:5000/files \
  -H "Content-Type: application/json" \
  -d '{"filename":"teste.txt","content":"ola do meu computador"}'

curl http://<EC2_PUBLIC_IP>:5000/files
```

#### Teste com PowerShell (Windows)

```powershell
Invoke-RestMethod -Method Get -Uri "http://<EC2_PUBLIC_IP>:5000/health"

Invoke-RestMethod -Method Get -Uri "http://<EC2_PUBLIC_IP>:5000/files"

$body = @{
  filename = "teste-powershell.txt"
  content  = "ola via PowerShell"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://<EC2_PUBLIC_IP>:5000/files" -ContentType "application/json" -Body $body

Invoke-RestMethod -Method Get -Uri "http://<EC2_PUBLIC_IP>:5000/files"
```

### Observações rápidas

- Esta implementação é propositalmente simples para fins didáticos.
- Em produção, usar servidor WSGI (ex.: Gunicorn), TLS e endpoint atrás de ALB.

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