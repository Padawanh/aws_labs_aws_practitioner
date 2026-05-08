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
