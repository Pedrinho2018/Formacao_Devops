# Módulo 02 · CALMS e as Três Maneiras

O **CALMS** é um framework para diagnosticar e evoluir a adoção da cultura DevOps dentro de uma organização. As **Três Maneiras** complementam o framework, guiando a implementação prática.

> CALMS responde: *"Como estamos hoje?"*
> As Três Maneiras respondem: *"Como chegamos lá?"*

---

## Índice

- [CALMS](#calms)
  - [C — Culture](#c--culture)
  - [A — Automation](#a--automation)
  - [L — Lean](#l--lean)
  - [M — Measurement](#m--measurement)
  - [S — Sharing](#s--sharing)
- [As Três Maneiras](#as-três-maneiras)

---

## CALMS

| Letra | Significado | Foco |
|---|---|---|
| C | Culture | Colaboração e mentalidade entre times |
| A | Automation | Eliminar processos manuais e repetitivos |
| L | Lean | Entregar valor com o mínimo de desperdício |
| M | Measurement | Métricas técnicas e de negócio |
| S | Sharing | Descentralização do conhecimento |

---

### C — Culture

Abordado em detalhes no [Módulo 01](./modulo-01-cultura-devops.md). A cultura é a base de tudo — sem ela, ferramentas e processos não sustentam uma transformação real.

---

### A — Automation

**Tudo que pode ser automatizado, deve ser automatizado.**

Observe os processos do time e identifique candidatos à automação. Os sinais mais comuns:

- Processos repetitivos que consomem tempo do time
- Tarefas que não escalam conforme a empresa cresce
- Ações manuais propensas a erro humano

**Entrega Contínua (CI/CD)**

Todo o fluxo de publicação deve ser automatizado:

```
Código → Dependências → Testes → Build → Deploy
```

Se os testes são manuais e exaustivos antes de cada deploy, isso é um gargalo direto — e indica distanciamento da cultura DevOps.

**IaC e GitOps — Fonte Única de Verdade**

Criar recursos manualmente no console da AWS, Azure ou GCP é um problema: não há rastreabilidade, surgem recursos duplicados e ninguém sabe exatamente o que existe no ambiente.

A solução é o **GitOps**:

- Toda infraestrutura fica **versionada no Git**
- O console cloud passa a ser **somente leitura**
- Qualquer mudança obrigatoriamente **passa pelo código**, com code review e histórico
- Resultado: economia, rastreabilidade e manutenibilidade

> Módulos dedicados a CI/CD e IaC/GitOps serão abordados adiante.

---

### L — Lean

Lean orienta o time a **focar no que gera valor real** e eliminar desperdício de tempo e energia.

O pior cenário possível: **alta complexidade + baixo valor**. Semanas de trabalho em algo que o cliente não vai usar.

**Mentalidade de MVP**

Aplica-se a produtos, features e histórias:

1. Identifique o **núcleo** da ideia — o que é absolutamente essencial
2. Entregue o **mínimo viável** desse núcleo
3. Colete feedbacks reais do mercado
4. **Itere** — evolua ou descontinue com base nos dados

Mesmo com pesquisa prévia, qualquer ideia tem incerteza. Só o mercado real confirma a aderência.

**Errar rápido, corrigir rápido**

Entregas pequenas e frequentes permitem identificar e resolver problemas cedo. Quanto maior e mais demorada a entrega, mais difícil e custoso é corrigir o erro quando ele aparece.

> O erro deve ser descoberto **pelo time**, não pelo cliente. Para isso, o time precisa de observabilidade, testes automatizados e capacidade de rollback.

---

### M — Measurement

Para melhorar continuamente, você precisa de **dados reais**. Métricas eliminam o achismo das decisões.

**Métricas de negócio**
- Acessos por período
- Engajamento com novas features
- Taxa de conversão e mapas de calor

**Métricas técnicas**
- Latência de endpoints críticos
- Taxa de erros em produção
- Disponibilidade e uptime dos serviços

> Erros críticos devem ser detectados **internamente**, antes que qualquer cliente os reporte.

Sem mensuração, a melhoria contínua é impossível — não há como otimizar o que não é medido.

---

### S — Sharing

Diretamente ligado ao antipadrão da **Síndrome da Pessoa Herói** ([Módulo 01](./modulo-01-cultura-devops.md)).

O que deve ser compartilhado ativamente:

- Postmortems e aprendizados de incidentes
- Tecnologias implementadas — o que funcionou e o que não funcionou
- Documentação de fluxos, arquiteturas e decisões técnicas
- Processos de deploy e resposta a incidentes

Um time com cultura de compartilhamento é mais autônomo, mais produtivo e consegue focar no que realmente importa — ao invés de ficar dependente de uma pessoa para resolver problemas específicos.

---

## As Três Maneiras

Originadas no livro **O Projeto Phoenix**, dos mesmos autores do Manual de DevOps. Representam os três estágios de maturidade na implementação da cultura DevOps.

---

### 1ª Maneira — Acelerar o Fluxo

`Dev → Ops`

Estabelecer fluxos de trabalho mais rápidos e eficientes entre Desenvolvimento e Operações.

- Transparência total sobre o ciclo de vida da aplicação
- Eliminar tarefas de baixo valor e alta complexidade
- Evitar a criação de pessoas heróis — o conhecimento deve ser coletivo
- Deploys frequentes para ciclos de feedback mais curtos
- Otimizações baseadas em métricas, não em percepções
- Automação de tudo que for repetitivo

---

### 2ª Maneira — Amplificar o Feedback

`Dev ↔ Ops`

Estabelecer feedback contínuo em todas as direções do fluxo de trabalho.

- Comunicação constante e bidirecional entre times
- Detecção rápida de erros para recuperação ágil
- Incorporação de conhecimento a cada incidente e entrega
- Loops de feedback que permitem corrigir o curso rapidamente

---

### 3ª Maneira — Experimentação e Aprendizado Contínuos

O estágio mais maduro. A cultura de aprendizado organizacional está consolidada.

- Experimentos constantes — técnicos e de negócio — fazem parte do dia a dia
- Problemas locais são transformados em melhorias globais
- O time evolui coletivamente, sem centralização de conhecimento
- Aprendizado contínuo é um valor cultural, não um evento pontual

> Uma organização na 3ª Maneira está genuinamente operando dentro da cultura DevOps.

---

> **Módulo anterior ←** [Módulo 01 · Cultura DevOps](./modulo-01-cultura-devops.md)
> **Voltar ao início →** [README](./README.md)
