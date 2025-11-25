# PUC-CAMPINAS  
## PROJETO CANGURU  

---

### Disciplina: Computação em Nuvem  
### 6° semestre – 2025  

**Equipe:**  
- Arturo Bento Duran  
- Raphael Bento von Zuben  

---

# 1. Introdução

## Contexto Aplicado  
O projeto em questão é a plataforma 
**Canguru**
(disponível em: `https://asteroide-app-dqe5edbqapbta6ce.brazilsouth-01.azurewebsites.net/`), 
que se insere no contexto de 
**[uma aplicação com âmbito de segurança e acadêmica]**.  

Esta aplicação tem como público-alvo 
**[professores, alunos e pesquisadores]**
e opera em 
**[na nuvem Azure em uma disposição de contâineres, rodando em um ambiente Flask, imortando dados via API e exibindo-os via HTML]**.

---

## Problema  
Atualmente, enfrenta-se o desafio de 
**[Falta de modelos que consigam manipular dados astrofísicos de maneira simples e usual]**.  

Esse problema é importante porque 
**[A pesquisa sobre os objetos rochosos fica estritamente fechada a pesquisadores da área]**.

---

## Motivação  
A motivação para abordar esse problema surge de 
**[A falta de flexibilidade no estudo astrofísico e de criação de parâmetros]**.  

Resolver esse problema trará benefícios como:  
- **[Facilidade ao identificar e catalogar um asteroide]**  
- **[As informações chegrão ao público de maneira mais concisa]**  

---

## Objetivos  

### Objetivo Geral  
Predizer o perigo de um asteróide inputado pelo usuário.


---

## Estrutura do Relatório  
Este relatório está organizado da seguinte forma:

1. **Diagnóstico** — análise técnica e organizacional da situação-problema;  
2. **Métodos** — abordagem utilizada para investigar e comparar soluções;  
3. **Propostas de Intervenção** — recomendações detalhadas de melhoria;  
4. **Métricas de Sucesso** — critérios para medir a eficácia das soluções aplicadas;  
5. **Conclusão** — síntese dos resultados e próximos passos.


---

# 2. Conjunto de Dados

## 2.1 Fonte dos Dados
Os dados utilizados no projeto Asteroide têm origem da
**[API oficial da NASA, salvos em csv]**.

---

## 2.2 Descrição Geral dos Dados
O conjunto de dados contém informações relacionadas a:

- **[Tamanho dos asteroides]**  
- **[Velocidade dos ateróides]**  
- **[Distância entre o mesmo e o planeta]**

---

## 2.3 Esquema dos Dados
Abaixo está o esquema lógico do conjunto de dados utilizado:

```text
Tabela/Objeto: [asteroids]
--------------------------------------------------
- campo_1 (tipo): descrição
- campo_2 (tipo): descrição
- campo_3 (tipo): descrição
- campo_4 (tipo): descrição
