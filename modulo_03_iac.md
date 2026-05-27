# 🚀 Módulo 03 — IaC: Infrastructure as Code

> Resumo simples, direto e mais curto para revisar no Notion/GitHub.

---

## ⚡ TL;DR

**IaC** significa **Infrastructure as Code**: criar, alterar e remover infraestrutura usando código.

Em vez de clicar no console da AWS/Azure/GCP, você escreve arquivos `.tf`, versiona no Git e usa uma ferramenta como o **Terraform** para aplicar tudo.

A ideia principal do módulo é:

```text
Infra manual no console ❌
Infra declarada em código ✅
```

---

## 🧠 1. O que é IaC?

IaC é transformar infraestrutura em código.

Você descreve recursos como:

- 🖥️ máquinas virtuais;
- 🌐 redes;
- 📦 buckets;
- 🗄️ bancos de dados;
- 🔐 permissões;
- ☁️ serviços de cloud.

Exemplo mental:

```text
Quero um bucket S3 chamado app-storage.
```

Com IaC, isso vira código e não clique manual.

---

## 🎯 2. Qual problema o IaC resolve?

Sem IaC, a infra vira bagunça rápido.

Problemas comuns:

- 💸 recurso esquecido gerando custo;
- 🧱 recurso duplicado;
- 🕵️ ninguém sabe quem alterou;
- ⚠️ alteração manual quebrando produção;
- 🔁 dificuldade para recriar ambiente;
- 📉 dev, homologação e produção diferentes.

Com IaC, você ganha:

- ✅ versionamento;
- ✅ histórico;
- ✅ padronização;
- ✅ revisão por Pull Request;
- ✅ automação;
- ✅ controle melhor de custos;
- ✅ fonte única da verdade.

---

## 🖱️ 3. Console manual vs IaC

### ❌ Sem IaC

```text
Entrar na AWS
→ clicar em EC2
→ criar instância
→ configurar tudo manualmente
```

Funciona, mas não escala bem.

### ✅ Com IaC

```hcl
resource "aws_instance" "app" {
  ami           = "ami-exemplo"
  instance_type = "t2.micro"

  tags = {
    Name = "app-server"
  }
}
```

Você declara o recurso e a ferramenta cria para você.

---

## 📌 4. Conceito mais importante: estado desejado

IaC trabalha com a ideia de **estado desejado**.

Você escreve:

```text
Eu quero que exista uma EC2 t2.micro chamada app-server.
```

A ferramenta compara:

```text
Código declarado
      vs
Infra real na cloud
```

Se estiver diferente, ela ajusta.

---

## 🔁 5. Declarativo vs Imperativo

| Modelo          | Ideia                           | Exemplo                      |
| --------------- | ------------------------------- | ---------------------------- |
| ✅ Declarativo  | Diz**o que** deve existir | “Quero uma EC2”            |
| ⚙️ Imperativo | Diz**como** fazer         | “Execute passo 1, 2, 3...” |

### 🟢 Declarativo

Você descreve o resultado final.

```text
Quero um bucket S3 com estas tags.
```

O Terraform decide como criar.

### 🟡 Imperativo

Você escreve os passos.

```text
1. Criar rede
2. Criar subnet
3. Criar security group
4. Criar EC2
```

Aqui a ordem importa muito.

---

## 🌿 6. O que é GitOps?

**GitOps = Git + Operations**

A ideia é usar o Git como fonte da verdade da infraestrutura.

Fluxo comum:

```text
Código IaC
→ Commit
→ Push
→ Pull Request
→ Revisão
→ Apply/Pipeline
→ Infra criada na cloud
```

Isso evita o clássico:

```text
“Vou só alterar rapidinho no console.”
```

Esse tipo de alteração parece inofensivo, mas pode quebrar tudo depois.

---

## ☁️ 7. Ferramentas citadas no módulo

| Ferramenta                    | Resumo                                 | Ponto de atenção          |
| ----------------------------- | -------------------------------------- | --------------------------- |
| **CloudFormation**      | IaC nativo da AWS                      | Só funciona na AWS         |
| **Pulumi**              | IaC usando Python, TypeScript, Go etc. | Menos popular que Terraform |
| **Terraform**           | IaC multi-cloud com HCL                | Precisa entender state      |
| **Ansible/Chef/Puppet** | Automação/configuração             | Não são o foco do módulo |

---

## 🧩 8. CloudFormation

O **CloudFormation** é a ferramenta de IaC da própria AWS.

Ele cria recursos usando **stacks**.

Exemplo de stack:

```text
Stack app-web
├── EC2
├── S3
├── VPC
└── Load Balancer
```

### ✅ Vantagem

- Forte integração com AWS.

### ❌ Limitação

- Gera **lock-in**, porque só funciona na AWS.

---

## 🧪 9. Pulumi

O **Pulumi** permite escrever infraestrutura usando linguagens conhecidas:

- Python;
- TypeScript;
- Go;
- Java;
- C#;
- YAML.

### ✅ Vantagem

Bom para quem já programa e quer usar uma linguagem conhecida.

### ❌ Por que não foi escolhido?

O módulo preferiu seguir com Terraform por ser mais popular, mais usado no mercado e mais dominante em IaC.

---

## 🏗️ 10. Terraform

O **Terraform** é a ferramenta principal do módulo.

Ele é usado para criar, alterar e destruir infraestrutura como código.

