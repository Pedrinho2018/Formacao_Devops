# Módulo 03 — Terraform: Data Sources, Outputs, Variables e Modules

> **Objetivo deste material:** entender como o Terraform busca informações de recursos existentes, expõe valores de saída, usa variáveis e organiza infraestrutura com módulos internos e externos.

---

## TL;DR — Resumo rápido

Neste bloco do módulo, você sai do Terraform “básico” e começa a organizar infraestrutura de verdade.

Você aprende a usar:

| Recurso | Para que serve |
|---|---|
| `data` | Buscar informações de recursos já existentes |
| `output` | Expor valores gerados pelo Terraform |
| `variable` | Evitar código repetido e deixar o código configurável |
| `module` | Reutilizar blocos de infraestrutura |
| `depends_on` | Forçar ordem de criação entre recursos |
| `terraform fmt` | Padronizar a formatação dos arquivos `.tf` |
| `terraform validate` | Validar sintaxe antes de rodar o plano |
| `terraform plan` | Ver o que será criado, alterado ou destruído |
| `terraform apply` | Aplicar as mudanças na AWS |
| `terraform destroy` | Remover recursos gerenciados pelo Terraform |

---

# 1. O que muda nesta parte do módulo?

Antes, você já tinha visto:

- provider AWS;
- recurso S3;
- `terraform init`;
- `terraform plan`;
- `terraform apply`;
- `terraform destroy`;
- `tfstate`;
- workspaces.

Agora o foco muda para **organização e reaproveitamento**.

A ideia deixa de ser:

> “Criar um recurso simples no Terraform.”

E passa a ser:

> “Criar uma infraestrutura organizada, reaproveitável e fácil de manter.”

---

# 2. Data Source no Terraform

## 2.1 O que é um Data Source?

Um **Data Source** é uma forma de o Terraform **consultar informações de algo que já existe**.

Ele não cria recurso.

Ele apenas lê dados.

Exemplo:

Você criou um bucket S3. Depois da criação, esse bucket tem várias informações que você não escreveu manualmente:

- `id`;
- `arn`;
- `bucket_domain_name`;
- `bucket_regional_domain_name`;
- `region`;
- outras propriedades geradas pela AWS.

Essas informações podem ser necessárias para criar outro recurso.

Por exemplo:

> O CloudFront precisa saber qual bucket S3 ele vai usar como origem.

Então você pode usar um `data` para buscar essas informações.

---

## 2.2 Diferença entre `resource` e `data`

| Bloco | Função |
|---|---|
| `resource` | Cria, altera ou destrói infraestrutura |
| `data` | Consulta informações de infraestrutura já existente |

Exemplo mental:

```hcl
resource "aws_s3_bucket" "bucket" {
  bucket = "meu-bucket"
}
```

Esse bloco cria um bucket.

Agora:

```hcl
data "aws_s3_bucket" "bucket" {
  bucket = "meu-bucket"
}
```

Esse bloco consulta um bucket que já existe.

---

## 2.3 Exemplo de Data Source para S3

Arquivo sugerido:

```txt
datasources.tf
```

Código:

```hcl
data "aws_s3_bucket" "bucket" {
  bucket = "${var.org_name}-bucket-iac-${terraform.workspace}"
}
```

Explicando:

| Parte | Significado |
|---|---|
| `data` | Palavra reservada para consulta |
| `aws_s3_bucket` | Tipo de recurso que será consultado |
| `bucket` | Nome interno no Terraform |
| `bucket = ...` | Nome real do bucket na AWS |
| `terraform.workspace` | Workspace atual, exemplo: `default` ou `staging` |

---

## 2.4 Atenção importante

Se o recurso ainda não existir na AWS, o `data` pode falhar.

Por isso, em alguns casos, você primeiro cria o recurso com `resource`, aplica com `terraform apply`, e depois usa `data` para consultar.

---

# 3. Outputs no Terraform

## 3.1 O que é Output?

`output` é uma variável de saída.

Ele serve para mostrar ou disponibilizar informações geradas pelo Terraform.

Exemplo:

Depois que o bucket S3 é criado, você pode querer ver:

- domínio do bucket;
- região;
- ARN;
- ID;
- endpoint;
- URL.

O `output` mostra isso no terminal depois do `terraform apply`.

---

## 3.2 Exemplo simples de Output

Arquivo sugerido:

```txt
outputs.tf
```

Código:

