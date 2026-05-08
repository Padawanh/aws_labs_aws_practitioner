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
