# Módulo 03 — Iniciando com Terraform

> Material de estudo sobre o início prático com Terraform no contexto de IaC.
>
> Foco: entender a ferramenta, preparar o ambiente, configurar AWS, criar o primeiro recurso, entender `state` e usar `workspaces`.

---

## TL;DR

Neste trecho do módulo, o foco sai da teoria de IaC e entra na prática com **Terraform**.

Você aprende:

- O que existe dentro do ecossistema do Terraform.
- Para que serve o **Terraform Registry**.
- Diferença entre **provider**, **resource** e **module**.
- Como usar os comandos principais da CLI.
- Como configurar AWS com **SSO**, em vez de chave fixa.
- Como criar, alterar e destruir um bucket S3.
- Como o Terraform controla recursos usando o **state**.
- Como separar ambientes usando **workspaces**.

---

# 1. Visão geral do Terraform

O Terraform é uma ferramenta usada para criar, alterar e remover infraestrutura usando código.

Em vez de criar recursos manualmente no painel da AWS, Azure ou GCP, você escreve arquivos `.tf`.

Exemplo de ideia:

```txt
Eu quero um bucket S3.
Eu quero uma máquina EC2.
Eu quero uma VPC.
Eu quero um cluster Kubernetes.
```

Com Terraform, isso vira código.

---

## 1.1 Onde fica o ecossistema do Terraform?

O principal ponto de consulta é o site/documentação do Terraform.

Nele você encontra:

| Área | Função |
|---|---|
| Documentação | Explica como instalar, configurar e usar |
| Registry | Lista providers e modules disponíveis |
| Comunidade | Fóruns, discussões e suporte |
| GitHub/Bug Tracker | Issues, melhorias e problemas |
| Terraform Cloud | Plataforma da HashiCorp para automação/pipeline de infraestrutura |

---

# 2. Terraform Cloud

O **Terraform Cloud** é uma plataforma para automatizar execuções do Terraform.

Ele pode ser usado em fluxos como:

```txt
Commit no GitHub
      ↓
Pull Request / Merge
      ↓
Pipeline roda Terraform
      ↓
Infraestrutura é criada, alterada ou destruída
```

A ideia dele é funcionar como uma espécie de **CI/CD para infraestrutura**.

Porém, neste momento do módulo, o foco ainda está no uso local do Terraform.

---

# 3. Comunidade e documentação

Um ponto importante ao escolher uma ferramenta de IaC é verificar se ela tem comunidade ativa.

O Terraform possui:

- Fórum da comunidade.
- Repositório no GitHub.
- Bug tracker.
- Documentação ampla.
- Registry com providers e módulos.
- Certificações da HashiCorp.

Isso é importante porque, quando você tiver erro, dúvida ou precisar de exemplo, a chance de encontrar solução é maior.

---

# 4. Terraform Registry

O **Terraform Registry** é como se fosse um “Docker Hub da infraestrutura”.

Só que, em vez de imagens de containers, ele reúne:

- Providers.
- Resources.
- Modules.

---

## 4.1 Provider

O **provider** é o conector entre o Terraform e algum serviço externo.

Exemplos:

| Provider | Para quê serve |
|---|---|
| AWS | Criar recursos na Amazon Web Services |
| Azure | Criar recursos na Microsoft Azure |
| Google Cloud | Criar recursos no GCP |
| Kubernetes | Gerenciar objetos no Kubernetes |
| Helm | Gerenciar charts Helm |
| Datadog | Gerenciar recursos de observabilidade |
| Grafana | Gerenciar dashboards e recursos do Grafana |

Em resumo:

```txt
Provider = quem o Terraform vai controlar
```

Exemplo de provider AWS:

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

---

## 4.2 Resource

O **resource** é o recurso real que será criado dentro de um provider.

Exemplos na AWS:

| Resource | O que cria |
|---|---|
| `aws_s3_bucket` | Bucket S3 |
| `aws_instance` | Máquina EC2 |
| `aws_vpc` | VPC |
| `aws_security_group` | Security Group |
| `aws_iam_user` | Usuário IAM |