```hcl
output "bucket_domain_name" {
  value       = data.aws_s3_bucket.bucket.bucket_domain_name
  sensitive   = false
  description = "Nome de domínio do bucket S3"
}
```

Explicando:

| Campo | Função |
|---|---|
| `output "bucket_domain_name"` | Nome da saída |
| `value` | Valor que será exibido |
| `sensitive` | Define se é informação sensível |
| `description` | Explica o que esse output representa |

---

## 3.3 Output da região do bucket

```hcl
output "bucket_region" {
  value       = data.aws_s3_bucket.bucket.region
  sensitive   = false
  description = "Região do bucket S3"
}
```

---

## 3.4 Quando usar `sensitive = true`?

Use `sensitive = true` quando o output mostrar algo confidencial.

Exemplos:

- senha;
- token;
- chave de API;
- connection string;
- secret;
- credencial.

Exemplo:

```hcl
output "database_password" {
  value       = var.database_password
  sensitive   = true
  description = "Senha do banco de dados"
}
```

Atenção: marcar como `sensitive` esconde a saída no terminal, mas **não significa que a informação sumiu do state**. O `tfstate` ainda pode conter dados sensíveis. Por isso ele deve ser protegido.

---

# 4. Variables no Terraform

## 4.1 O que são variáveis?

Variáveis servem para evitar código duplicado.

Em vez de escrever o mesmo nome várias vezes, você cria uma variável e usa em vários lugares.

Sem variável:

```hcl
bucket = "rocketseat-bucket-iac-staging"
```

Com variável:

```hcl
bucket = "${var.org_name}-bucket-iac-${terraform.workspace}"
```

Agora você muda `org_name` em um lugar só.

---

## 4.2 Arquivo de variáveis

Arquivo sugerido:

```txt
variables.tf
```

Exemplo:

```hcl
variable "org_name" {
  type        = string
  default     = "rocketseat"
  description = "Nome da organização usado nos recursos"
}
```

---

## 4.3 Como usar uma variável

Sempre use o prefixo `var.`.

```hcl
var.org_name
```

Exemplo completo:

```hcl
resource "aws_s3_bucket" "bucket" {
  bucket = "${var.org_name}-bucket-iac-${terraform.workspace}"

  tags = {
    iac = "true"
  }
}
```

---

## 4.4 Tipos comuns de variável

| Tipo | Exemplo | Uso |
|---|---|---|
| `string` | `"rocketseat"` | Texto |
| `number` | `10` | Número |
| `bool` | `true` | Verdadeiro/falso |
| `list(string)` | `["a", "b"]` | Lista |
| `map(string)` | `{ iac = "true" }` | Mapa/chave-valor |

---

## 4.5 Exemplo de variável com `map(string)`

Muito usada para tags:

```hcl
variable "s3_tags" {
  type        = map(string)
  default     = {}
  description = "Tags do bucket S3"
}
```

Uso:

```hcl
resource "aws_s3_bucket" "bucket" {
  bucket = "${var.s3_bucket_name}-${terraform.workspace}"

  tags = var.s3_tags
}
```

---

# 5. Organização dos arquivos `.tf`

Uma estrutura mais limpa fica assim:

```txt
primeiro-projeto-iac/
├── providers.tf
├── main.tf
├── variables.tf
├── outputs.tf
├── datasources.tf
└── modules/
    ├── s3/
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── datasources.tf
    └── cloudfront/
        ├── main.tf
        ├── variables.tf
        ├── outputs.tf
        └── datasources.tf
```

Separar os arquivos ajuda muito.

| Arquivo | Responsabilidade |
|---|---|
| `providers.tf` | Configuração dos providers |
| `main.tf` | Chamada dos recursos ou módulos principais |
| `variables.tf` | Variáveis de entrada |
| `outputs.tf` | Saídas do Terraform |
| `datasources.tf` | Consultas de recursos existentes |
| `modules/` | Módulos internos reutilizáveis |

---

# 6. Módulos no Terraform

## 6.1 O que é um módulo?

Um módulo é um pacote de arquivos Terraform que resolve uma parte da infraestrutura.

Pensa assim:

> Módulo é uma “peça reutilizável” da sua infraestrutura.

Exemplos de módulos:

- módulo de S3;
- módulo de CloudFront;
- módulo de VPC;
- módulo de EKS;
- módulo de SQS;
- módulo de IAM.

---

## 6.2 Por que usar módulos?

Porque infraestrutura cresce rápido.

Se você colocar tudo no `main.tf`, vira bagunça.

Módulos ajudam em:

