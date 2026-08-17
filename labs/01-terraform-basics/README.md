# 🧪 Lab 01 — Terraform Basics

Primeiro laboratório prático da trilha DevOps.

## Objetivo

Executar o ciclo básico do Terraform sem criar recursos em cloud e sem gerar custo.

O laboratório usa o provider `hashicorp/local` para criar um arquivo local a partir de uma configuração Terraform.

## O que você pratica

- `terraform init`
- `terraform fmt`
- `terraform validate`
- `terraform plan`
- `terraform apply`
- variáveis
- outputs
- state
- `terraform destroy`

## Estrutura

```text
01-terraform-basics/
├── .gitignore
├── README.md
├── main.tf
├── outputs.tf
└── variables.tf
```

## Executar

Entre nesta pasta:

```bash
cd labs/01-terraform-basics
```

Inicialize o Terraform:

```bash
terraform init
```

Formate e valide:

```bash
terraform fmt
terraform validate
```

Visualize o plano:

```bash
terraform plan
```

Aplique:

```bash
terraform apply
```

Confirme com `yes` quando solicitado.

## Resultado esperado

Após o `apply`, o Terraform cria:

```text
devops-lab-output.txt
```

O conteúdo padrão é definido em `variables.tf`.

Para testar outra mensagem:

```bash
terraform apply -var="message=Infraestrutura como código na prática"
```

## Consultar outputs

```bash
terraform output
```

## Limpeza

```bash
terraform destroy
```

Como o recurso é apenas um arquivo local, o laboratório não utiliza conta cloud nem gera cobrança.

## Segurança

Este lab não usa tokens, chaves de API ou credenciais. Arquivos de state e diretórios locais do Terraform estão ignorados pelo Git.
