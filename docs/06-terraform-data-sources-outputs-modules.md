# 🚀 Módulo 03 — Terraform: Data Sources, Outputs, Variables e Modules

> Guia melhorado para estudar Terraform com foco em **entender o porquê**, não só copiar código.

---

## ⚡ TL;DR — Resumo rápido

Nesta parte do módulo, você aprende a deixar o Terraform mais **organizado, reutilizável e profissional**.

| Conceito       | Explicação direta                           |
| -------------- | --------------------------------------------- |
| `data`       | Consulta informações de algo que já existe |
| `output`     | Mostra valores gerados pelo Terraform         |
| `variable`   | Deixa o código flexível e evita repetição |
| `module`     | Agrupa código Terraform reutilizável        |
| `depends_on` | Garante ordem de criação entre recursos     |
| `fmt`        | Formata os arquivos `.tf`                   |
| `validate`   | Valida se a sintaxe está correta             |
| `plan`       | Mostra o que vai acontecer                    |
| `apply`      | Aplica as mudanças na nuvem                  |

---

# 🧠 1. Ideia principal desta parte

Antes, você criou recursos básicos com Terraform, como um bucket S3.

Agora o objetivo é evoluir para uma estrutura mais real:

```txt
Antes:
Criar um recurso simples.

Agora:
Organizar código, reaproveitar blocos e conectar recursos entre si.
```

Exemplo prático:

```txt
S3 guarda os arquivos
        ↓
CloudFront entrega esses arquivos na internet
        ↓
SQS cria fila para comunicação assíncrona
```

Para isso funcionar bem, você precisa entender:

- como consultar dados;
- como expor informações;
- como usar variáveis;
- como criar módulos;
- como controlar dependências.

---

# 🔍 2. Data Source

## ✅ O que é?

`data` serve para **buscar informações de recursos existentes**.

Ele **não cria** recurso.

Ele apenas consulta.

Pense assim:

```txt
resource = cria algo
data     = lê algo que já existe
```

---

## 🧩 Exemplo simples

Imagine que você já tem um bucket S3 criado.

Agora você quer pegar o domínio dele para usar no CloudFront.

```hcl
data "aws_s3_bucket" "bucket" {
  bucket = "meu-bucket"
}
```

Isso diz:

```txt
Terraform, procure na AWS um bucket chamado "meu-bucket"
e deixe as informações dele disponíveis para eu usar.
```

---

## 🔁 Diferença entre `resource` e `data`

| Bloco        | Faz o quê?         | Exemplo                                 |
| ------------ | ------------------- | --------------------------------------- |
| `resource` | Cria/alterar/remove | Criar bucket S3                         |
| `data`     | Consulta            | Buscar dados de um bucket já existente |

```hcl
resource "aws_s3_bucket" "bucket" {
  bucket = "meu-bucket"
}
```

Cria o bucket.

```hcl
data "aws_s3_bucket" "bucket" {
  bucket = "meu-bucket"
}
```

Consulta o bucket.

---

## ⚠️ Atenção

Se o recurso não existir, o `data` pode falhar.

Exemplo:

```txt
Você manda o Terraform consultar um bucket.
Mas o bucket ainda não foi criado.
Resultado: erro.
```

Quando o recurso está no mesmo projeto, muitas vezes é melhor usar o output direto do `resource` ou do `module`.

---

# 📤 3. Outputs

## ✅ O que é?

`output` serve para **mostrar valores gerados pelo Terraform**.

Exemplo:

Depois de criar um bucket, você pode querer ver:

- ID do bucket;
- domínio do bucket;
- região;
- ARN;
- endpoint.

---

## 🧩 Exemplo de output

```hcl
output "bucket_domain_name" {
  value       = aws_s3_bucket.bucket.bucket_domain_name
  description = "Domínio do bucket S3"
  sensitive   = false
}
```

Explicando:

| Campo                           | Função                            |
| ------------------------------- | ----------------------------------- |
| `output "bucket_domain_name"` | Nome da saída                      |
| `value`                       | Valor que será mostrado            |
| `description`                 | Explica o output                    |
| `sensitive`                   | Esconde ou não o valor no terminal |

---

## 🧠 Para que serve na prática?

Output é muito útil para conectar módulos.

Exemplo:

```txt
Módulo S3 cria o bucket
        ↓
Output expõe o domínio do bucket
        ↓
Módulo CloudFront usa esse domínio
```

---

## 🔐 Quando usar `sensitive = true`?

Use para dados sensíveis:

- senha;
- token;
- chave de API;
- secret;
- connection string;
- credenciais.

Exemplo:

```hcl
output "database_password" {
  value       = var.database_password
  sensitive   = true
  description = "Senha do banco"
}
```

⚠️ Mesmo com `sensitive = true`, o valor ainda pode aparecer no `tfstate`.
Por isso, o state precisa ser protegido.

