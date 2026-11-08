# CTF 06: XSS (Cross-Site Scripting)

Projeto criado a partir do [template-seguranca](https://github.com/renanscarmo/template-seguranca)
para praticar segurança em Python.

## Objetivo

Executar um script no navegador por meio de um campo que repete o texto digitado, ler um cookie sem proteção e depois corrigir a falha.

## Como foi

1. **Antes:** a página `/ola` colocava o nome digitado direto no HTML. Com `<script>alert(document.cookie)</script>` no campo, o navegador executava o código e mostrava o cookie da sessão, que não tinha a marca HttpOnly.
2. **Detecção:** o Bandit e o pip-audit ficaram verdes, porque essa falha não aparece na leitura do código. Quem achou foi o **OWASP ZAP** (DAST), que liga o app no pipeline e o ataca sozinho: ele encontrou o XSS refletido (alerta 40012). Na primeira execução o pipeline passou mesmo assim, porque o achado veio só como aviso. Depois, um passo extra passou a ler o relatório do ZAP e a reprovar o pipeline quando há XSS refletido ou cookie sem HttpOnly.
3. **Depois:** o texto digitado passou por `escape`, e o cookie ganhou `HttpOnly` e `SameSite=Strict`. O pipeline voltou a ficar verde.

## O que aprendi

- XSS acontece quando o texto do usuário vai para a página sem filtro, e o navegador não distingue isso do código do site
- Escapar a saída transforma `<` e `>` em texto comum, que o navegador não executa
- O cookie com HttpOnly não pode ser lido por JavaScript, o que limita o estrago mesmo se houver XSS
- SAST (Bandit) e SCA (pip-audit) não pegam esse tipo de falha, e o DAST (ZAP) pega, porque testa o site rodando
- Ferramentas de DAST também geram falsos positivos, como o "XSS DOM Based" em uma página sem JavaScript, então é preciso avaliar cada achado
- Um scanner só protege se o pipeline estiver configurado para falhar quando ele acha algo importante

## Ferramentas

- SAST com Bandit
- SCA com pip-audit
- DAST com OWASP ZAP
- GitHub Actions
