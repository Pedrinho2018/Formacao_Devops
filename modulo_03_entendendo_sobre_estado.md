# Módulo 03 — Entendendo sobre Estado no Terraform

> Material de estudo sobre **Terraform State**, estado local, estado remoto, backup, backend S3, versionamento, `destroy`, `.gitignore` e `tfvars`.

---

## TL;DR

O **estado** é o arquivo que o Terraform usa para saber **o que existe na infraestrutura** e **o que precisa mudar**.

Sem o estado, o Terraform fica “cego”.

Ele compara:

```text
Código .tf  +  terraform.tfstate  +  infraestrutura real na cloud
```

E decide se precisa:

```text
criar → alterar → deletar → não fazer nada
```

---

# 1. O que é o Terraform State?

O **Terraform State** é o controle interno do Terraform.

Ele normalmente aparece como:

```text
terraform.tfstate
```

Esse arquivo guarda informações dos recursos criados, como:

```text
nome do bucket
ARN
região
ID do recurso
domain name
tags
provider usado
módulo de origem
```

Exemplo mental:

```text
Código Terraform:
"quero um bucket S3 chamado empresa-state"

AWS:
bucket criado de verdade

terraform.tfstate:
registro dizendo que esse bucket existe e pertence ao Terraform
```

---

# 2. Por que o estado é tão importante?

Porque o Terraform precisa saber se um recurso:

```text
já existe
não existe
foi alterado
precisa ser recriado
precisa ser destruído
```

Exemplo:

Você cria um bucket S3 via Terraform.

Depois roda:

```bash
terraform plan
```

Se nada mudou, ele responde algo parecido com:

```text
No changes.
```

Agora, se você alterar alguma coisa no código, por exemplo uma tag, o Terraform compara o código com o estado e mostra o que será alterado.

---

# 3. O estado é a fonte da verdade?

Na prática, sim.

O Terraform trabalha comparando:

```text
código declarativo
estado salvo
infraestrutura real no provider
```

Se alguém altera um recurso direto no console da AWS, sem passar pelo Terraform, acontece uma **dissonância de estado**.

## Exemplo

No código existe:

```hcl
tags = {
  iac = "true"
}
```

Mas alguém entra na AWS e adiciona manualmente:

```text
teste = true
```

Quando rodar:

```bash
terraform plan
```

O Terraform percebe que existe algo fora do código e tenta voltar para o que está declarado.

Ou seja:

```text
O console da AWS não deve ser o lugar principal de alteração.
O repositório Terraform deve ser a fonte principal.
```

---

# 4. Quando o estado é alterado?

O estado é alterado quando o Terraform aplica uma mudança com sucesso usando:

```bash
terraform apply
```

O `plan` não altera o estado. Ele só simula e mostra o que será feito.

```bash
terraform plan
```

Pense assim:

```text
terraform plan  = prévia
terraform apply = execução real
```

---

# 5. Estado local

Por padrão, o Terraform cria o estado localmente.

Exemplo:

```text
projeto-iac/
├── main.tf
├── providers.tf
├── terraform.tfstate
└── terraform.tfstate.backup
```

Quando usa workspace, pode aparecer assim:

```text
terraform.tfstate.d/
└── staging/
    ├── terraform.tfstate
    └── terraform.tfstate.backup
```

## Problema do estado local

O estado local é ruim para trabalho em equipe.

Porque:

```text
fica preso na sua máquina
pode ser perdido
pode gerar conflito
não funciona bem em pipeline
pode conter informação sensível
não deve ir para o GitHub
```

---

# 6. Arquivo `terraform.tfstate.backup`

O backup é uma cópia da versão anterior do estado.

Exemplo:

```text
terraform.tfstate        → estado atual
terraform.tfstate.backup → estado anterior
```

Se você aplica uma mudança, o Terraform atualiza o `terraform.tfstate` e guarda a versão antiga no backup.

## Para que serve?

Serve como segurança caso o estado atual seja corrompido ou dê algum problema.

Exemplo mental:

```text
Antes:
estado tinha 1 bucket

Depois do apply:
estado atual tem 2 buckets
backup ainda guarda a versão com 1 bucket
```

---

# 7. Comandos para olhar o estado

O Terraform tem comandos específicos para estado.

## Listar recursos no estado

```bash
terraform state list
```

Mostra os recursos que o Terraform conhece.

Exemplo:

```text
module.s3.aws_s3_bucket.bucket
module.cloudfront.aws_cloudfront_distribution.cloudfront
```

## Mostrar detalhes de um recurso

```bash
terraform state show module.s3.aws_s3_bucket.bucket
```

Mostra os atributos daquele recurso no estado.

## Outros comandos avançados

```bash
terraform state mv
terraform state pull
terraform state push
terraform state rm
```

Uso rápido:

| Comando | Função |
|---|---|
| `state list` | Lista recursos no estado |
| `state show` | Mostra detalhes de um recurso |
| `state mv` | Move recurso dentro do estado |
| `state pull` | Baixa estado atual |
| `state push` | Envia estado manualmente |
| `state rm` | Remove recurso do estado |