- organização;
- reutilização;
- manutenção;
- padronização;
- redução de duplicidade;
- reaproveitamento entre projetos;
- clareza para times.

---

## 6.3 Módulo interno vs módulo externo

| Tipo | O que é |
|---|---|
| Módulo interno | Criado por você dentro do projeto |
| Módulo externo | Baixado do Terraform Registry ou Git |

Exemplo de módulo interno:

```hcl
module "s3" {
  source = "./modules/s3"
}
```

Exemplo de módulo externo:

```hcl
module "sqs" {
  source = "terraform-aws-modules/sqs/aws"
}
```

---

# 7. Criando módulo interno de S3

## 7.1 Estrutura

```txt
modules/
└── s3/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

---

## 7.2 `modules/s3/variables.tf`

```hcl
variable "s3_bucket_name" {
  type        = string
  description = "Nome base do bucket S3"
}

variable "s3_tags" {
  type        = map(string)
  default     = {}
  description = "Tags do bucket S3"
}
```

---

## 7.3 `modules/s3/main.tf`

```hcl
resource "aws_s3_bucket" "bucket" {
  bucket = "${var.s3_bucket_name}-${terraform.workspace}"

  tags = var.s3_tags
}
```

Aqui o nome final muda conforme o workspace.

Exemplo:

| Workspace | Nome gerado |
|---|---|
| `default` | `rocketseat-iac-default` |
| `staging` | `rocketseat-iac-staging` |
| `prod` | `rocketseat-iac-prod` |

---

## 7.4 `modules/s3/outputs.tf`

```hcl
output "bucket_domain_name" {
  value       = aws_s3_bucket.bucket.bucket_domain_name
  sensitive   = false
  description = "Nome de domínio do bucket S3"
}

output "bucket_id" {
  value       = aws_s3_bucket.bucket.id
  sensitive   = false
  description = "ID do bucket S3"
}
```

Esses outputs podem ser usados por outro módulo.

Exemplo:

> O módulo CloudFront precisa saber o domínio e o ID do bucket S3.

---

# 8. Chamando o módulo S3 na raiz

Arquivo:

```txt
main.tf
```

Código:

```hcl
module "s3" {
  source = "./modules/s3"

  s3_bucket_name = "rocketseat-iac"

  s3_tags = {
    iac = "true"
  }
}
```

---

## 8.1 Ponto importante

Sempre que adicionar ou alterar módulos, rode:

```bash
terraform init
```

Depois:

```bash
terraform fmt
terraform validate
terraform plan
terraform apply
```

---

# 9. Criando módulo interno de CloudFront

## 9.1 O que é CloudFront?

CloudFront é o serviço de CDN da AWS.

CDN significa **Content Delivery Network**, ou seja, rede de entrega de conteúdo.

Uso comum:

- entregar frontend;
- cachear arquivos estáticos;
- melhorar performance;
- servir conteúdo vindo de S3;
- disponibilizar domínio de acesso.

Fluxo mental:

```txt
Usuário → CloudFront → S3
```

O CloudFront fica na frente.

O S3 guarda os arquivos.

---

## 9.2 Por que o CloudFront depende do S3?

Porque ele precisa saber:

- qual bucket será usado como origem;
- qual domínio do bucket será usado;
- qual ID/origin ID será usado.

Por isso o S3 precisa ser criado antes.

---

## 9.3 Estrutura do módulo CloudFront

```txt
modules/
└── cloudfront/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

---

## 9.4 `modules/cloudfront/variables.tf`

```hcl
variable "origin_id" {
  type        = string
  description = "ID da origem do CloudFront"
}

variable "bucket_domain_name" {
  type        = string
  description = "Nome de domínio do bucket S3"
}

variable "cdn_price_class" {
  type        = string
  default     = "PriceClass_200"
  description = "Classe de preço da CDN"
}

variable "cdn_tags" {
  type        = map(string)
  default     = {}
  description = "Tags da CDN"
}
```

---

## 9.5 `modules/cloudfront/main.tf`

```hcl
resource "aws_cloudfront_distribution" "cloudfront" {
  enabled     = true
  price_class = var.cdn_price_class

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

  tags = var.cdn_tags
}
```

---

## 9.6 Chamando CloudFront na raiz

Arquivo:

```txt
main.tf
```

Código:

```hcl
module "cloudfront" {
  source = "./modules/cloudfront"

  origin_id          = module.s3.bucket_id
  bucket_domain_name = module.s3.bucket_domain_name
  cdn_price_class    = "PriceClass_200"

  cdn_tags = {
    iac = "true"
  }

  depends_on = [module.s3]
}
```