Em resumo:

```txt
Resource = o que será criado, alterado ou removido
```

Exemplo de bucket S3:

```hcl
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "meu-primeiro-bucket-iac"

  tags = {
    Name = "Primeiro Bucket"
    IAC  = "true"
  }
}
```

---

## 4.3 Module

O **module** é um conjunto pronto ou reutilizável de configurações Terraform.

Ele serve para evitar repetição e simplificar recursos complexos.

Exemplos de módulos:

| Module | Para quê serve |
|---|---|
| VPC | Criar rede completa |
| Security Group | Criar regras de segurança |
| EKS | Criar cluster Kubernetes na AWS |
| S3 Bucket | Criar bucket com boas práticas |
| Lambda | Criar funções serverless |

Em resumo:

```txt
Module = template reutilizável
```

Você pode usar módulos públicos do Registry ou criar módulos internos na sua empresa.

---

# 5. Estrutura inicial de projeto Terraform

Uma boa prática é deixar claro no nome do repositório que ele é de infraestrutura.

Exemplos:

```txt
projeto-iac
projeto.infra
sistema-iac
empresa-cloud-infra
```

Estrutura inicial simples:

```txt
projeto-iac/
├── providers.tf
├── main.tf
├── variables.tf
├── outputs.tf
└── .gitignore
```

No começo do módulo, a estrutura pode ser mais simples:

```txt
projeto-iac/
├── providers.tf
└── main.tf
```

---

# 6. Arquivos Terraform

Os arquivos Terraform usam extensão:

```txt
.tf
```

O Terraform usa uma linguagem chamada **HCL**, que significa:

```txt
HashiCorp Configuration Language
```

Ela lembra JSON, mas não é JSON.

Exemplo:

```hcl
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "meu-bucket"

  tags = {
    Name = "Meu bucket"
    IAC  = "true"
  }
}
```

---

# 7. Principais comandos da CLI do Terraform

A CLI do Terraform é usada no terminal.

Os comandos principais vistos no módulo são:

| Comando | Função |
|---|---|
| `terraform init` | Inicializa o projeto |
| `terraform validate` | Valida sintaxe dos arquivos `.tf` |
| `terraform plan` | Mostra o que será criado, alterado ou destruído |
| `terraform apply` | Aplica as mudanças na infraestrutura |
| `terraform destroy` | Destrói recursos gerenciados |
| `terraform workspace` | Gerencia workspaces |

---

## 7.1 `terraform init`

Inicializa o projeto Terraform.

Ele baixa providers, plugins e prepara o diretório.

```bash
terraform init
```

Quando rodado em um diretório vazio, ele apenas inicializa sem muita coisa.

Quando já existe um provider configurado, ele baixa o provider necessário.

Depois do `init`, podem aparecer arquivos/pastas como:

```txt
.terraform/
.terraform.lock.hcl
```

---

## 7.2 `terraform validate`

Valida se a estrutura dos arquivos `.tf` está correta.

```bash
terraform validate
```

Se estiver certo, ele retorna algo parecido com:

```txt
Success! The configuration is valid.
```

Esse comando ajuda a pegar erros de sintaxe antes de tentar criar algo na nuvem.

---

## 7.3 `terraform plan`

Mostra o plano de execução.

```bash
terraform plan
```

Ele informa o que será:

- Adicionado.
- Alterado.
- Destruído.

Exemplo de saída conceitual:

```txt
Plan: 1 to add, 0 to change, 0 to destroy.
```

Esse comando é essencial porque permite revisar antes de aplicar.

---

## 7.4 `terraform apply`

Aplica as mudanças na infraestrutura.

```bash
terraform apply
```

Por padrão, ele pede confirmação:

```txt
Do you want to perform these actions?
Enter a value:
```

Você confirma digitando:

```txt
yes
```

Também é possível usar:

```bash
terraform apply -auto-approve
```