### Por que Terraform?

- 🌎 é multi-cloud;
- 📦 usa providers;
- 🧠 é declarativo;
- 🗂️ usa arquivos `.tf`;
- 🔁 trabalha com state;
- 🧱 tem módulos reutilizáveis;
- 📚 tem documentação forte;
- 💼 é muito usado no mercado.

---

## 🔌 11. Provider no Terraform

Provider é o plugin que conecta o Terraform a uma plataforma.

Exemplo:

```text
Terraform + AWS Provider = cria recursos na AWS
Terraform + Azure Provider = cria recursos na Azure
Terraform + Kubernetes Provider = cria recursos no Kubernetes
```

Providers comuns:

- AWS;
- Azure;
- GCP;
- Kubernetes;
- Helm;
- DigitalOcean;
- Oracle Cloud.

---

## 📚 12. Terraform Registry

O **Terraform Registry** é o catálogo de providers e módulos.

Pense assim:

```text
Docker Hub → imagens de container
Terraform Registry → providers e módulos de infra
```

Você usa o Registry para encontrar:

- providers;
- documentação;
- exemplos;
- módulos prontos.

---

## 🧾 13. HCL e arquivos `.tf`

Terraform usa **HCL**, que significa:

```text
HashiCorp Configuration Language
```

Os arquivos terminam com:

```text
.tf
```

Exemplo simples:

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "bucket" {
  bucket = "meu-bucket-iac"
}
```

---

## 🧠 14. Estrutura mental do Terraform

Guarde isso:

```text
Provider  = com quem o Terraform conversa
Resource  = o que o Terraform cria
State     = o que o Terraform sabe que existe
Module    = bloco reutilizável
Workspace = separação de ambiente/estado
Registry  = catálogo de providers e módulos
```

---

## 💻 15. Comandos básicos

```bash
terraform version
```

Mostra a versão instalada.

```bash
terraform init
```

Inicializa o projeto e baixa providers.

```bash
terraform plan
```

Mostra o que será criado, alterado ou removido.

```bash
terraform apply
```

Aplica as mudanças na cloud.

```bash
terraform destroy
```

Remove recursos gerenciados pelo Terraform.

---

## 🧠 16. O que é State?

O **state** é o arquivo que mostra o que o Terraform conhece da infraestrutura.

Ele guarda informações como:

- quais recursos existem;
- quais atributos eles têm;
- o que foi criado;
- o que precisa mudar;
- o que precisa ser removido.

Sem state, o Terraform fica “cego”.

Exemplo:

```text
Código diz: quero uma EC2 t3.micro.
State diz: existe uma EC2 t2.micro.
Terraform entende: preciso alterar.
```

---

## ⚠️ 17. Cuidados importantes

Nunca faça isso:

- ❌ commitar Access Key;
- ❌ commitar Secret Key;
- ❌ alterar recurso gerenciado direto no console;
- ❌ rodar `destroy` sem revisar;
- ❌ ignorar o `terraform plan`.

Boas práticas:

- ✅ usar Git;
- ✅ revisar Pull Request;
- ✅ usar `.gitignore`;
- ✅ separar ambientes;
- ✅ revisar permissões IAM;
- ✅ usar tags;
- ✅ olhar custos na cloud.

---

## 🗺️ 18. Mapa mental rápido

```text
IaC 🚀
├── Infra como código
├── Evita clique manual
├── Usa Git como fonte da verdade
├── Trabalha com estado desejado
├── Aproxima Dev + Infra + SRE
├── Ferramentas
│   ├── CloudFormation
│   ├── Pulumi
│   └── Terraform
└── Terraform
    ├── HCL
    ├── Provider
    ├── Resource
    ├── State
    ├── Module
    └── Workspace
```

---

## ✅ 19. Checklist de revisão

- [ ] Sei explicar o que é IaC.
- [ ] Entendi por que criar tudo no console não escala.
- [ ] Sei o que é GitOps.
- [ ] Sei a diferença entre declarativo e imperativo.
- [ ] Sei o que é CloudFormation.
- [ ] Entendi o lock-in da AWS.
- [ ] Sei o que é Pulumi.
- [ ] Sei por que o módulo escolheu Terraform.
- [ ] Sei o que é provider.
- [ ] Sei o que é Terraform Registry.
- [ ] Sei o que é HCL.
- [ ] Sei para que serve o state.
- [ ] Conheço `init`, `plan`, `apply` e `destroy`.

---

## 🧪 20. Perguntas de revisão

### O que é IaC?

É criar e gerenciar infraestrutura usando código.

### Por que IaC é melhor que console manual?

Porque dá histórico, rastreabilidade, automação e padronização.

### O que é GitOps?

É usar o Git como fonte da verdade para infraestrutura e operações.

### Declarativo ou imperativo?

Terraform usa o modelo **declarativo**.

### Por que Terraform?

Porque é popular, multi-cloud, declarativo e muito usado no mercado.

---

## 🧾 Resumo final em 4 linhas

IaC transforma infraestrutura em código versionado.
GitOps usa Git como fonte da verdade para mudanças de infra.
Terraform é a ferramenta principal do módulo por ser popular e multi-cloud.
O segredo do Terraform é entender `provider`, `resource`, `state`, `module` e `workspace`.

---

## 🧠 Frase para memorizar

```text
IaC é parar de clicar na cloud e começar a declarar a infraestrutura em código.
```
