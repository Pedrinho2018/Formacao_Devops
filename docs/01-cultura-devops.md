# Módulo 01 — Cultura DevOps

> *"DevOps não é uma ferramenta, não é um cargo — é uma cultura."*

---

## 📌 O que é Cultura DevOps?

DevOps é uma cultura organizacional que une **Desenvolvimento** e **Operações** com o objetivo de entregar software com mais velocidade, qualidade e confiabilidade. Mais do que adotar ferramentas, significa mudar a forma como times colaboram, aprendem e entregam valor.

---

## 🏢 Empresa SEM DevOps

Em organizações tradicionais, os times costumam operar em silos isolados:

| Time | Responsabilidades |
|---|---|
| **Desenvolvimento** | Frontend, Backend, Mobile |
| **Operações (Infra)** | Servidores, Deploy, Monitoramento |

### Problemas comuns nesse modelo

- **Descentralização do conhecimento** — cada time sabe apenas sobre o seu domínio, criando dependências e gargalos.
- **Falta de feedback** — ciclos longos entre desenvolvimento e produção dificultam a identificação de problemas.
- **Processos manuais** — ausência de automação gera retrabalho e inconsistências.
- **Dificuldade de escala** — processos manuais e silos tornam o crescimento lento e arriscado.

---

## 🚀 Empresa COM DevOps

Com a adoção da cultura DevOps, a dinâmica muda completamente:

### Pilares da Cultura DevOps

### 🤝 1. Integração entre Times
Desenvolvimento e Operações trabalham juntos desde o início. Não existe mais o famoso *"na minha máquina funciona"* — todos são co-responsáveis pela entrega e pela saúde do produto em produção.

### 📄 2. Documentação Contínua
O conhecimento é registrado e atualizado de forma contínua, não apenas no final do projeto. Runbooks, ADRs (Architecture Decision Records), wikis e READMEs são tratados como parte da entrega.

### 🔄 3. Feedback e Aprendizado Contínuos
Ciclos curtos de feedback permitem aprender rápido com erros e acertos. O aprendizado não é um evento pontual — é parte do fluxo diário de trabalho.

### ⚙️ 4. Automação
Tudo que pode ser automatizado, deve ser. Testes, builds, deploys, monitoramento e alertas são automatizados para reduzir erros humanos e liberar o time para trabalhar no que gera valor.

### 💥 5. Errar Rápido e Corrigir Rápido (*Fail Fast, Fix Fast*)
Ambientes seguros para experimentação, onde falhas em produção são detectadas rapidamente e revertidas com o menor impacto possível. A cultura DevOps não pune o erro — ela cria sistemas que minimizam seu impacto.

---

## 🛡️ SRE — Site Reliability Engineering

O **SRE (Engenheiro de Confiabilidade de Sites)** é uma das práticas que emerge da cultura DevOps, popularizada pelo Google. Enquanto o DevOps é a cultura, o SRE é uma forma de implementá-la com foco em **confiabilidade e escalabilidade de sistemas**.

Conceitos-chave do SRE:

- **SLO** (Service Level Objective) — metas de confiabilidade do serviço
- **SLI** (Service Level Indicator) — métricas que medem o comportamento real
- **Error Budget** — margem de falha aceitável que equilibra velocidade e estabilidade
- **Toil** — trabalho operacional manual e repetitivo que o SRE busca eliminar com automação

> O SRE trata a operação de sistemas como um problema de engenharia de software.

---

## 🦸 Síndrome da Pessoa Herói

Um dos **antipadrões** mais comuns em times sem cultura DevOps.

Ocorre quando **uma única pessoa concentra o conhecimento crítico** de sistemas ou processos. Ela é insubstituível — e isso é um problema, não um elogio.

### Sintomas
- Só uma pessoa sabe fazer o deploy em produção
- Se ela sair de férias, o time trava
- O conhecimento está na cabeça, não na documentação
- Há uma dependência emocional e operacional dessa pessoa

### Por que é prejudicial?
- Cria um **ponto único de falha humano**
- Sobrecarrega o indivíduo e gera burnout
- Impede o crescimento e a autonomia do time
- Contradiz diretamente os princípios de colaboração e documentação contínua do DevOps

### Como combater?
- Documentação contínua e acessível
- Rotação de responsabilidades (on-call, deploys, revisões)
- Pair programming e code/ops reviews
- Cultura de compartilhamento de conhecimento sem julgamentos

---

## 🗺️ Resumo Visual

```
ANTES (Silos)                     DEPOIS (DevOps)
─────────────────                 ──────────────────────────────
  Dev  │  Ops                      Dev + Ops + SRE
  ─────┼──────                     ──────────────
  ❌ Silos                          ✅ Colaboração
  ❌ Deploys manuais               ✅ CI/CD automatizado
  ❌ Feedback lento                ✅ Observabilidade contínua
  ❌ Conhecimento centralizado     ✅ Documentação viva
  ❌ Pessoa Herói                  ✅ Time autônomo e resiliente
```

---

*Documentação mantida por: `@seu-usuario` | Última atualização: 2026*

---

## Navegação

> **Início ←** [README](./README.md)
> **Próximo módulo →** [Módulo 02 · CALMS e as Três Maneiras](./modulo-02-calms-e-as-tres-maneiras.md)