Isso aplica sem perguntar.

A boa prática é:

```bash
terraform plan
terraform apply -auto-approve
```

---

## 7.5 `terraform destroy`

Remove os recursos gerenciados pelo Terraform.

```bash
terraform destroy
```

Também é possível planejar uma destruição antes:

```bash
terraform plan -destroy
```

Ou aplicar destruição com:

```bash
terraform apply -destroy
```

Com confirmação automática:

```bash
terraform apply -destroy -auto-approve
```

⚠️ Cuidado: esse comando realmente remove recursos da nuvem.

---

# 8. Configurando o provider AWS

O arquivo `providers.tf` pode conter a configuração do provider.

Exemplo:

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

Depois disso, rode:

```bash
terraform init
```

O Terraform vai baixar o provider da AWS.

---

# 9. AWS CLI e autenticação

Para o Terraform criar recursos na AWS, ele precisa conseguir se autenticar.

Existem duas formas comuns:

| Forma | Característica |
|---|---|
| Access Key / Secret Key | Mais simples, mas menos segura |
| AWS SSO / IAM Identity Center | Mais segura e recomendada no módulo |

O módulo segue pela opção mais segura: **SSO**.

---

# 10. AWS SSO / IAM Identity Center

O **SSO** significa **Single Sign-On**.

Na AWS, isso é feito pelo **IAM Identity Center**.

A ideia é criar uma forma de login temporária e mais segura.

Vantagens:

- Token temporário.
- Expiração da sessão.
- MFA obrigatório.
- Melhor controle de acesso.
- Evita deixar Access Key fixa na máquina.

---

## 10.1 Passos gerais para configurar SSO

Fluxo geral:

```txt
AWS Console
    ↓
IAM Identity Center
    ↓
Enable
    ↓
Criar usuário
    ↓
Criar Permission Set
    ↓
Associar permissão ao usuário
    ↓
Configurar AWS CLI local
```

---

## 10.2 Comando de configuração inicial

Para configurar pela primeira vez:

```bash
aws configure sso
```

Ele pede informações como:

- Nome da sessão.
- URL inicial do SSO.
- Região.
- Escopo.
- Conta AWS.
- Permission Set.
- Região default.
- Formato de output.

Exemplo conceitual:

```bash
aws configure sso
```

Depois disso, o navegador abre para autenticação.

---

## 10.3 Login depois de já configurado

Depois que o SSO já foi configurado, você não precisa rodar `aws configure sso` de novo.

Use:

```bash
aws sso login
```

Esse comando renova o login local.

---

## 10.4 Tempo de sessão

No exemplo do módulo, a sessão tem duração de **8 horas**.

Depois disso, é necessário logar novamente:

```bash
aws sso login
```

Isso é melhor do que ter uma chave permanente na máquina.

---

# 11. Configuração do VS Code

Para melhorar a produtividade, o módulo recomenda instalar uma extensão de Terraform no VS Code.

Ela ajuda com:

- Highlight de sintaxe.
- Ícone de arquivos `.tf`.
- Um pouco de autocomplete.
- Validação básica.

Exemplo de arquivo:

```txt
main.tf
providers.tf
module.tf
```

Quando a extensão está correta, o VS Code reconhece os arquivos Terraform.

---

# 12. Criando o primeiro recurso: Bucket S3

O primeiro recurso criado no módulo é um bucket S3.

O S3 é um serviço de armazenamento da AWS.

Ele pode guardar:

- Arquivos.
- Imagens.
- Backups.
- Logs.
- Objetos em geral.

---

## 12.1 Exemplo de `main.tf`

```hcl
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "rocketseat-bucket-iac"

  tags = {
    Name = "Primeiro Bucket"
    IAC  = "true"
  }
}
```

Explicando:

| Parte | Significado |
|---|---|
| `resource` | Indica que será criado um recurso |
| `aws_s3_bucket` | Tipo do recurso |
| `s3_bucket` | Nome interno/alias no Terraform |
| `bucket` | Nome real do bucket na AWS |
| `tags` | Metadados para organização |

