# 🧠 Módulo 03 — Terraform State explicado

> Guia direto sobre **estado no Terraform**: `terraform.tfstate`, backup, state local/remoto, backend S3, versionamento, `destroy`, `.gitignore` e `tfvars`.

---

## ⚡ TL;DR

O **Terraform State** é o “mapa” que o Terraform usa para saber o que existe na sua infraestrutura.

Ele compara:

```text
Código .tf  +  terraform.tfstate  +  AWS real
```

E decide se precisa:

```text
criar ✅ | alterar 🔄 | destruir 🗑️ | não fazer nada 👍
```

Sem o state, o Terraform fica praticamente **cego**.

---

# 1. 🗺️ O que é o Terraform State?

O Terraform State normalmente fica em um arquivo chamado:

```text
terraform.tfstate
```

Esse arquivo guarda informações reais dos recursos criados, como:

- nome do recurso;
- ID;
- ARN;
- região;
- tags;
- provider usado;
- módulo de origem;
- dados gerados pela AWS.

Exemplo simples:

```text
Você escreve no código:
"Quero um bucket S3 chamado empresa-state"

A AWS cria:
bucket real no S3

O Terraform salva no state:
"Esse bucket existe e eu gerencio ele"
```

👉 **Resumo direto:**
O state é o controle interno do Terraform sobre a infraestrutura.

---

# 2. 🤔 Por que o state é importante?

Porque o Terraform precisa responder:

```text
Esse recurso já existe?
Foi alterado?
Precisa mudar?
Precisa ser recriado?
Precisa ser apagado?
```

Exemplo:

```bash
terraform plan
```

Se nada mudou, ele mostra algo parecido com:

```text
No changes.
```

Mas se você alterou uma tag no código, ele percebe e mostra o que será mudado.

---

# 3. 🎯 Quem é a fonte da verdade?

No Terraform, a fonte da verdade deve ser:

```text
Código Terraform + State
```

Não o console da AWS.

## Exemplo de problema

No código está assim:

```hcl
tags = {
  iac = "true"
}
```

Aí alguém entra manualmente na AWS e adiciona:

```text
teste = true
```

Quando você roda:

```bash
terraform plan
```

O Terraform percebe que a AWS está diferente do código.

Ele tenta corrigir para ficar igual ao que está declarado no `.tf`.

✅ Certo:

```text
Alterar o arquivo .tf
Rodar terraform plan
Rodar terraform apply
```

❌ Errado:

```text
Alterar direto no console da AWS
```

---

# 4. 🔄 Quando o state muda?

O state só muda quando o comando abaixo termina com sucesso:

```bash
terraform apply
```

O `plan` **não altera nada**.

Pense assim:

| Comando                  | O que faz                  |
| ------------------------ | -------------------------- |
| `terraform plan`       | Mostra uma prévia         |
| `terraform apply`      | Aplica de verdade          |
| `terraform destroy`    | Remove recursos            |
| `terraform state list` | Lista o que está no state |

---

# 5. 💻 State local

Por padrão, o Terraform salva o state na sua máquina.

Exemplo:

```text
projeto-iac/
├── main.tf
├── providers.tf
├── terraform.tfstate
└── terraform.tfstate.backup
```

Com workspace, pode aparecer assim:

```text
terraform.tfstate.d/
└── staging/
    └── terraform.tfstate
```

## ⚠️ Problemas do state local

State local é ok para estudo, mas ruim para projeto real.

Problemas:

- fica preso na sua máquina;
- pode ser perdido;
- pode gerar conflito em equipe;
- não funciona bem com pipeline;
- pode conter dados sensíveis;
- não deve ir para o GitHub.

👉 Em projeto real, use **state remoto**.

---

# 6. 🧯 O que é `terraform.tfstate.backup`?

É a versão anterior do state.

```text
terraform.tfstate        → estado atual
terraform.tfstate.backup → estado anterior
```

Exemplo:

```text
Antes:
state tinha 1 bucket

Depois do apply:
state atual tem 2 buckets
backup ainda guarda a versão com 1 bucket
```

