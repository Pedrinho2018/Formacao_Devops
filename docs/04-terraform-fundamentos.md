# 🚀 Módulo 03 — Iniciando com Terraform

> Revisão rápida e prática sobre o começo do Terraform no módulo de IaC.

---

## ⚡ TL;DR

Neste módulo, você sai da teoria de IaC e começa a usar **Terraform na prática**.

Você aprende a:

- entender o ecossistema do Terraform;
- usar **provider**, **resource** e **module**;
- rodar os comandos principais da CLI;
- configurar autenticação na AWS com **SSO**;
- criar, alterar e destruir um bucket S3;
- entender o básico de **state**;
- separar ambientes com **workspaces**.

---

# 🧠 1. Ideia principal

O Terraform serve para criar infraestrutura usando código.

Em vez de clicar no painel da AWS, você escreve arquivos `.tf`.

Exemplo mental:

```txt
Quero um bucket S3
Quero uma EC2
Quero uma VPC
Quero um cluster Kubernetes
```

Com Terraform, isso vira código.

---

# 🧩 2. Conceitos que você precisa gravar

| Conceito            | Explicação simples                  |
| ------------------- | ------------------------------------- |
| **Provider**  | Serviço que o Terraform controla     |
| **Resource**  | Recurso que será criado              |
| **Module**    | Bloco reutilizável de infraestrutura |
| **State**     | Arquivo que guarda o estado da infra  |
| **Workspace** | Separação de ambientes/estados      |
| **Registry**  | Catálogo de providers e módulos     |

---

# 🌐 3. Terraform Registry

O **Terraform Registry** é tipo um “Docker Hub da infraestrutura”.

Nele você encontra:

- providers;
- resources;
- modules;
- exemplos de uso;
- documentação.

Resumo:

```txt
Provider = com quem o Terraform fala
Resource = o que o Terraform cria
Module = pacote reutilizável pronto
```

---

# 🔌 4. Provider

O provider conecta o Terraform com algum serviço.

Exemplo AWS:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}
```

Depois rode:

```bash
terraform init
```

---

# 📦 5. Resource

Resource é o recurso real criado na cloud.

Exemplo: criar um bucket S3.

```hcl
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "meu-primeiro-bucket-iac"

  tags = {
    Name = "Primeiro Bucket"
    IAC  = "true"
  }
}
```

| Parte             | Significado                   |
| ----------------- | ----------------------------- |
| `resource`      | Indica criação de recurso   |
| `aws_s3_bucket` | Tipo do recurso               |
| `s3_bucket`     | Nome interno no Terraform     |
| `bucket`        | Nome real do bucket           |
| `tags`          | Identificação/organização |

---

# 🧱 6. Module

Module é um bloco reutilizável.

Ele evita código repetido.

Pense assim:

```txt
Module = template pronto para reaproveitar
```

Você pode usar:

- módulos públicos do Terraform Registry;
- módulos internos da empresa/projeto.

---

# 🗂️ 7. Estrutura inicial recomendada

```txt
projeto-iac/
├── providers.tf
├── main.tf
├── variables.tf
├── outputs.tf
└── .gitignore
```

No início, pode ser só:

```txt
projeto-iac/
├── providers.tf
└── main.tf
```

Boa prática no nome do repositório:

```txt
sistema-iac
projeto-infra
empresa-cloud-infra
```

---

# 💻 8. Comandos principais

| Comando                 | Para que serve             |
| ----------------------- | -------------------------- |
| `terraform init`      | Inicializa o projeto       |
| `terraform validate`  | Valida os arquivos `.tf` |
| `terraform plan`      | Mostra o que vai acontecer |
| `terraform apply`     | Aplica as mudanças        |
| `terraform destroy`   | Remove recursos            |
| `terraform workspace` | Gerencia ambientes/estados |

Fluxo recomendado:

```bash
terraform init
terraform validate
terraform plan
terraform apply
```

Com aprovação automática:

```bash
terraform apply -auto-approve
```

⚠️ Use `-auto-approve` com cuidado. Em produção, revise o `plan` antes.

---

# 🔐 9. Autenticação na AWS

Para o Terraform criar recursos na AWS, ele precisa autenticar.

| Forma                   | Comentário                    |
| ----------------------- | ------------------------------ |
| Access Key / Secret Key | Mais simples, mas menos segura |
| AWS SSO                 | Mais segura e recomendada      |

O módulo usa **AWS SSO / IAM Identity Center**.

Vantagens:

- token temporário;
- expiração da sessão;
- suporte a MFA;
- evita chave fixa na máquina;
- mais seguro para longo prazo.

Comandos:

```bash
aws configure sso
aws sso login
```

---

# 🪣 10. Primeiro recurso: Bucket S3

O S3 é um serviço de armazenamento da AWS.

Exemplo:

```hcl
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "rocketseat-bucket-iac"

  tags = {
    Name = "Primeiro Bucket"
    IAC  = "true"
  }
}
```

Criar:

```bash
terraform validate
terraform plan
terraform apply
```

Resultado esperado:

```txt
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

---

# 🏷️ 11. Por que usar tags?

Tags ajudam a organizar e identificar recursos.

Exemplo:

```hcl
tags = {
  Name = "Primeiro Bucket"
  IAC  = "true"
}
```

A tag `IAC = true` indica que o recurso é gerenciado por código.

---

# ✏️ 12. Alterando recurso

