# Relatório de Auditoria de Segurança

**Disciplina:** Programação Web I — IFSE Campus Lagarto  
**Professor:** Jean Louis  
**Projeto:** Portfólio Acadêmico (Trabalho 2)

## Integrantes

- Marcos Henrique Garcia Pereira
- Márcio Pierre Santos Monteiro

## Verificação por requisito

| RS | Verificação / Correção |
|----|------------------------|
| **RS01** | Corrigido: `SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS` passam a ser lidos de variáveis de ambiente; `SESSION_COOKIE_HTTPONLY=True` e `X_FRAME_OPTIONS='DENY'`; opções SSL (`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`) documentadas e comentadas para uso em produção com HTTPS. |
| **RS02** | Corrigido: em `editar_projeto_view` e `excluir_projeto_view`, a busca passou de `get_object_or_404(Projeto, pk=pk)` + checagem manual para `get_object_or_404(Projeto, pk=pk, autor=request.user)`, retornando **404** quando o registro não pertence ao usuário (proteção contra IDOR). |
| **RS03** | Corrigido: `MinimumLengthValidator` com `min_length=10`; mantidos os demais validadores nativos (similaridade, senha comum, só numérica). |
| **RS04** | Já estava correto: todos os formulários POST usam `{% csrf_token %}` (login, registro, perfil, projeto, exclusão, logout); nenhuma view usa `@csrf_exempt`. |
| **RS05** | Já estava correto: nenhum template usa `|safe` e não há `mark_safe()` sobre dados do usuário; o escape padrão do Django permanece ativo. |
| **RS06** | Implementado: logger `portfolio.security` grava em console e em `logs/seguranca.log` a exclusão de projetos (usuário, título e pk). |

## Risco remanescente

A listagem de projetos (`lista_projetos_view`) exibe projetos de **todos** os usuários autenticados. A edição/exclusão já está protegida por IDOR, mas a exposição da listagem global ainda permite que um usuário veja títulos e dados básicos de projetos alheios. Não foi alterado neste trabalho por estar fora do escopo mínimo (RS02 trata edição/exclusão) e para não mudar o comportamento funcional do Trabalho 1.