Ele serve como uma segurança caso o state atual dê problema.

---

# 7. 🔎 Comandos úteis para state

## Listar recursos conhecidos pelo Terraform

```bash
terraform state list
```

Exemplo de saída:

```text
module.s3.aws_s3_bucket.bucket
module.cloudfront.aws_cloudfront_distribution.cloudfront
```

## Ver detalhes de um recurso

```bash
terraform state show module.s3.aws_s3_bucket.bucket
```

## Comandos avançados

| Comando                  | Função                     |
| ------------------------ | ---------------------------- |
| `terraform state list` | Lista recursos no state      |
| `terraform state show` | Mostra detalhes              |
| `terraform state mv`   | Move recurso dentro do state |
| `terraform state rm`   | Remove recurso do state      |
| `terraform state pull` | Baixa o state                |
| `terraform state push` | Envia state manualmente      |

⚠️ Cuidado: mexer manualmente no state é avançado.

---

# 8. ☁️ State remoto

A boa prática é guardar o state remotamente.

No módulo, o exemplo usa:

```text
AWS S3 como backend remoto
```

Ou seja, o arquivo `terraform.tfstate` passa a ficar em um bucket S3.

## Vantagens

- melhor para equipe;
- melhor para CI/CD;
- menos risco de perder o state;
- mais fácil de controlar versões;
- menos dependência da máquina local.

---

# 9. 🪣 Criando bucket para guardar o state

Exemplo:

```hcl
resource "aws_s3_bucket" "terraform_state" {
  bucket = var.state_bucket

  lifecycle {
    prevent_destroy = true
  }
}
```

## O que é `prevent_destroy`?

É uma trava de segurança.

```hcl
lifecycle {
  prevent_destroy = true
}
```

Isso impede que o Terraform apague esse bucket sem querer.

👉 Faz sentido porque esse bucket guarda o state.
Se apagar ele, você pode perder o controle da infraestrutura.

---

# 10. 🧩 Variável para o bucket do state

Arquivo:

```text
variables.tf
```

Exemplo:

```hcl
variable "state_bucket" {
  type        = string
  default     = "empresa-state-bucket-tf"
  description = "Bucket usado para guardar o state remoto"
}
```

Uso:

```hcl
bucket = var.state_bucket
```

---

# 11. 🔗 Configurando backend S3

No bloco `terraform`, você configura onde o state vai ficar:

```hcl
terraform {
  backend "s3" {
    bucket  = "empresa-state-bucket-tf"
    key     = "terraform.tfstate"
    region  = "us-east-2"
    encrypt = true
  }
}
```

## Explicando

| Campo       | Significado                   |
| ----------- | ----------------------------- |
| `bucket`  | Bucket onde o state fica      |
| `key`     | Nome/caminho do arquivo state |
| `region`  | Região da AWS                |
| `encrypt` | Criptografa o state no S3     |

⚠️ No `backend`, normalmente você não usa `var.` direto.
Por isso o nome do bucket costuma ficar fixo ali.

---

# 12. 🚀 Migrando do state local para remoto

Depois de configurar o backend, rode:

```bash
terraform init
```

O Terraform pode perguntar:

```text
Do you want to copy existing state to the new backend?
```

Responda:

```text
yes
```

Isso copia o state local para o bucket S3.

---

# 13. 🧱 State remoto com workspace

Se você usa workspaces, o Terraform separa os states.

Exemplo:

```text
env:/
└── staging/
    └── terraform.tfstate
```

Então cada ambiente pode ter seu próprio state:

```text
default
staging
production
```

---

# 14. 🕓 Versionamento do bucket

Como o state é crítico, ative versionamento no bucket S3.

Exemplo:

```hcl
resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.bucket

  versioning_configuration {
    status = "Enabled"
  }

  depends_on = [
    aws_s3_bucket.terraform_state
  ]
}
```

## Por que isso é importante?

Porque cada alteração no `terraform.tfstate` gera uma nova versão.

Se der problema, você pode recuperar uma versão anterior no S3.

---

# 15. 🔗 `depends_on`

`depends_on` força ordem de criação.