---

# 🧱 4. Variables

## ✅ O que são?

Variáveis deixam o código configurável.

Sem variável:

```hcl
bucket = "rocketseat-bucket-iac-staging"
```

Com variável:

```hcl
bucket = "${var.org_name}-bucket-iac-${terraform.workspace}"
```

Agora você muda o nome da organização em um lugar só.

---

## 🧩 Exemplo de variável

Arquivo:

```txt
variables.tf
```

```hcl
variable "org_name" {
  type        = string
  default     = "rocketseat"
  description = "Nome da organização"
}
```

Uso:

```hcl
bucket = "${var.org_name}-bucket-iac-${terraform.workspace}"
```

---

## 🧠 Como lembrar?

```txt
variable = entrada
output   = saída
data     = consulta
resource = criação
```

---

## 🔤 Tipos comuns

| Tipo             | Exemplo              | Quando usar      |
| ---------------- | -------------------- | ---------------- |
| `string`       | `"prod"`           | Texto            |
| `number`       | `3`                | Número          |
| `bool`         | `true`             | Verdadeiro/falso |
| `list(string)` | `["a", "b"]`       | Lista            |
| `map(string)`  | `{ iac = "true" }` | Tags             |

---

## 🏷️ Variável para tags

```hcl
variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags do recurso"
}
```

Uso:

```hcl
tags = var.tags
```

Isso deixa o módulo mais genérico.

---

# 📁 5. Organização dos arquivos

Uma estrutura boa para Terraform:

```txt
terraform-modulo-03/
├── providers.tf
├── main.tf
├── variables.tf
├── outputs.tf
├── datasources.tf
└── modules/
    ├── s3/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    └── cloudfront/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

| Arquivo            | Responsabilidade                         |
| ------------------ | ---------------------------------------- |
| `providers.tf`   | Configuração do provider               |
| `main.tf`        | Chamada dos módulos/recursos principais |
| `variables.tf`   | Entradas configuráveis                  |
| `outputs.tf`     | Saídas do Terraform                     |
| `datasources.tf` | Consultas de recursos existentes         |
| `modules/`       | Códigos reutilizáveis                  |

---

# 📦 6. Modules

## ✅ O que é um módulo?

Módulo é um pacote de código Terraform reutilizável.

Pense assim:

```txt
Módulo = uma peça pronta da infraestrutura
```

Exemplos:

- módulo de S3;
- módulo de CloudFront;
- módulo de VPC;
- módulo de SQS;
- módulo de EKS.

---

## 🧠 Por que usar módulos?

Porque infraestrutura cresce rápido.

Sem módulo:

```txt
main.tf gigante
código repetido
difícil manter
difícil reaproveitar
```

Com módulo:

```txt
cada parte em seu lugar
código reutilizável
mais fácil entender
mais fácil alterar
```

---

## 🔁 Módulo interno vs externo

| Tipo    | O que é            | Exemplo                           |
| ------- | ------------------- | --------------------------------- |
| Interno | Criado por você    | `./modules/s3`                  |
| Externo | Vem do Registry/Git | `terraform-aws-modules/sqs/aws` |

---

# 🪣 7. Módulo interno de S3

## 📁 Estrutura

```txt
modules/s3/
├── main.tf
├── variables.tf
└── outputs.tf
```

---

## `modules/s3/variables.tf`

```hcl
variable "bucket_name" {
  type        = string
  description = "Nome base do bucket S3"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags do bucket"
}
```

---

## `modules/s3/main.tf`

```hcl
resource "aws_s3_bucket" "bucket" {
  bucket = "${var.bucket_name}-${terraform.workspace}"

  tags = var.tags
}
```

O nome muda conforme o workspace:

| Workspace   | Nome final                 |
| ----------- | -------------------------- |
| `default` | `rocketseat-iac-default` |
| `staging` | `rocketseat-iac-staging` |
| `prod`    | `rocketseat-iac-prod`    |

---

## `modules/s3/outputs.tf`

```hcl
output "bucket_id" {
  value       = aws_s3_bucket.bucket.id
  description = "ID do bucket"
}

output "bucket_domain_name" {
  value       = aws_s3_bucket.bucket.bucket_domain_name
  description = "Domínio do bucket"
}
```

Esses outputs serão usados pelo CloudFront.

---

# 🌐 8. Módulo interno de CloudFront

## ✅ O que é CloudFront?

CloudFront é a CDN da AWS.

CDN significa:

```txt
Content Delivery Network
```

Uso comum:

```txt
Usuário acessa o site
        ↓
CloudFront responde rápido
        ↓
