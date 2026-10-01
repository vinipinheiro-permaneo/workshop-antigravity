---
name: configurar-pessoal
description: "Pergunta se a pessoa quer registrar atividades pessoais que podem interferir no profissional (horário indisponível, compromisso da semana) e documenta em DOMINIOS/PESSOAL/, só na máquina dela. Use na primeira conversa deste repositório, ou quando alguém pedir para configurar isso."
---

# Configurar pessoal

**Objetivo:** saber só o que pode interferir no trabalho — nada de perfil completo, nada de dado sensível.

## Passos

1. Pergunte, uma vez por sessão: *"Quer configurar o seu `DOMINIOS/PESSOAL/`? Serve só para eu saber de atividades pessoais suas que podem interferir no profissional — por exemplo, um horário em que você não deve ser interrompido, ou um compromisso que reduz sua disponibilidade essa semana. Não é um perfil completo, e o arquivo nunca sai da sua máquina (está no `.gitignore`)."*
2. Se a resposta for não: não crie nenhum arquivo e não pergunte de novo nesta sessão.
3. Se a resposta for sim, pergunte uma de cada vez, só avançando depois da resposta:
   - "Tem algum horário ou dia em que você não deve ser interrompido com tarefas?"
   - "Tem algum compromisso pessoal nas próximas semanas que vai reduzir sua disponibilidade?"
   - "Tem algo pontual que eu deva saber agora para não sobrecarregar você?"
4. Escreva só o que a pessoa disse (não invente nada) em `DOMINIOS/PESSOAL/atividades.yaml`:
   ```yaml
   atualizado: "<data de hoje>"
   indisponibilidade: "<resposta 1, ou vazio se não houver>"
   compromissos: "<resposta 2, ou vazio se não houver>"
   observacao: "<resposta 3, ou vazio se não houver>"
   ```
5. Confirme à pessoa o que foi escrito e lembre que ela pode editar o arquivo a qualquer momento ou apagá-lo.

## Verificação

- [ ] O arquivo só tem os quatro campos acima — nenhum dado de terceiro, nenhum CPF, e-mail ou informação de cliente.
- [ ] Nada foi inventado: cada campo veio de uma resposta direta da pessoa, ou ficou vazio.
- [ ] `DOMINIOS/PESSOAL/` está listado no `.gitignore` da raiz do repositório.