```hcl
depends_on = [
  aws_s3_bucket.terraform_state
]
```

Tradução:

```text
Só ative o versionamento depois que o bucket existir.
```

---

# 16. 🗑️ Destroy no Terraform

O comando `destroy` remove recursos.

Formas comuns:

```bash
terraform destroy
```

ou:

```bash
terraform apply -destroy
```

Antes, sempre rode:

```bash
terraform plan -destroy
```

Assim você vê o que será apagado.

---

# 17. ⚠️ Cuidado: destroy pode apagar tudo

Se você rodar:

```bash
terraform destroy
```

O Terraform tenta apagar tudo que está naquele state.

Exemplo:

```text
S3
CloudFront
SQS
DLQ
IAM
VPC
```

Tudo pode entrar no plano de destruição.

👉 Por isso: **nunca rode destroy sem revisar o plan.**

---

# 18. 🎯 Destroy com target

Para destruir só um recurso específico, use `--target`.

Exemplo:

```bash
terraform plan -destroy --target=module.s3.aws_s3_bucket.bucket
```

Depois:

```bash
terraform destroy --target=module.s3.aws_s3_bucket.bucket
```

Ou:

```bash
terraform apply -destroy --target=module.s3.aws_s3_bucket.bucket
```

## Atenção

Mesmo usando `target`, se outro recurso depender dele, o Terraform pode afetar recursos relacionados.

Exemplo:

```text
CloudFront depende do S3.
Se apagar o S3, o CloudFront pode precisar mudar também.
```

---

# 19. 🚫 `.gitignore` para Terraform

Crie um `.gitignore` para não mandar arquivos errados para o Git.

```gitignore
# Terraform
.terraform/*
*.tfstate
*.tfstate.*

# Variáveis locais
*.tfvars

# Logs
crash.log
crash.*.log

# Overrides
override.tf
override.tf.json
*_override.tf
*_override.tf.json
```

## Não envie `tfstate`

Porque ele pode conter:

- IDs internos;
- nomes de recursos;
- estrutura real da infra;
- outputs;
- informações sensíveis.

## Não envie `.terraform/`

Porque é cache local.
Dá para reconstruir com:

```bash
terraform init
```

---

# 20. 🔒 `.terraform.lock.hcl`

Esse arquivo pode ir para o Git.

Ele trava versões dos providers usados.

```text
.terraform.lock.hcl
```

Ele ajuda todo mundo a usar as mesmas versões.

---

# 21. 🧾 `terraform.tfvars`

O `tfvars` serve para definir valores reais das variáveis.

## `variables.tf`

```hcl
variable "state_bucket" {
  type        = string
  default     = "empresa-state-bucket-tf"
  description = "Bucket usado para guardar o state remoto"
}
```

## `terraform.tfvars`

```hcl
state_bucket = "meu-bucket-de-state"
```

O valor do `terraform.tfvars` sobrescreve o `default`.

Pense assim:

```text
variables.tf     → declara as variáveis
terraform.tfvars → informa os valores
```

É parecido com:

```text
.env em uma aplicação
```

⚠️ Se tiver dado sensível, não envie para o Git.

---

# 22. ✅ Fluxo recomendado

## Quando iniciar ou mudar backend

```bash
terraform init
```

## Antes de aplicar

```bash
terraform fmt
terraform validate
terraform plan
```

## Para aplicar

```bash
terraform apply
```

## Para verificar o state

```bash
terraform state list
```

## Para destruir com segurança

```bash
terraform plan -destroy
terraform destroy
```

---

# 23. 🧭 Fluxo visual

```text
1. Escreve código .tf
        ↓
2. terraform fmt
        ↓
3. terraform validate
        ↓
4. terraform plan
        ↓
5. Terraform compara:
   código + state + cloud
        ↓
6. terraform apply
        ↓
7. Infra muda na AWS
        ↓
8. terraform.tfstate é atualizado
```

---

# 24. 🆚 State local vs remoto

| Tipo   | Onde fica                            | Melhor uso                      |
| ------ | ------------------------------------ | ------------------------------- |
| Local  | Sua máquina                         | Estudo e teste                  |
| Remoto | S3, Azure Blob, GCS, Terraform Cloud | Projeto real, equipe e pipeline |