CloudFront busca arquivos no S3 quando necessário
```

---

## 🧠 Por que depende do S3?

Porque o CloudFront precisa saber:

- qual bucket será a origem;
- qual domínio do bucket;
- qual ID da origem.

Por isso o S3 precisa existir antes.

---

## `modules/cloudfront/variables.tf`

```hcl
variable "origin_id" {
  type        = string
  description = "ID da origem"
}

variable "bucket_domain_name" {
  type        = string
  description = "Domínio do bucket S3"
}

variable "price_class" {
  type        = string
  default     = "PriceClass_200"
  description = "Classe de preço da CDN"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags do CloudFront"
}
```

---

## `modules/cloudfront/main.tf`

```hcl
resource "aws_cloudfront_distribution" "cdn" {
  enabled     = true
  price_class = var.price_class

  origin {
    origin_id   = var.origin_id
    domain_name = var.bucket_domain_name

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id       = var.origin_id
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = var.tags
}
```

---

# 🔗 9. Conectando S3 com CloudFront

Na raiz do projeto:

```hcl
module "s3" {
  source = "./modules/s3"

  bucket_name = "rocketseat-iac"

  tags = {
    iac         = "true"
    environment = terraform.workspace
    project     = "modulo-03"
  }
}

module "cloudfront" {
  source = "./modules/cloudfront"

  origin_id          = module.s3.bucket_id
  bucket_domain_name = module.s3.bucket_domain_name
  price_class        = "PriceClass_200"

  tags = {
    iac         = "true"
    environment = terraform.workspace
    project     = "modulo-03"
  }

  depends_on = [module.s3]
}
```

---

## 🧠 O que está acontecendo?

```hcl
origin_id = module.s3.bucket_id
```

Pega o ID gerado pelo módulo S3.

```hcl
bucket_domain_name = module.s3.bucket_domain_name
```

Pega o domínio do bucket gerado pelo módulo S3.

```hcl
depends_on = [module.s3]
```

Garante que o S3 seja criado antes do CloudFront.

---

# ⛓️ 10. `depends_on`

## ✅ O que faz?

`depends_on` força ordem de criação.

Exemplo:

```hcl
depends_on = [module.s3]
```

Significa:

```txt
Crie este recurso somente depois do módulo S3.
```

---

## Quando usar?

Use quando um recurso depende claramente de outro.

Exemplos:

| Recurso               | Depende de     |
| --------------------- | -------------- |
| CloudFront            | S3             |
| Subnet                | VPC            |
| Security Group Rule   | Security Group |
| Bucket Website Config | Bucket         |
| Policy Attachment     | IAM Role       |

---

# 🧰 11. Comandos importantes

## Formatar

```bash
terraform fmt -recursive
```

Use para deixar o código padronizado.

---

## Validar

```bash
terraform validate
```

Use para conferir se a sintaxe está correta.

---

## Planejar

```bash
terraform plan
```

Mostra o que será criado, alterado ou destruído.

---

## Aplicar

```bash
terraform apply
```

Aplica as mudanças.

Com aprovação automática:

```bash
terraform apply -auto-approve
```

---

## Destruir

```bash
terraform plan -destroy
terraform destroy
```

⚠️ Sempre revise antes de destruir.

---

# 📨 12. Módulo externo SQS

## ✅ O que é SQS?

SQS é o serviço de filas da AWS.

Ele permite comunicação assíncrona.

Exemplo:

```txt
Sistema A envia mensagem
        ↓
SQS guarda
        ↓
Sistema B processa depois
```

---

## ☠️ O que é DLQ?

DLQ significa:

```txt
Dead Letter Queue
```

É uma fila para mensagens que deram erro.

Fluxo:

```txt
Mensagem entra na fila principal
        ↓
Sistema tenta processar
        ↓
Falha várias vezes
        ↓
Mensagem vai para DLQ
```

Assim você não perde mensagens importantes.

---

## Exemplo com módulo externo

```hcl
module "sqs" {
  source = "terraform-aws-modules/sqs/aws"

  name       = "rocketseat-sqs-${terraform.workspace}"
  create_dlq = true

  tags = {
    iac         = "true"
    environment = terraform.workspace
    project     = "modulo-03"
  }
}
```

Depois de adicionar módulo externo, rode:

```bash
terraform init
terraform plan
terraform apply
```

---

# 🌍 13. Website configuration no S3

## ✅ O que é?

É uma configuração que permite usar o S3 como site estático.

Exemplo:

```hcl
resource "aws_s3_bucket_website_configuration" "bucket" {
  bucket = aws_s3_bucket.bucket.bucket

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }

  depends_on = [aws_s3_bucket.bucket]
}
```

Isso é comum para sites front-end simples.

---

# 🏷️ 14. Tags

Tags ajudam a organizar recursos.

Exemplo mínimo:

```hcl
tags = {
  iac = "true"
}
```

Melhor:

```hcl
tags = {
  iac         = "true"
  environment = terraform.workspace
  project     = "modulo-03"
}
```

Use tags para saber:

- qual projeto criou;
- qual ambiente usa;
- se é gerenciado por IaC;
- quem deve pagar o custo;
- se pode ser removido.

---

# ⚠️ 15. Erros comuns

## 1. Esquecer `terraform init`

Acontece quando você adiciona provider ou módulo.

Correção:

```bash
terraform init
```

---

## 2. Passar variável que o módulo não espera

Errado:

```hcl
module "s3" {
  source = "./modules/s3"

