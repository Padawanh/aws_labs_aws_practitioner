## Lab 1 – Aplicação web simples em EC2 + S3

**Objetivo:**  
Praticar computação (EC2), rede básica (VPC, Security Groups), armazenamento (S3) e IAM (roles).

**Cenário:**  
Criar uma **API simples** em uma instância EC2 que lê e grava arquivos em um bucket S3.

---

## Visão geral das atividades

1. VPC e segurança básica
2. Criar a instância EC2
3. Criar o bucket S3
4. Configurar IAM Role para EC2
5. Sobre o código da API
6. Subir a API na EC2
7. Testar do seu computador local
8. Alta disponibilidade conceitual *(opcional)*

---

## Passo a passo

### 1. VPC e segurança básica

- Usar a **VPC default** (para simplificar) ou criar uma VPC simples com:
  - 1 subnet pública.
  - Internet Gateway.
- Criar um **Security Group** com as seguintes regras de entrada:
  - SSH (porta 22) apenas do seu IP.
  - Custom TCP (porta 5000) apenas do seu IP.
    > Para descobrir seu IP público: acesse [https://checkip.amazonaws.com](https://checkip.amazonaws.com)

---

### 2. Criar a instância EC2

- **Tipo**: `t2.micro` ou `t3.micro` (Free Tier).
- **AMI**: Amazon Linux 2 (ou similar).
- Associar ao Security Group criado no passo anterior.
- Conectar via SSH após a criação.

---

### 3. Criar o bucket S3

1. Vá em **S3 → Create bucket**.
2. **Bucket name**: use um nome único global (ex.: `lab-ec2-s3-seunome-2026`).
3. **Região**: escolha a **mesma região** da sua EC2 (ex.: `us-east-1`).
4. **Object Ownership**: deixe ACLs desabilitadas (padrão).
5. **Block Public Access**: mantenha **tudo bloqueado**.
6. **Bucket Versioning**: clique em **Enable**.
7. Clique em **Create bucket**.

> Guarde o nome exato do bucket — você vai usá-lo mais à frente.

---

### 4. Configurar IAM Role para EC2

#### 4a. Criar a IAM Policy mínima

1. Vá em **IAM → Policies → Create policy**.
2. Clique na aba **JSON** e cole o conteúdo abaixo, substituindo `NOME_DO_BUCKET`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListBucket",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::NOME_DO_BUCKET"
    },
    {
      "Sid": "PutObject",
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::NOME_DO_BUCKET/*"
    }
  ]
}
```

> O ARN do `ListBucket` aponta para o bucket (sem `/`); o do `PutObject` aponta para objetos dentro dele (com `/*`). Invertê-los gera `AccessDenied`.

3. Dê o nome `policy-lab1-s3` e clique em **Create policy**.

#### 4b. Criar a IAM Role

1. Vá em **IAM → Roles → Create role**.
2. **Trusted entity**: AWS service → **EC2**. Clique em **Next**.
3. Busque e selecione `policy-lab1-s3`. Clique em **Next**.
4. **Role name**: `role-ec2-lab1-s3`. Clique em **Create role**.

#### 4c. Anexar a Role na instância

1. Vá em **EC2 → Instances** e selecione sua instância.
2. **Actions → Security → Modify IAM role**.
3. Selecione `role-ec2-lab1-s3` e clique em **Update IAM role**.
4. Aguarde ~1 minuto para propagação.

---

### 5. Sobre o código da API

O código já está pronto na pasta `lab1/api`:

- **`app.py`** – API Flask com três endpoints:
  - `GET /health` – health check.
  - `GET /files` – lista objetos do bucket S3.
  - `POST /files` – envia texto para o S3.
- **`requirements.txt`** – dependências (`Flask` e `boto3`).

Formato do corpo esperado no `POST /files`:

```json
{
  "filename": "meu-arquivo.txt",
  "content": "texto para salvar no S3"
}
```

Se `filename` não for enviado, a API gera um nome automático com timestamp.

---

### 6. Subir a API na EC2

Conecte-se via SSH e execute:

```bash
# Atualiza pacotes e instala Python 3
sudo yum update -y
sudo yum install -y python3

# Navega até a pasta da API
cd ~/aws_labs_aws_practitioner/lab1/api

# Cria e ativa o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instala as dependências
pip install -r requirements.txt

# Define as variáveis de ambiente (substitua pelo nome real do bucket)
export BUCKET_NAME="NOME_DO_BUCKET"
export AWS_REGION="us-east-1"

# Inicia a API
python app.py
```

Se aparecer `Running on http://0.0.0.0:5000`, a API está no ar.

**Valide localmente antes de testar do seu PC** (em outro terminal SSH):

```bash
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/files
```

- Falha aqui → problema na aplicação ou dependências.
- Funciona aqui mas não do seu PC → problema no Security Group.

---

### 7. Testar do seu computador local

Substitua `<EC2_PUBLIC_IP>` pelo **IPv4 público** da instância (visível no Console EC2).

#### curl (Linux / macOS / Git Bash)

```bash
# Health check
curl http://<EC2_PUBLIC_IP>:5000/health

# Listar arquivos no bucket
curl http://<EC2_PUBLIC_IP>:5000/files

# Fazer upload de um arquivo
curl -X POST http://<EC2_PUBLIC_IP>:5000/files \
  -H "Content-Type: application/json" \
  -d '{"filename":"teste.txt","content":"ola do meu computador"}'

# Confirmar que o arquivo aparece na listagem
curl http://<EC2_PUBLIC_IP>:5000/files
```

#### PowerShell (Windows)

```powershell
# Health check
Invoke-RestMethod -Method Get -Uri "http://<EC2_PUBLIC_IP>:5000/health"

# Listar arquivos no bucket
Invoke-RestMethod -Method Get -Uri "http://<EC2_PUBLIC_IP>:5000/files"

# Fazer upload de um arquivo
$body = @{ filename = "teste-ps.txt"; content = "ola via PowerShell" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://<EC2_PUBLIC_IP>:5000/files" `
  -ContentType "application/json" -Body $body

# Confirmar que o arquivo aparece na listagem
Invoke-RestMethod -Method Get -Uri "http://<EC2_PUBLIC_IP>:5000/files"
```

#### Erros comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `AccessDenied` em `GET /files` | ARN do `ListBucket` com `/*` | Remova o `/*` do ARN do bucket |
| `AccessDenied` em `POST /files` | ARN do `PutObject` sem `/*` | Adicione `/*` ao ARN dos objetos |
| `Connection refused` / timeout | Porta 5000 não liberada no SG | Adicione inbound rule TCP 5000 com seu IP |
| `EndpointConnectionError` | `AWS_REGION` incorreto | Confirme que bucket e EC2 estão na mesma região |
| Funciona na EC2, não do PC | `app.run` sem `0.0.0.0` | Verifique `host="0.0.0.0"` no `app.py` |
| Sem credenciais na EC2 | Role não anexada | Refaça o passo 4c e aguarde 1–2 min |

> Esta implementação é propositalmente simples para fins didáticos. Em produção: usar Gunicorn, TLS e ALB.

---

### 8. Alta disponibilidade conceitual *(opcional)*

- Discutir: se essa instância cair, o que acontece?
- Criar um **Auto Scaling Group (ASG)** mínimo com 1–2 instâncias.
- Criar um **Application Load Balancer (ALB)**:
  - Criar um Target Group apontando para as instâncias do ASG.
  - Configurar o ALB para encaminhar tráfego HTTP para o Target Group.
- Acessar a API via DNS do ALB (em vez do IP da instância).

---

## Domínios do exame reforçados

- **Domínio 3 – Tecnologia e serviços da nuvem**
  - EC2, VPC, Security Groups, S3, Auto Scaling, Load Balancer.
- **Domínio 2 – Segurança e conformidade**
  - IAM Roles, princípio de menor privilégio.