---

## 9.7 O que está acontecendo aqui?

```hcl
origin_id = module.s3.bucket_id
```

O CloudFront pega o ID vindo do output do módulo S3.

```hcl
bucket_domain_name = module.s3.bucket_domain_name
```

O CloudFront pega o domínio do bucket vindo do módulo S3.

```hcl
depends_on = [module.s3]
```

Garante que o S3 será criado antes do CloudFront.

---

# 10. `depends_on`

## 10.1 O que é?

`depends_on` força uma ordem de dependência.

Exemplo:

```hcl
depends_on = [module.s3]
```

Isso significa:

> “Só crie este recurso depois que o módulo S3 estiver pronto.”

---

## 10.2 Quando usar?

Use quando um recurso realmente depende de outro.

Exemplos:

- CloudFront depende do S3;
- Website config depende do bucket;
- Policy depende de role;
- Subnet depende de VPC;
- Route table association depende da subnet e da route table.

---

# 11. Melhorando os módulos com tags

Tags são essenciais para organização.

Exemplo:

```hcl
tags = {
  iac = "true"
}
```

Recomendação:

```hcl
tags = {
  iac         = "true"
  environment = terraform.workspace
  project     = "modulo-03-iac"
}
```

Tags ajudam a responder:

- quem criou o recurso?
- é gerenciado por IaC?
- pertence a qual ambiente?
- pertence a qual projeto?
- pode ser deletado?
- gera custo para qual área?

---

# 12. `terraform fmt`

## 12.1 Para que serve?

Formata automaticamente os arquivos Terraform.

```bash
terraform fmt
```

Para formatar tudo, inclusive subpastas:

```bash
terraform fmt -recursive
```

Use antes de commitar.

---

# 13. `terraform validate`

## 13.1 Para que serve?

Valida a sintaxe dos arquivos `.tf`.

```bash
terraform validate
```

Ele detecta erros como:

- atributo escrito errado;
- variável inexistente;
- bloco inválido;
- argumento não esperado;
- estrutura quebrada.

---

# 14. Módulo externo: SQS

## 14.1 O que é SQS?

SQS significa **Simple Queue Service**.

É o serviço de filas da AWS.

Ele é usado para comunicação assíncrona.

Exemplo:

```txt
Sistema A envia mensagem → SQS → Sistema B consome depois
```

Isso desacopla sistemas.

---

## 14.2 O que é DLQ?

DLQ significa **Dead Letter Queue**.

É uma fila para mensagens que deram erro no processamento.

Exemplo:

```txt
Mensagem chega na fila principal
↓
Aplicação tenta processar
↓
Falha várias vezes
↓
Mensagem vai para DLQ
```

Isso evita perder eventos importantes.

---

## 14.3 Usando módulo externo SQS

Arquivo:

```txt
main.tf
```

Exemplo:

```hcl
module "sqs" {
  source = "terraform-aws-modules/sqs/aws"

  name       = "rocketseat-sqs"
  create_dlq = true

  tags = {
    iac = "true"
  }
}
```

---

## 14.4 O que o módulo SQS cria?

Mesmo com poucas linhas, ele pode criar vários recursos:

- fila principal;
- DLQ;
- política de redrive;
- permissões/configurações auxiliares.

Essa é a força de usar módulos.

Você escreve pouco, mas recebe uma estrutura mais completa.

---

## 14.5 Sempre rode `terraform init` ao usar módulo externo

Quando você adiciona:

```hcl
source = "terraform-aws-modules/sqs/aws"
```

O Terraform precisa baixar o módulo.

Rode:

```bash
terraform init
```

Depois:

```bash
terraform plan
terraform apply
```

---

# 15. Múltiplos Data Sources

## 15.1 Por que usar múltiplos data sources?

Quando sua infraestrutura cresce, um recurso começa a depender de vários dados.

Exemplo:

Você pode consultar:

- bucket S3;
- distribuição CloudFront;
- fila SQS;
- VPC;
- subnets;
- security groups;
- IAM roles.

Cada consulta pode ficar em um `datasources.tf`.

---

## 15.2 Data source do S3 dentro do módulo

Exemplo:

```hcl
data "aws_s3_bucket" "bucket" {
  bucket = aws_s3_bucket.bucket.bucket
}
```

---

## 15.3 Data source do CloudFront