  url = "teste"
}
```

Se `url` não existe em `variables.tf`, dá erro.

Correção:

```txt
Declare a variável no módulo ou remova o argumento.
```

---

## 3. Bucket S3 já existe

Bucket S3 precisa ter nome único globalmente.

Correção:

```hcl
bucket = "nortemt-${var.bucket_name}-${terraform.workspace}"
```

---

## 4. Alterar recurso manualmente no console

Isso quebra a ideia de IaC.

Correção:

```txt
Altere no código .tf
rode plan
rode apply
```

---

## 5. CloudFront demora

CloudFront pode levar alguns minutos para criar.

Isso é normal.

---

## 6. `data` buscando recurso inexistente

Se o recurso não existe, a consulta falha.

Correção:

- crie o recurso primeiro;
- use output do módulo;
- ajuste dependências.

---

# ✅ 16. Boas práticas

## Organização

- Separe arquivos por responsabilidade.
- Use módulos para partes reutilizáveis.
- Não deixe tudo no `main.tf`.
- Use nomes claros.

---

## Segurança

- Não commite `tfstate`.
- Não commite `.tfvars` com segredo.
- Não use Access Key fixa sem necessidade.
- Proteja outputs sensíveis.

---

## Execução

Sempre rode:

```bash
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

---

## Código limpo

Evite hardcoded.

Ruim:

```hcl
bucket = "rocketseat-bucket-iac-staging"
```

Melhor:

```hcl
bucket = "${var.bucket_name}-${terraform.workspace}"
```

---

# 🧪 17. Mini projeto desta parte

Objetivo:

```txt
Criar uma infra com:
- S3
- CloudFront
- SQS com DLQ
- variables
- outputs
- modules
- depends_on
```

Estrutura:

```txt
terraform-modulo-03/
├── providers.tf
├── main.tf
├── variables.tf
├── outputs.tf
├── .gitignore
└── modules/
    ├── s3/
    └── cloudfront/
```

---

# 🧭 18. Fluxo mental completo

```txt
1. Crio variáveis
        ↓
2. Crio módulo S3
        ↓
3. Exponho outputs do S3
        ↓
4. Crio módulo CloudFront
        ↓
5. Passo outputs do S3 para CloudFront
        ↓
6. Uso depends_on
        ↓
7. Adiciono tags
        ↓
8. Uso módulo externo SQS
        ↓
9. Rodo fmt, validate, plan e apply
```

---

# 🧠 19. Mapa mental rápido

```txt
Terraform
├── data
│   └── consulta recurso existente
├── output
│   └── mostra valores gerados
├── variable
│   └── deixa configurável
├── module
│   ├── interno
│   └── externo
├── depends_on
│   └── controla dependência
├── S3
│   └── armazena arquivos
├── CloudFront
│   └── entrega conteúdo
└── SQS
    ├── fila principal
    └── DLQ
```

---

# 📝 20. Perguntas de revisão

## Data Source cria recurso?

Não. Ele apenas consulta.

---

## Output serve para quê?

Para expor valores gerados ou consultados.

---

## Variável serve para quê?

Para evitar repetição e deixar o código configurável.

---

## Módulo serve para quê?

Para organizar e reaproveitar código Terraform.

---

## O que é `depends_on`?

É uma forma de forçar ordem de criação.

---

## O que é DLQ?

É uma fila para mensagens que falharam no processamento.

---

# ✅ 21. Checklist final

- [ ] Entendi `data`.
- [ ] Entendi `output`.
- [ ] Entendi `variable`.
- [ ] Entendi `module`.
- [ ] Sei diferenciar módulo interno e externo.
- [ ] Sei por que S3 e CloudFront se conectam.
- [ ] Sei usar `depends_on`.
- [ ] Sei por que tags são importantes.
- [ ] Sei rodar `terraform fmt -recursive`.
- [ ] Sei rodar `terraform validate`.
- [ ] Sei rodar `terraform plan`.
- [ ] Sei rodar `terraform apply`.
- [ ] Sei o que é SQS.
- [ ] Sei o que é DLQ.

---

# 🧾 Resumo final em 4 linhas

`data` consulta informações de recursos existentes.
`output` expõe valores para visualização ou uso em outros módulos.
`variable` evita repetição e deixa o Terraform configurável.
`module` organiza a infraestrutura e permite reaproveitar código.