---

## 12.2 Fluxo correto para criar

```bash
terraform validate
terraform plan
terraform apply
```

Ou, depois de revisar o `plan`:

```bash
terraform apply -auto-approve
```

---

## 12.3 Resultado esperado

Depois do `apply`, o bucket aparece no painel da AWS.

Exemplo de saída conceitual:

```txt
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

---

# 13. Alterando o recurso

Depois de criado, o recurso pode ser alterado pelo código.

Exemplo: adicionar tags.

```hcl
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "rocketseat-bucket-iac"

  tags = {
    Name  = "Primeiro Bucket"
    IAC   = "true"
    Teste = "true"
  }
}
```

Depois rode:

```bash
terraform plan
terraform apply
```

O Terraform detecta que não precisa criar outro bucket, apenas alterar o existente.

Saída conceitual:

```txt
Plan: 0 to add, 1 to change, 0 to destroy.
```

---

# 14. Destruindo o recurso

Para remover o bucket:

```bash
terraform plan -destroy
terraform apply -destroy
```

Ou:

```bash
terraform destroy
```

Com confirmação automática:

```bash
terraform apply -destroy -auto-approve
```

Saída conceitual:

```txt
Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

---

# 15. Tag `IAC = true`

Uma boa prática mostrada no módulo é marcar recursos criados por IaC.

Exemplo:

```hcl
tags = {
  Name = "Primeiro Bucket"
  IAC  = "true"
}
```

Por quê?

Porque ajuda a identificar quais recursos são gerenciados por código.

Isso é útil quando a empresa está migrando aos poucos para IaC.

Exemplo:

| Recurso | Gerenciado por IaC? |
|---|---|
| Bucket A | Sim |
| EC2 antiga | Não |
| VPC nova | Sim |
| Banco antigo | Não |

---

# 16. Terraform State

O **state** é um dos conceitos mais importantes do Terraform.

Ele é o arquivo que registra o estado atual da infraestrutura.

Arquivo comum:

```txt
terraform.tfstate
```

Backup:

```txt
terraform.tfstate.backup
```

O state guarda informações como:

- Recursos criados.
- IDs dos recursos.
- Atributos gerados.
- Região.
- Tags.
- Nome do provider.
- Estado atual conhecido pelo Terraform.

---

## 16.1 Para que serve o state?

O Terraform usa o state para responder:

```txt
Esse recurso já existe?
Precisa criar?
Precisa alterar?
Precisa destruir?
O que mudou fora do Terraform?
```

Sem o state, o Terraform não teria como comparar o código com a infraestrutura real.

---

## 16.2 Exemplo prático de funcionamento

Imagine que o código diz:

```hcl
tags = {
  Name = "Primeiro Bucket"
  IAC  = "true"
}
```

Mas alguém vai no console da AWS e adiciona manualmente:

```txt
Test = true
```

Quando você roda:

```bash
terraform plan
```

O Terraform percebe a diferença.

Ele compara:

```txt
Código Terraform
      ↓
State
      ↓
Infraestrutura real na AWS
```

Se algo foi alterado manualmente, ele tenta voltar ao que está no código.

---

## 16.3 Fonte da verdade

No IaC, a fonte da verdade deve ser o repositório/código.

Não o console da AWS.

Errado:

```txt
Editar recurso manualmente no painel da AWS
```

Certo:

```txt
Alterar o arquivo .tf
Rodar terraform plan
Rodar terraform apply
```

---

## 16.4 State local não é ideal para produção

No início do estudo, o state fica local.

Mas, em ambientes reais, não é boa prática manter apenas localmente.

O ideal é usar um backend remoto, como:

```txt
S3 + DynamoDB
Terraform Cloud
Azure Storage
GCS
```

Motivo:

- Evita perda do state.
- Permite colaboração.
- Evita conflito entre pessoas.
- Melhora segurança.
- Centraliza o estado da infraestrutura.