Atenção: mexer manualmente no estado é avançado. Use com cuidado.

---

# 8. Estado remoto

A boa prática é guardar o estado remotamente.

No módulo, o exemplo usa:

```text
AWS S3 como backend remoto
```

Assim, o estado deixa de ficar só na máquina local e passa a ficar em um bucket S3.

## Vantagens

```text
melhor para equipe
melhor para pipeline CI/CD
mais seguro
mais fácil de versionar
menos dependência da máquina local
```

---

# 9. Criando um bucket para o estado

Exemplo de recurso para criar o bucket do estado:

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

Isso impede que o Terraform destrua esse bucket acidentalmente.

Por quê?

Porque esse bucket guarda o estado.

Se ele for apagado, você pode perder o controle da infraestrutura.

---

# 10. Variável para o bucket de estado

Arquivo:

```text
variables.tf
```

Exemplo:

```hcl
variable "state_bucket" {
  type        = string
  default     = "rocketseat-state-bucket-tf"
  description = "Bucket com o estado remoto do Terraform"
}
```

Uso:

```hcl
bucket = var.state_bucket
```

---

# 11. Configurando backend remoto com S3

No bloco `terraform`, você configura o backend:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket  = "rocketseat-state-bucket-tf"
    key     = "terraform.tfstate"
    region  = "us-east-2"
    encrypt = true
  }
}
```

## Explicando cada campo

| Campo | Função |
|---|---|
| `bucket` | Nome do bucket S3 onde o state ficará |
| `key` | Caminho/nome do arquivo do estado |
| `region` | Região da AWS |
| `encrypt` | Criptografa o arquivo no S3 |

Importante: no bloco `backend`, normalmente você não usa variável diretamente. Por isso o nome do bucket costuma ficar fixo nessa configuração.

---

# 12. Depois de configurar o backend

Sempre que mexer no backend, rode:

```bash
terraform init
```

O Terraform vai perceber que você saiu do backend local para o backend remoto.

Ele pode perguntar algo como:

```text
Do you want to copy existing state to the new backend?
```

Resposta comum:

```text
yes
```

Isso migra o estado local para o S3.

---

# 13. Como fica o estado remoto com workspace?

Se você usa workspace, o Terraform organiza o state no bucket considerando o ambiente.

Exemplo:

```text
env:/
└── staging/
    └── terraform.tfstate
