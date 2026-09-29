# Kings AI Platform — instruções pra IA

- **O que é e como instalar:** [README.md](README.md).
- **Decisões e fases:** `docs/`, local e fora do git — o repo é feito pra poder ser público. Se a pasta existir, `docs/Roadmap.md` é o ponto de partida.

## Regras do repo

- Conteúdo dos plugins (skills, agentes, `claude-md/`) e README em **inglês**; docs de decisão em `docs/` em português.
- **Nada que cite empresa, cliente ou pessoa** — isso vai pra marketplace privado (ex.: `Kings-AI-Novibet`) ou pro arquivo pessoal privado.
- Skill: a `description` é o gatilho — dizer **quando** usar, com as frases que o usuário falaria.
- Agente: `tools` mínimo pro trabalho dele.
- Validar antes de commitar: `claude plugin validate .` e `claude plugin validate plugins/<nome>`.
- Testar instalação sempre num `HOME` temporário, nunca no `~/.claude` real.

## Git

- Trunk-based: branch curta a partir do `main`, PR, o Gui mergeia no GitHub.
- A IA faz os commits; o Gui revisa.
- Mensagem de commit curta e direta, em inglês.