Para alterar, mude o código e rode novamente:

```bash
terraform plan
terraform apply
```

Exemplo: adicionar uma tag.

```hcl
tags = {
  Name  = "Primeiro Bucket"
  IAC   = "true"
  Teste = "true"
}
```

O Terraform entende que não precisa criar outro bucket, apenas alterar.

```txt
Plan: 0 to add, 1 to change, 0 to destroy.
```

---

# 🗑️ 13. Destruindo recurso

Planejar destruição:

```bash
terraform plan -destroy
```

Aplicar destruição:

```bash
terraform apply -destroy
```

Ou:

```bash
terraform destroy
```

⚠️ Cuidado: isso remove recursos reais da AWS.

---

# 🧾 14. Terraform State

O **state** é o arquivo que guarda o que o Terraform sabe sobre a infraestrutura.

Arquivos comuns:

```txt
terraform.tfstate
terraform.tfstate.backup
```

Resumo:

```txt
State = memória do Terraform
```

Ele guarda:

- recursos criados;
- IDs;
- atributos;
- região;
- tags;
- provider usado;
- estado atual conhecido.

---

## ⚠️ Alterar pelo console dá problema

Errado:

```txt
Editar recurso direto no painel da AWS
```

Certo:

```txt
Alterar arquivo .tf
Rodar terraform plan
Rodar terraform apply
```

Motivo: o código deve ser a **fonte da verdade**.

---

# 🧪 15. Workspaces

Workspace separa estados/ambientes.

O padrão é:

```txt
default
```

Comandos úteis:

```bash
terraform workspace show
terraform workspace list
terraform workspace new staging
terraform workspace select staging
terraform workspace select default
```

Exemplo de lista:

```txt
  default
* staging
```

O `*` mostra o workspace atual.

---

# 🧠 16. Workspace no nome do recurso

Problema: bucket S3 precisa ter nome único.

Se usar o mesmo nome em vários workspaces, pode dar erro.

Solução:

```hcl
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "rocketseat-bucket-iac-${terraform.workspace}"

  tags = {
    Name    = "Primeiro Bucket"
    IAC     = "true"
    Context = terraform.workspace
  }
}
```

Resultado:

```txt
rocketseat-bucket-iac-default
rocketseat-bucket-iac-staging
rocketseat-bucket-iac-production
```

---

# 🚨 17. Atenção com recriação

Alguns recursos não aceitam certas alterações.

Exemplo: renomear bucket S3 pode exigir:

```txt
destroy antigo
create novo
```

Antes de aplicar:

- leia o `terraform plan`;
- veja se haverá `destroy`;
- confirme se existe backup;
- nunca rode às cegas em produção.

---

# ✅ 18. Fluxo mental do Terraform

```txt
1. Escreve o .tf
2. Roda validate
3. Roda plan
4. Revisa o plano
5. Roda apply
6. Infra muda na AWS
7. State é atualizado
```

Para destruir:

```txt
1. Roda plan -destroy
2. Revisa o que será removido
3. Roda apply -destroy
4. Recursos são removidos
5. State é atualizado
```

---

# 🧠 19. Mapa mental rápido

```txt
Terraform
├── Registry
│   ├── Providers
│   ├── Resources
│   └── Modules
│
├── CLI
│   ├── init
│   ├── validate
│   ├── plan
│   ├── apply
│   ├── destroy
│   └── workspace
│
├── AWS
│   ├── Provider
│   ├── AWS CLI
│   ├── SSO
│   └── S3
│
├── State
│   ├── terraform.tfstate
│   ├── backup
│   └── fonte da verdade
│
└── Workspaces
    ├── default
    ├── staging
    └── production
```

---

# 🧰 20. Erros comuns

| Erro                        | Solução                                     |
| --------------------------- | --------------------------------------------- |
| Esqueceu `terraform init` | Rode `terraform init`                       |
| SSO expirou                 | Rode `aws sso login`                        |
| Bucket já existe           | Use nome único ou `${terraform.workspace}` |
| Alterou pelo console        | Volte a alteração para o `.tf`            |
| Rodou destroy sem revisar   | Sempre use `terraform plan -destroy` antes  |

---

# ✅ 21. Checklist de revisão

- [ ] Sei o que é Terraform.
- [ ] Sei o que é provider.
- [ ] Sei o que é resource.
- [ ] Sei o que é module.
- [ ] Sei rodar `terraform init`.
- [ ] Sei rodar `terraform validate`.
- [ ] Sei rodar `terraform plan`.
- [ ] Sei rodar `terraform apply`.
- [ ] Sei o que é AWS SSO.
- [ ] Sei criar um bucket S3.
- [ ] Sei o que é `terraform.tfstate`.
- [ ] Sei o que é workspace.
- [ ] Sei usar `${terraform.workspace}`.
- [ ] Sei por que não devo alterar recurso direto no console.

---

# 🧾 22. Resumo em 4 linhas

Terraform cria infraestrutura usando arquivos `.tf`.

Provider conecta o Terraform com a cloud, resource cria o recurso e module reaproveita código.

State é a memória do Terraform e mostra o que já existe.

Workspaces ajudam a separar ambientes como `default`, `staging` e `production`.

---

# 🎯 Frase para memorizar

```txt
Terraform declara a infraestrutura.
Provider conecta na cloud.
Resource cria o recurso.
State guarda a memória.
Workspace separa ambientes.
```