Exemplo conceitual:

```hcl
data "aws_cloudfront_distribution" "cloudfront" {
  id = aws_cloudfront_distribution.cloudfront.id
}
```

---

## 15.4 Outputs usando Data Sources

Exemplo:

```hcl
output "cdn_id" {
  value       = data.aws_cloudfront_distribution.cloudfront.id
  sensitive   = false
  description = "ID do CloudFront"
}

output "cdn_domain_name" {
  value       = data.aws_cloudfront_distribution.cloudfront.domain_name
  sensitive   = false
  description = "Nome de domínio do CloudFront"
}
```

---

# 16. Website configuration no S3

## 16.1 O que é?

É uma configuração para o bucket S3 atuar como site estático.

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

---

## 16.2 Por que usar `depends_on` aqui?

Porque a configuração de website só pode ser aplicada depois que o bucket existir.

```hcl
depends_on = [aws_s3_bucket.bucket]
```

---

# 17. Fluxo completo recomendado

Sempre siga esta ordem:

```bash
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

Para destruir:

```bash
terraform plan -destroy
terraform destroy
```

Ou:

```bash
terraform apply -destroy
```

---

# 18. Fluxo mental desta parte do módulo

```txt
1. Criar módulo S3
   ↓
2. Expor outputs do S3
   ↓
3. Criar módulo CloudFront
   ↓
4. Passar outputs do S3 como inputs do CloudFront
   ↓
5. Usar depends_on para garantir ordem
   ↓
6. Usar tags para organização
   ↓
7. Usar módulo externo SQS para evitar código gigante
   ↓
8. Criar data sources e outputs para consultar informações geradas
```

---

# 19. Erros comuns

## Erro 1 — Esquecer `terraform init`

Quando você cria ou muda módulo, rode:

```bash
terraform init
```

Senão pode aparecer erro de módulo não instalado.

---

## Erro 2 — Passar variável não declarada no módulo

Exemplo errado:

```hcl
module "s3" {
  source = "./modules/s3"

  url = "teste"
}
```

Se `url` não existir em `modules/s3/variables.tf`, o Terraform retorna erro parecido com:

```txt
An argument named "url" is not expected here.
```

Correção:

Declare a variável no módulo:

```hcl
variable "url" {
  type        = string
  description = "URL usada pelo módulo"
}
```

Ou remova o argumento.

---

## Erro 3 — Nome de bucket S3 já existe

Bucket S3 precisa ter nome globalmente único.

Se der conflito, use algo mais específico:

```hcl
bucket = "nortemt-${var.s3_bucket_name}-${terraform.workspace}"
```

---

## Erro 4 — Alterar recurso manualmente no console

Se você altera manualmente no console da AWS, quebra a ideia de IaC.

O Terraform pode desfazer sua alteração no próximo `apply`.

A fonte da verdade deve ser o código.

---

## Erro 5 — CloudFront demora para criar

CloudFront pode demorar alguns minutos.

Isso é normal.

Não mate o processo sem necessidade.

---

## Erro 6 — Data Source buscando recurso inexistente

Se o `data` consulta algo que ainda não existe, o Terraform pode falhar.

Solução:

- criar o recurso primeiro;
- usar outputs diretos do recurso;
- ajustar dependências;
- separar o apply em etapas, se necessário.

---

# 20. Boas práticas

## 20.1 Separe responsabilidades

Evite jogar tudo no `main.tf`.

Prefira:

```txt
providers.tf
variables.tf
outputs.tf
datasources.tf
main.tf
```

---

## 20.2 Use tags sempre

No mínimo:

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
  project     = "terraform-modulo-03"
}
```

---

## 20.3 Use `fmt` e `validate`

Antes de rodar `plan`:

```bash
terraform fmt -recursive
terraform validate
```

---

## 20.4 Evite valores hardcoded

Ruim:

```hcl
bucket = "rocketseat-bucket-iac-staging"
```

Melhor:

```hcl
bucket = "${var.s3_bucket_name}-${terraform.workspace}"
```

---

## 20.5 Não commite arquivos sensíveis

Evite commitar:

```txt
.terraform/
terraform.tfstate
terraform.tfstate.backup
*.tfvars
```

Exemplo de `.gitignore`:

```gitignore
.terraform/
*.tfstate
*.tfstate.*
*.tfvars
crash.log
override.tf
override.tf.json
*_override.tf
*_override.tf.json
```

---

# 21. Mini projeto desta parte

## Objetivo

