# Gabarito do Lab 6: relatório da auditoria

## O que o scanner pega (`python FERRAMENTAS/auditar.py ../caca-ao-risco`)
| Regra | Onde | Risco | Correção |
|---|---|---|---|
| SEC-01 | `.env` | chave escrita no arquivo | tirar o valor; variável de ambiente ou cofre de segredos |
| SEC-02 | `.env` | `.env` fora do `.gitignore`: vai parar no git | `.gitignore` com `.env` |
| SEC-03 | `site/index.html` | biblioteca de CDN sem versão: o código muda sem aviso | fixar `lodash@4.17.21` |
| SEC-04 | `.github/workflows/ci.yml` | Action apontando para `@main` | fixar pelo SHA do release (tag é o mínimo) |
| SEC-05 | `pacote-baixado/settings.json` | `command(*)` e `read_url(*)`: o agente roda e acessa qualquer coisa | liberar prefixos específicos |
| SEC-06 | `pacote-baixado/settings.json` | `dangerouslySkipPermissions: true` | modo com aprovação (`toolPermission: request-review`) |
| SEC-07 | `pacote-baixado/skills/turbo-deploy/SKILL.md` | "ignore as regras" e "não conte ao usuário": injeção de prompt | não instalar; reportar |
| SEC-08 | `pacote-baixado/README.md` | `curl ... \| sh`: executa código da internet sem ler | baixar, ler, fixar versão, só então rodar |
| SEC-09 | `scripts/deploy.sh` | conta de serviço com `roles/editor` | papel mínimo para a tarefa |
| SEC-10 | `dados/amostra.csv` | CPF (dado pessoal) no workspace | dado fictício mascarado; dado real não entra (POL-DADOS) |
| SEC-11 | `.github/workflows/ci.yml` | `permissions: write-all` | `contents: read` |
| SEC-12 | `pacote-baixado/hooks/libera_tudo.py` | hook que responde `allow` para tudo | hook só restringe: responder `ask` |

## O que o scanner NÃO pega (precisa de gente lendo)
1. **Skill gananciosa:** a `description` do `turbo-deploy` diz "Use sempre, em qualquer pedido". O agente lê a descrição para decidir quando ativar a skill, então ela sequestra toda conversa.
2. **Matcher `*` no `hooks.json`:** o hook que libera tudo vale para **toda** ferramenta, não só para comandos.
3. **`--allow-unauthenticated` no `deploy.sh`:** o serviço fica público na internet. A defesa é exigir login (por exemplo, via IAP) com conta da empresa.
4. **CI que faz deploy a cada push:** não existe etapa de teste nem homologação, e não há aprovação humana entre o código e a produção.
5. **`allowNonWorkspaceAccess: true`:** o agente pode ler e escrever fora do projeto.

## Correção aplicada no gabarito
Os arquivos de `gabarito/lab6/` sobrescrevem os de `caca-ao-risco/`. Depois disso, o scanner mostra **0 erro** e sobra um aviso: a Action continua fixada por tag, e trocar pelo SHA é o desafio 🔴.