```

Então, se você usa o workspace `staging`, o estado desse ambiente fica separado.

---

# 14. Versionamento do bucket de estado

Como o estado é sensível e muito importante, é boa prática ativar versionamento no bucket.

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

## Por que ativar versionamento?

Porque cada alteração no arquivo `terraform.tfstate` gera uma versão.

Se algo der ruim, você consegue voltar uma versão anterior no S3.

---

# 15. `depends_on`

O `depends_on` força uma ordem de criação.

Exemplo:

```hcl
depends_on = [
  aws_s3_bucket.terraform_state
]
```

Tradução:

```text
Só configure o versionamento depois que o bucket existir.
```

Isso evita erro de dependência.

---

# 16. Destroy no Terraform

O comando de destruição remove recursos da infraestrutura.

Existem duas formas principais:

```bash
terraform destroy
```

ou:

```bash
terraform apply -destroy
```

Antes de destruir, o ideal é sempre rodar:

```bash
terraform plan -destroy
```

Assim você vê o que será apagado antes.

---

# 17. Cuidado: `destroy` apaga tudo do escopo

Se você rodar:

```bash
terraform destroy
```

O Terraform tenta destruir tudo que está naquele estado.

Então, se o repositório tem:

```text
S3
CloudFront
SQS
DLQ
IAM
VPC
```

Ele vai tentar apagar tudo.

Por isso, muito cuidado.

---

# 18. Destroy com `target`

Se você quer destruir só um recurso específico, use `--target`.

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

## O que o `target` faz?

Ele limita o escopo da operação.

Em vez de destruir tudo, ele tenta destruir só o recurso indicado.

Mesmo assim, atenção: se outro recurso depende dele, o Terraform pode precisar alterar ou destruir recursos relacionados.

---

# 19. `.gitignore` para Terraform

O estado não deve ser enviado para o GitHub.

Crie um `.gitignore`:

```gitignore
# Terraform local files
.terraform/*
*.tfstate
*.tfstate.*

# Terraform variables
*.tfvars

# Crash logs
crash.log
crash.*.log

# Override files
override.tf
override.tf.json
*_override.tf
*_override.tf.json
```

## Por que ignorar `tfstate`?

Porque pode conter:

```text
IDs internos
nomes de recursos
informações sensíveis
estrutura real da infra
outputs
dados de providers
```

## Por que ignorar `.terraform/`?

Porque é pasta local de inicialização/cache/plugin.

Ela pode ser reconstruída com:

```bash
terraform init
```

---

# 20. O arquivo `.terraform.lock.hcl`

Diferente do `tfstate`, o lock pode ser versionado.

Ele ajuda a travar versões dos providers usados.

Exemplo:

```text
.terraform.lock.hcl
```

Ele melhora a consistência entre máquinas e pipelines.

---

# 21. `terraform.tfvars`

O `tfvars` serve para sobrescrever valores de variáveis.

Exemplo de variável:

```hcl
variable "state_bucket" {
  type        = string
  default     = "rocketseat-state-bucket-tf"
  description = "Bucket com o estado remoto do Terraform"
}
```

Arquivo:

```text
terraform.tfvars
```

Conteúdo:

```hcl
state_bucket = "meu-bucket-de-state"
```

O valor do `tfvars` sobrescreve o `default`.

---

# 22. `tfvars` é parecido com `.env`

Pense assim:

```text
variables.tf       → declara quais variáveis existem
terraform.tfvars   → define valores reais dessas variáveis
```

Comparação:

```text
.env está para aplicação
tfvars está para Terraform
```

Mas cuidado: `tfvars` não deve ser enviado para o Git se tiver dados sensíveis.

---

# 23. Fluxo recomendado do módulo

## Primeira vez

```bash
terraform init
```

## Validar sintaxe

```bash
terraform validate
```

## Formatador

```bash
terraform fmt
```

## Ver plano

```bash
terraform plan
```

## Aplicar

```bash
terraform apply
```

## Ver estado

```bash
terraform state list
```

## Planejar destruição

```bash
terraform plan -destroy
```

## Destruir com cuidado

```bash
terraform destroy
```

---

# 24. Fluxo visual

```text
1. Escreve código .tf
        ↓
2. terraform validate
        ↓
3. terraform fmt
        ↓
4. terraform plan
        ↓
5. Terraform compara:
   código + state + cloud
        ↓
6. terraform apply
        ↓
7. Recurso criado/alterado/deletado
        ↓
8. terraform.tfstate atualizado
```

---

# 25. Estado local vs remoto

| Tipo | Onde fica | Uso recomendado |
|---|---|---|
| Local | Na sua máquina | Estudo/testes simples |
| Remoto | S3, Azure Blob, GCS etc. | Projeto real, equipe, pipeline |

---

# 26. Boas práticas

## Faça

```text
use backend remoto
ative versionamento no bucket do state
use prevent_destroy no bucket do state
rode plan antes do apply
rode plan -destroy antes do destroy
ignore tfstate no Git
versione .terraform.lock.hcl
use tags como iac = true
```

## Evite

```text
alterar recurso manualmente no console
comitar terraform.tfstate
comitar terraform.tfvars sensível
rodar destroy sem plan antes
usar target sem entender dependências
deixar state só local em projeto real
```

---

# 27. Erros comuns

## 1. Comitar `terraform.tfstate`

Erro grave. Pode expor estrutura da infra.

## 2. Apagar o bucket do state

Pode fazer você perder o controle da infraestrutura.

Use:

```hcl
prevent_destroy = true
```

## 3. Alterar recurso manualmente na AWS

Isso cria diferença entre:

```text
código
estado
infra real
```

## 4. Rodar `terraform destroy` sem conferir

Pode apagar tudo do projeto.

## 5. Esquecer `terraform init` depois de mudar backend

Sempre que mudar backend ou módulo:

```bash
terraform init
```

---

# 28. Exemplo completo — Backend S3

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket  = "rocketseat-state-bucket-tf"
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
  default     = "rocketseat-state-bucket-tf"
  description = "Bucket com o estado remoto do Terraform"
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

# 29. Checklist de revisão

Marque mentalmente:

```text
[ ] Sei o que é terraform.tfstate
[ ] Sei por que o state não vai para o Git
[ ] Sei a diferença entre state local e remoto
[ ] Sei para que serve o terraform.tfstate.backup
[ ] Sei configurar backend S3
[ ] Sei por que usar encrypt = true
[ ] Sei por que ativar versionamento no bucket
[ ] Sei usar prevent_destroy
[ ] Sei rodar terraform state list
[ ] Sei usar plan -destroy antes do destroy
[ ] Sei o risco do terraform destroy
[ ] Sei usar --target com cuidado
[ ] Sei para que serve terraform.tfvars
[ ] Sei configurar .gitignore para Terraform
```

---

# 30. Resumo final

O **Terraform State** é o mapa da sua infraestrutura.

Ele registra tudo que o Terraform criou, alterou ou removeu. Por isso, o arquivo `terraform.tfstate` é extremamente importante e não deve ser enviado para o Git.

Em projeto real, o ideal é usar **estado remoto**, como um bucket S3, com criptografia e versionamento ativados.

Também é importante proteger esse bucket com `prevent_destroy`, porque se ele for apagado você pode perder a referência do que existe na infraestrutura.

Para apagar recursos, use `destroy` com muito cuidado. Sempre rode `terraform plan -destroy` antes e, se quiser apagar apenas um recurso específico, use `--target`.

---

## Resumo de 4 linhas

Terraform usa o `terraform.tfstate` para saber o que existe na infraestrutura.  
Esse estado não deve ser comitado no Git, porque pode ser sensível.  
Em projetos reais, use backend remoto no S3 com versionamento e criptografia.  
Cuidado com `destroy`: ele pode apagar tudo se você não limitar o escopo.