Criar uma infraestrutura com:

- S3;
- CloudFront;
- SQS com DLQ;
- outputs;
- variables;
- data sources;
- modules.

---

## Estrutura final sugerida

```txt
terraform-modulo-03/
├── providers.tf
├── main.tf
├── variables.tf
├── outputs.tf
├── datasources.tf
├── .gitignore
└── modules/
    ├── s3/
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── datasources.tf
    └── cloudfront/
        ├── main.tf
        ├── variables.tf
        ├── outputs.tf
        └── datasources.tf
```

---

# 22. Exemplo final de `main.tf` da raiz

```hcl
module "s3" {
  source = "./modules/s3"

  s3_bucket_name = "rocketseat-iac"

  s3_tags = {
    iac         = "true"
    environment = terraform.workspace
    project     = "modulo-03"
  }
}

module "cloudfront" {
  source = "./modules/cloudfront"

  origin_id          = module.s3.bucket_id
  bucket_domain_name = module.s3.bucket_domain_name
  cdn_price_class    = "PriceClass_200"

  cdn_tags = {
    iac         = "true"
    environment = terraform.workspace
    project     = "modulo-03"
  }

  depends_on = [module.s3]
}

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

---

# 23. Checklist de revisão

Marque quando entender:

- [ ] Sei explicar a diferença entre `resource` e `data`.
- [ ] Sei criar um `datasources.tf`.
- [ ] Sei criar um `outputs.tf`.
- [ ] Sei usar `value = data...`.
- [ ] Sei usar `value = module...`.
- [ ] Sei criar variáveis em `variables.tf`.
- [ ] Sei usar `var.nome_da_variavel`.
- [ ] Sei criar módulo interno.
- [ ] Sei chamar módulo interno com `source = "./modules/..."`.
- [ ] Sei usar módulo externo do Terraform Registry.
- [ ] Sei quando rodar `terraform init`.
- [ ] Sei usar `terraform fmt -recursive`.
- [ ] Sei usar `terraform validate`.
- [ ] Sei usar `depends_on`.
- [ ] Sei por que tags são importantes.
- [ ] Sei por que CloudFront depende do S3.
- [ ] Sei o que é SQS.
- [ ] Sei o que é DLQ.

---

# 24. Perguntas para testar conhecimento

## 1. Data Source cria recurso?

Não. Data Source apenas consulta informações de recursos existentes.

---

## 2. Output serve para quê?

Serve para expor valores gerados ou consultados pelo Terraform.

---

## 3. Por que usar variável?

Para evitar repetição e deixar o código configurável.

---

## 4. Por que usar módulo?

Para reutilizar código e organizar melhor a infraestrutura.

---

## 5. Quando rodar `terraform init`?

Quando iniciar o projeto, alterar provider ou adicionar/alterar módulos.

---

## 6. O que `depends_on` faz?

Força ordem de criação entre recursos ou módulos.

---

## 7. O que é DLQ?

É uma fila para mensagens que falharam no processamento.

---

# 25. Mapa mental textual

```txt
Terraform avançando
├── Data Sources
│   ├── Lê recurso existente
│   ├── Usa palavra data
│   └── Ajuda a reaproveitar atributos
│
├── Outputs
│   ├── Mostra saídas
│   ├── Pode alimentar outros módulos
│   └── Pode ser sensitive
│
├── Variables
│   ├── Evita repetição
│   ├── Usa var.nome
│   ├── Pode ter type
│   └── Pode ter default
│
├── Modules
│   ├── Internos
│   │   ├── ./modules/s3
│   │   └── ./modules/cloudfront
│   └── Externos
│       └── terraform-aws-modules/sqs/aws
│
├── Dependências
│   └── depends_on
│
└── Boas práticas
    ├── fmt
    ├── validate
    ├── tags
    ├── sem hardcoded
    └── não commitar tfstate
```

---

# 26. Resumo final em 4 linhas

Data Source consulta informações de recursos existentes.  
Output expõe valores que podem ser usados depois.  
Variables deixam o código flexível e sem repetição.  
Modules organizam a infraestrutura e evitam código duplicado.

---

# 27. Próximo passo lógico

Depois desta parte, o próximo assunto natural é:

> **gerenciamento de estado remoto no Terraform**.

Porque até aqui o state ainda está local.

Em projeto real, o state precisa ficar remoto, protegido e compartilhável, normalmente usando:

- S3;
- DynamoDB para lock;
- Terraform Cloud;
- outro backend remoto.