---

# 17. Workspaces

Workspace significa espaço de trabalho.

Por padrão, todo projeto Terraform começa no workspace:

```txt
default
```

Para ver o workspace atual:

```bash
terraform workspace show
```

---

## 17.1 Comandos de workspace

| Comando | Função |
|---|---|
| `terraform workspace show` | Mostra workspace atual |
| `terraform workspace list` | Lista workspaces |
| `terraform workspace new staging` | Cria workspace |
| `terraform workspace select staging` | Seleciona workspace |
| `terraform workspace delete staging` | Remove workspace |

---

## 17.2 Criando workspace

```bash
terraform workspace new staging
```

Depois disso, o Terraform já muda para o workspace criado.

Para confirmar:

```bash
terraform workspace show
```

Resultado:

```txt
staging
```

---

## 17.3 Listando workspaces

```bash
terraform workspace list
```

Exemplo:

```txt
  default
* staging
```

O asterisco `*` mostra o workspace atual.

---

## 17.4 Selecionando workspace

```bash
terraform workspace select default
```

ou:

```bash
terraform workspace select staging
```

---

# 18. Workspace e state

Cada workspace possui seu próprio state.

No workspace `default`, o state fica em:

```txt
terraform.tfstate
```

Em outros workspaces, pode aparecer algo como:

```txt
terraform.tfstate.d/
└── staging/
    └── terraform.tfstate
```

Isso permite separar estados diferentes.

---

# 19. Problema comum com workspaces

Se você usar o mesmo nome de bucket em dois workspaces, pode dar erro.

Exemplo:

```hcl
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "rocketseat-bucket-iac"
}
```

Se criar no workspace `staging` e depois tentar criar no `default`, o Terraform pode tentar criar o mesmo bucket de novo.

Na AWS, nomes de bucket S3 precisam ser únicos.

Erro comum:

```txt
409 Conflict
Bucket already exists
```

---

# 20. Usando o nome do workspace no recurso

Para evitar conflito, você pode usar o nome do workspace no bucket.

Exemplo:

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

Assim, o Terraform cria buckets diferentes:

```txt
rocketseat-bucket-iac-default
rocketseat-bucket-iac-staging
rocketseat-bucket-iac-production
```

---

# 21. Atenção: alguns recursos são recriados

Nem todo recurso aceita alteração de nome.

No caso do S3 Bucket, alterar o nome pode exigir recriação.

Isso significa:

```txt
Destroy antigo
Create novo
```

Ou seja, o Terraform pode destruir e criar novamente.

⚠️ Cuidado com recursos que possuem dados importantes.

Antes de renomear ou recriar:

- Verifique backup.
- Leia o `terraform plan`.
- Confirme se o recurso pode ser destruído.
- Nunca rode `apply` no automático sem revisar em produção.

---

# 22. Fluxo mental do Terraform

Pense assim:

```txt
1. Escrevo o código .tf
2. Rodo terraform validate
3. Rodo terraform plan
4. Reviso o que vai acontecer
5. Rodo terraform apply
6. Terraform atualiza a infraestrutura
7. Terraform atualiza o state
```

Para destruir:

```txt
1. Rodo terraform plan -destroy
2. Reviso o que será destruído
3. Rodo terraform apply -destroy
4. Terraform remove os recursos
5. Terraform atualiza o state
```

---

# 23. Fluxo visual

```txt
Código Terraform
      ↓
terraform validate
      ↓
terraform plan
      ↓
terraform apply
      ↓
Provider AWS
      ↓
Recurso criado/alterado/removido
      ↓
terraform.tfstate atualizado
```

---

# 24. Diferença entre provider, resource, module, state e workspace

| Conceito | Explicação simples |
|---|---|
| Provider | Serviço que o Terraform controla |
| Resource | Recurso criado dentro do provider |
| Module | Pacote/template reutilizável |
| State | Arquivo que guarda o estado da infra |
| Workspace | Separação lógica de estados/ambientes |

