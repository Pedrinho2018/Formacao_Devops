# 🚀 Módulo 04: Trabalhando com CI/CD - Criando Nosso Primeiro Pipeline

Neste módulo, saímos da teoria e colocamos a mão na massa para construir nosso primeiro pipeline de Integração Contínua (CI). O objetivo é automatizar a validação de uma aplicação Node.js (NestJS) utilizando o **GitHub Actions**, uma poderosa ferramenta nativa do próprio GitHub.

---

## 📦 1. Preparação do Ambiente e Repositório

O primeiro passo para utilizar o GitHub Actions é ter o seu código versionado na nuvem.
* Criamos um repositório no GitHub (no exemplo, nomeado de forma padronizada como `rocketcity.ci.api`).
* Fizemos o *push* da aplicação base (que já conta com um `Dockerfile` configurado em módulos anteriores) para a branch `main`.
* A grande vantagem do GitHub Actions é que, ao criar o repositório, a aba **"Actions"** já fica disponível instantaneamente, sem necessidade de integrar sistemas de terceiros via webhooks manuais.

---

## ⚙️ 2. A Estrutura do GitHub Actions (YAML)

O GitHub Actions orquestra suas automações através de arquivos declarativos na linguagem **YAML** (`.yml`). Estes arquivos devem, obrigatoriamente, ficar armazenados dentro da pasta `.github/workflows/` na raiz do seu projeto.

### Conceitos Chave do Declarativo

| Componente | Descrição Prática |
| :--- | :--- |
| **Workflow** | O arquivo inteiro (`ci.yml`). É o processo automatizado de ponta a ponta. |
| **Events (`on`)** | O "Gatilho" (Trigger). Define *quando* o workflow deve ser executado. |
| **Jobs** | Um agrupamento de passos (Steps). Por padrão, jobs rodam em paralelo. |
| **Runner (`runs-on`)** | A máquina virtual (servidor) que executará os comandos (ex: `ubuntu-latest`). |
| **Steps** | As etapas individuais e sequenciais dentro de um job (ex: clonar o código, rodar comandos). |

---

## 🛠️ 3. Construindo o Pipeline Passo a Passo

Construímos o arquivo de configuração para realizar as etapas fundamentais de uma Integração Contínua: preparar a máquina, instalar dependências e testar a aplicação.

### Passo A: O Gatilho (`on`)
O gatilho é obrigatório. Sem ele, o GitHub não sabe quando disparar a automação. 
* Configuramos para que o pipeline escute eventos de `push` especificamente na branch `main`.

### Passo B: Checkout do Código (`actions/checkout`)
A máquina virtual do GitHub (`ubuntu-latest`) nasce vazia. Para que ela possa testar nosso projeto, precisamos fazer o download dos arquivos para dentro dela.
* Utilizamos a action oficial `actions/checkout@v4` para sincronizar o repositório dentro do runner.

### Passo C: Configuração do Node.js (`actions/setup-node`)
Como nossa aplicação roda em Node.js, precisamos instalar essa dependência no runner.
* Utilizamos a action `actions/setup-node@v4`.
* Especificamos a utilização do gerenciador de pacotes `yarn`.

### Passo D: Execução dos Comandos
Com a máquina pronta e o código baixado, passamos comandos diretos no terminal do runner utilizando a tag `run`:
* Executamos `yarn` para instalar as dependências da aplicação (`node_modules`).
* Executamos `yarn test` para rodar os testes unitários padrão do NestJS e garantir que a aplicação não está quebrada.

---

## 🧠 4. O Poder da Estratégia de Matriz (Matrix Strategy)

Para garantir uma confiabilidade extrema do código, adicionamos um recurso avançado do GitHub Actions: a **Matrix Strategy** (`strategy.matrix`).

Em vez de testar a aplicação em apenas uma versão do Node.js, configuramos uma matriz contendo um array de versões: **16, 18 e 20**.
* **Como funciona:** O GitHub Actions lê essa matriz e multiplica os jobs automaticamente.
* **O Resultado:** Em vez de um único job, ele roda *três jobs em paralelo*, cada um com uma versão diferente do Node.js. 
* **O Benefício:** Garantimos instantaneamente que nosso software é compatível e estável em diferentes ecossistemas, identificando quebras de versão de forma preventiva.

---

## 📄 Estrutura Final do Arquivo `ci.yml`

Abaixo está o reflexo final do código YAML que construímos, consolidando todos os conceitos aprendidos:

```yaml
name: CI

on:
  push:
    branches:
      - main

jobs:
  build-and-test:
    name: Build and Test Node - ${{ matrix.node }}
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node: [16, 18, 20]

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'yarn'

      - name: Install Dependencies
        run: yarn

      - name: Run Tests
        run: yarn test