---

# 25. ✅ Boas práticas

## Faça

- use backend remoto;
- ative versionamento no bucket do state;
- use `prevent_destroy`;
- rode `plan` antes do `apply`;
- rode `plan -destroy` antes do `destroy`;
- ignore `tfstate` no Git;
- versione `.terraform.lock.hcl`;
- use tags como `iac = "true"`.

## Evite

- alterar recurso manualmente no console;
- commitar `terraform.tfstate`;
- commitar `terraform.tfvars` com dados sensíveis;
- rodar `destroy` sem revisar;
- deixar state só local em projeto real;
- mexer manualmente no state sem necessidade.

---

# 26. 🧨 Erros comuns

## 1. Comitar `terraform.tfstate`

Erro grave. Pode expor dados da infraestrutura.

## 2. Apagar o bucket do state

Você pode perder o controle da infra.

Use:

```hcl
prevent_destroy = true
```

## 3. Alterar recurso manualmente na AWS

Cria diferença entre:

```text
código
state
AWS real
```

## 4. Rodar `destroy` sem conferir

Pode apagar tudo.

## 5. Esquecer `terraform init`

Sempre rode `init` depois de mudar backend ou adicionar módulos.

---

# 27. 📦 Exemplo completo — Backend S3

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket  = "empresa-state-bucket-tf"
    key     = "terraform.tfstate"
    region  = "us-east-2"
    encrypt = true
  }
}

provider "aws" {
  region = "us-east-2"
}

variable "state_bucket" {
  type        = string
  default     = "empresa-state-bucket-tf"
  description = "Bucket usado para guardar o state remoto"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = var.state_bucket

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.bucket

  versioning_configuration {
    status = "Enabled"
  }

  depends_on = [
    aws_s3_bucket.terraform_state
  ]
}
```

---

# 28. 🧪 Perguntas rápidas

## O que é `terraform.tfstate`?

É o arquivo que guarda o estado conhecido da infraestrutura.

## Posso enviar `tfstate` para o GitHub?

Não. Ele pode conter dados sensíveis.

## O que é state remoto?

É guardar o state fora da sua máquina, por exemplo em um bucket S3.

## Para que serve `prevent_destroy`?

Para impedir que um recurso importante seja destruído sem querer.

## Para que serve `terraform.tfvars`?

Para passar valores reais para as variáveis.

## `destroy` apaga tudo?

Pode apagar tudo que está naquele state. Por isso precisa de cuidado.

---

# 29. ✅ Checklist de revisão

- [ ] Sei o que é `terraform.tfstate`.
- [ ] Sei por que o state é importante.
- [ ] Sei a diferença entre state local e remoto.
- [ ] Sei para que serve o backup.
- [ ] Sei configurar backend S3.
- [ ] Sei por que usar `encrypt = true`.
- [ ] Sei por que ativar versionamento.
- [ ] Sei usar `prevent_destroy`.
- [ ] Sei rodar `terraform state list`.
- [ ] Sei o risco do `terraform destroy`.
- [ ] Sei usar `--target` com cuidado.
- [ ] Sei para que serve `terraform.tfvars`.
- [ ] Sei configurar `.gitignore`.

---

# 30. 🧠 Resumo final

O **Terraform State** é o mapa que mostra ao Terraform o que existe na infraestrutura.

Em estudo, ele pode ficar local. Em projeto real, o ideal é usar **state remoto**, como S3.

O bucket do state deve ser protegido com **criptografia, versionamento e `prevent_destroy`**.

O comando `destroy` deve ser usado com muito cuidado, porque pode apagar tudo que está no state.

---

## 🚀 Resumo em 4 linhas

Terraform usa `terraform.tfstate` para saber o que existe na infraestrutura.
Esse arquivo não deve ir para o Git, porque pode conter dados sensíveis.
Em projeto real, use backend remoto no S3 com criptografia e versionamento.
Sempre revise `terraform plan -destroy` antes de apagar qualquer recurso.