---

# 25. Exemplo completo do início

## `providers.tf`

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

## `main.tf`

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

## Comandos

```bash
terraform init
terraform validate
terraform workspace new staging
terraform plan
terraform apply -auto-approve
terraform workspace select default
terraform plan
terraform apply -auto-approve
```

---

# 26. Boas práticas vistas no módulo

## Organização

- Criar repositório separado para infraestrutura.
- Usar nomes como `projeto-iac` ou `projeto-infra`.
- Separar provider e resources em arquivos diferentes.
- Usar tags para identificar recursos.

## Segurança

- Preferir AWS SSO em vez de Access Key fixa.
- Usar MFA.
- Evitar credenciais permanentes.
- Não alterar recurso manualmente no console.

## Execução

- Rodar `validate` antes.
- Rodar `plan` antes do `apply`.
- Ler o plano com atenção.
- Tomar cuidado com `destroy`.
- Não usar `-auto-approve` em produção sem revisão.

## State

- Entender que o state é crítico.
- Não perder o arquivo state.
- Não editar o state manualmente.
- Em produção, usar backend remoto.

---

# 27. Erros comuns

## 1. Esquecer de rodar `terraform init`

Erro comum quando o provider ainda não foi baixado.

Correção:

```bash
terraform init
```

---

## 2. Não estar logado na AWS

Se o SSO expirou, o Terraform não consegue autenticar.

Correção:

```bash
aws sso login
```

---

## 3. Bucket já existe

Nomes de buckets S3 precisam ser únicos.

Correção:

```hcl
bucket = "meu-bucket-${terraform.workspace}"
```

Ou use um nome globalmente único.

---

## 4. Alterar recurso pelo console

Isso quebra a ideia de fonte única da verdade.

Correção:

- Alterar pelo `.tf`.
- Rodar `terraform plan`.
- Rodar `terraform apply`.

---

## 5. Rodar `destroy` sem revisar

Pode apagar recursos importantes.

Correção:

```bash
terraform plan -destroy
```

Leia antes de aplicar.

---

# 28. Checklist de revisão rápida

Marque se você entendeu:

- [ ] O que é Terraform.
- [ ] O que é Terraform Registry.
- [ ] O que é provider.
- [ ] O que é resource.
- [ ] O que é module.
- [ ] Como rodar `terraform init`.
- [ ] Como rodar `terraform validate`.
- [ ] Como rodar `terraform plan`.
- [ ] Como rodar `terraform apply`.
- [ ] Como rodar `terraform destroy`.
- [ ] Como configurar AWS SSO.
- [ ] Por que SSO é melhor que chave fixa.
- [ ] Como criar bucket S3.
- [ ] Como adicionar tags.
- [ ] O que é `terraform.tfstate`.
- [ ] O que é workspace.
- [ ] Como usar `terraform.workspace`.
- [ ] Por que evitar alterações manuais no console.

---

# 29. Mapa mental em texto

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
│   ├── Provider AWS
│   ├── AWS CLI
│   ├── SSO
│   ├── MFA
│   └── S3 Bucket
│
├── State
│   ├── terraform.tfstate
│   ├── backup
│   ├── fonte da verdade
│   └── backend remoto no futuro
│
└── Workspaces
    ├── default
    ├── staging
    ├── production
    └── terraform.workspace
```

---

# 30. Resumo em 4 linhas

Terraform transforma infraestrutura em código.  
Provider conecta o Terraform à nuvem, resource cria o recurso e module reaproveita templates.  
O `state` guarda o que existe e permite saber se precisa criar, alterar ou destruir.  
Workspaces ajudam a separar ambientes como `default`, `staging` e `production`.

---

# 31. Próximo passo sugerido

Depois deste conteúdo, o próximo assunto natural é estudar:

```txt
variables
outputs
data sources
remote state
backend S3
módulos próprios
```

Esses tópicos deixam o Terraform mais profissional e mais próximo de um ambiente real.
