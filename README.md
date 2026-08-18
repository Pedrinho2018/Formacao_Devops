<div align="center">

# ⚙️ Formação DevOps — Labs & Notes

**Trilha prática de DevOps, Infrastructure as Code, CI/CD, containers, automação e observabilidade.**

![Status](https://img.shields.io/badge/status-em%20evolução-2ea44f?style=flat-square)
![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA?style=flat-square&logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-containers-2496ED?style=flat-square&logo=docker&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-pipelines-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Docs](https://img.shields.io/badge/docs-práticas-0A66C2?style=flat-square)

</div>

---

## 🎯 Objetivo

Este repositório documenta minha evolução em **DevOps aplicado à infraestrutura**, organizando teoria, exemplos e laboratórios em uma trilha progressiva.

A proposta não é apenas guardar anotações. Cada etapa deve evoluir para **documentação reutilizável + laboratório prático + evidência técnica**.

```text
Cultura DevOps
      ↓
Infrastructure as Code
      ↓
Terraform
      ↓
CI/CD
      ↓
Containers
      ↓
Automação de pipelines
      ↓
Observabilidade
      ↓
DevSecOps
```

---

## 🧭 Trilha atual

| # | Tema | Material | Status |
|---:|---|---|---|
| 01 | Cultura DevOps | [Abrir](docs/01-cultura-devops.md) | ✅ Documentado |
| 02 | CALMS e as Três Maneiras | [Abrir](docs/02-calms-tres-maneiras.md) | ✅ Documentado |
| 03 | Infrastructure as Code | [Abrir](docs/03-infrastructure-as-code.md) | ✅ Documentado |
| 04 | Terraform — fundamentos | [Abrir](docs/04-terraform-fundamentos.md) | ✅ Documentado |
| 05 | Terraform State | [Abrir](docs/05-terraform-state.md) | ✅ Documentado |
| 06 | Data Sources, Outputs e Modules | [Abrir](docs/06-terraform-data-sources-outputs-modules.md) | ✅ Documentado |
| 07 | CI/CD — fundamentos | [Abrir](docs/07-ci-cd.md) | ✅ Documentado |
| 08 | Primeiro Pipeline | [Abrir](docs/08-primeiro-pipeline.md) | ✅ Documentado |

➡️ [Índice completo da documentação](docs/README.md)

---

## 🧪 Laboratórios disponíveis

| Lab | Foco | Evidência prática |
|---|---|---|
| [`01-terraform-basics`](labs/01-terraform-basics/) | Terraform local | `init`, `fmt`, `validate`, `plan`, `apply`, outputs e destroy |
| [`02-docker-app`](labs/02-docker-app/) | Containers | Dockerfile, build, healthcheck, usuário não-root e Compose básico |

➡️ [Ver roadmap completo dos labs](labs/README.md)

> Nenhum laboratório deve conter credenciais, tokens, chaves privadas ou dados reais de ambientes corporativos.

---

## 📁 Estrutura

```text
Formacao_Devops/
├── README.md
├── ROADMAP.md
├── docs/
│   ├── README.md
│   ├── 01-cultura-devops.md
│   ├── 02-calms-tres-maneiras.md
│   ├── 03-infrastructure-as-code.md
│   ├── 04-terraform-fundamentos.md
│   ├── 05-terraform-state.md
│   ├── 06-terraform-data-sources-outputs-modules.md
│   ├── 07-ci-cd.md
│   └── 08-primeiro-pipeline.md
└── labs/
    ├── README.md
    ├── 01-terraform-basics/
    └── 02-docker-app/
```

---

## 🧠 Como uso este repositório

1. Estudo o conceito.
2. Resumo com linguagem objetiva.
3. Registro comandos, decisões e pontos de atenção.
4. Transformo o conteúdo em laboratório.
5. Versiono a evolução no Git.
6. Reviso o material como referência para trabalho, entrevistas e certificações.

---

## 🗺️ Próximos passos

O planejamento completo está em [`ROADMAP.md`](ROADMAP.md).

Próximos blocos técnicos:

`Docker Compose multi-serviço` → `GitHub Actions` → `CI/CD prático` → `Observabilidade` → `DevSecOps`

---

<div align="center">

**Aprender → construir → automatizar → observar → proteger.**

</div>
