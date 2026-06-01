# 🚀 Resumo do Módulo: Trabalhando com CI/CD 🔄

Este documento consolida os fundamentos de Continuous Integration (CI) e Continuous Delivery/Deployment (CD), abordando desde o contexto histórico até a introdução do GitHub Actions como ferramenta principal de automação.

## 📜 1. Contexto Histórico e a "Parede da Confusão" 🧱

Antes da adoção da cultura DevOps e das práticas de CI/CD, o processo de entrega de software era fragmentado e propenso a falhas, caracterizado por uma separação rígida entre as equipes.

* 💻 **Desenvolvimento:** Focado em criar novas funcionalidades (features).
* ⚙️ **Infraestrutura/Operações:** Focado em manter a estabilidade do sistema e realizar o deploy manual.
* 💥 **O Problema:** A transição do código entre essas equipes criava a "parede da confusão". A falta de contexto mútuo gerava o clássico problema *"na minha máquina funciona"*, resultando em correções demoradas, deploys manuais arriscados e ciclos de feedback extremamente longos.

### 📊 Comparativo: Cenário Tradicional vs. Cultura DevOps (CI/CD)

| Característica | 🦖 Cenário Tradicional (Pré-DevOps) | 🚀 Com CI/CD |
| :--- | :--- | :--- |
| **Processo de Deploy** | 🐢 Manual e demorado | ⚡ Automatizado e contínuo |
| **Ciclo de Feedback** | ⏳ Longo (erros descobertos tardiamente) | ⏱️ Curto (identificação rápida de falhas) |
| **Visibilidade** | 🙈 Baixa (times isolados) | 👁️ Alta (todos acompanham o status) |
| **Rollback (Reversão)** | 😓 Complexo e estressante | ⏪ Facilitado e automatizado |
| **Responsabilidade** | 🤼 Dividida e conflituosa | 🤝 Compartilhada e colaborativa |

---

## 🧩 2. Continuous Integration (CI) - Integração Contínua 🏗️

A Integração Contínua é a prática de mesclar frequentemente o código alterado no repositório central. O objetivo é garantir que as pequenas entregas sejam integradas e validadas de forma automatizada.

* ✅ **Validação Automatizada:** A CI é responsável por preparar o ambiente, instalar dependências, construir (build) a aplicação e executar testes (unitários e de integração).
* ⚡ **Feedback Rápido:** Permite que os desenvolvedores saibam quase imediatamente se o código novo quebrou alguma funcionalidade existente.

---

## 📦 3. Continuous Delivery/Deployment (CD) - Entrega Contínua 🚢

A Entrega Contínua é a continuação natural da CI. Uma vez que o código foi integrado e testado com sucesso, a CD automatiza a implantação desse software em ambientes de homologação (staging) e/ou produção.

* 🪞 **Paridade de Ambientes:** Seguindo a metodologia do *12-Factor App*, os ambientes de homologação e produção devem ser os mais similares possíveis (ex: se usa Kubernetes em produção, deve usar em homologação).
* 🎯 **Estratégias de Deploy:**
    * 🐤 **Canary Deployment:** Liberação gradual da nova versão para uma pequena porcentagem de usuários (ex: 10% do tráfego) antes da liberação total.
    * 💨 **Smoke Tests:** Testes rápidos executados logo após o deploy para garantir que a aplicação subiu corretamente. Se falharem, um rollback automatizado pode ser acionado.
* 🚦 **Aprovações:** O fluxo de implantação é automatizado, mas pode conter etapas de aprovação manual (gatilhos) por motivos de segurança ou regra de negócio.

---

## ☁️ 4. Pipeline de Infraestrutura (IaC) 🚜

Os conceitos de CI/CD não se aplicam apenas ao código da aplicação, mas também à infraestrutura, utilizando ferramentas como o Terraform.

* 🗺️ **CI na Infraestrutura:** Representado pelo `terraform plan`. É a etapa de validação, onde verifica-se o que será alterado ou criado.
* 🏗️ **CD na Infraestrutura:** Representado pelo `terraform apply`. É a entrega de fato, onde os recursos são provisionados no provedor de nuvem de forma automatizada.

---

## 🐙 5. Ferramenta de Escolha: GitHub Actions 🛠️

O GitHub Actions será a ferramenta utilizada para orquestrar as pipelines durante o módulo. Por ser nativa do GitHub, ela elimina a necessidade de integrar serviços externos via webhooks.

### ⚙️ Componentes Principais

* 📝 **Workflow:** O arquivo declarativo (escrito em formato `.yml` ou `.yaml`) que descreve todo o processo de automação. É o orquestrador geral.
* 🎬 **Actions:** As tarefas individuais dentro de um workflow (ex: clonar o repositório, instalar Node.js, rodar testes). O GitHub oferece um vasto ecossistema de actions open-source prontas para uso.
* 🏃‍♂️ **Runner:** A máquina (servidor) responsável por executar o workflow. Pode ser configurada com diferentes sistemas operacionais (ex: Ubuntu).

### ⭐ Vantagens do GitHub Actions

* 🔗 **Integração Nativa:** Fica na aba "Actions" diretamente no repositório do GitHub.
* 💰 **C
