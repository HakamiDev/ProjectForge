<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · **Português** · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**Um sistema operacional para uma equipe de agentes de IA.** Um único comando transforma uma pasta comum em um escritório disciplinado: um quadro único do qual todos os agentes trabalham, em qualquer plataforma; um portão de qualidade independente; governança de decisões; uma trilha de auditoria completa; métricas de desempenho que podem ser exportadas para o Power BI; e um site de gestão que funciona a partir de um único arquivo HTML.

Python 3.9 ou superior, sem dependências, sem servidor. Código aberto, licenciado sob MIT.

Site: https://hakamidev.github.io/ProjectForge/

## Instalação

Uma única linha, colada em um terminal. Ela baixa a ferramenta, executa, faz quatro perguntas e depois abre o seu site de gestão.

macOS e Linux (Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

O site também permite escolher antes a plataforma e o idioma preferido; ambos são incorporados ao comando de instalação e pré-selecionados no assistente.

## O que ele resolve

- **Os chats esquecem.** As regras e as descrições dos papéis ficam na pasta, não na memória do chat, de modo que qualquer chat pode retomar o trabalho.
- **Os agentes colidem.** Um quadro numerado; "em andamento" bloqueia uma linha; uma verificação por checksum impede gravações conflitantes.
- **Entregas sem verificação.** Um chefe de garantia da qualidade decide se o trabalho é aprovado ou reprovado antes de chegar ao dono.
- **Decisões paradas.** No máximo cinco decisões abertas e uma regra de 48 horas, após a qual a recomendação prevalece.
- **Nada é medido.** `report` fornece taxa de entrega, tempo de ciclo, taxa de aprovação no QA e carga por papel; `export` grava arquivos CSV para o Power BI.
- **Sem responsabilização.** Toda gravação no quadro é registrada: quem, quando e o quê.
- **Dados sensíveis em ferramentas externas.** Uma política de dados vinculante, com classificação e ferramentas aprovadas.

## O que você recebe

- **80 especializações** (estratégia, restaurantes, imóveis, software, RH, educação e mais) com mais de 330 papéis prontos que você adiciona com um clique.
- **130 habilidades prontas em 18 grupos.** Uma habilidade é um arquivo curto que descreve quando usá-la, as etapas, o resultado e o critério de aceitação, para que o colaborador a aplique em vez de improvisar.
- **Quatro plataformas:** Claude, ChatGPT, Grok e Gemini. Cada colaborador pode trabalhar em uma plataforma diferente.
- **27 idiomas de interface** no site e no assistente. O idioma preferido é o idioma de gestão de todo o sistema e o usado com os colaboradores.
- **Um site de gestão** a partir de um único arquivo HTML: quadro, equipe, decisões, métricas, uma biblioteca de comandos prontos e um mecanismo de atenção que sinaliza o que está atrasado ou aguardando você.

## Comandos

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Plataformas

| Plataforma | Como a equipe é configurada |
| --- | --- |
| Claude | Crie um projeto com o nome do seu projeto e adicione a pasta gerada. |
| ChatGPT | Crie um projeto e envie os arquivos da pasta. |
| Grok | Crie um projeto, cole o comando Compass nas instruções dele e adicione os arquivos. |
| Gemini | Crie um Gem para cada colaborador, cole o comando dele nas instruções e adicione os arquivos em Knowledge. |

Envie os arquivos da pasta do projeto a partir do local original e reenvie o que mudar. Até onde sabemos, Grok e Gemini não gravam diretamente na pasta, portanto mova você mesmo as saídas deles para dentro dela. As etapas seguem a documentação pública no momento da redação; as interfaces e os limites são definidos por essas plataformas e podem mudar.

## Limites atuais

- O assistente e o site aparecem em 27 idiomas, mas os arquivos gerados do projeto (regras, descrições dos papéis, quadro) e o site de gestão são escritos em árabe por enquanto. Os colaboradores são informados do idioma em que devem trabalhar e respondem a você nele.
- Os nomes de arquivos, os comandos e os termos de status do quadro permanecem em árabe porque a ferramenta os lê literalmente.
- A instalação no Windows ainda não foi testada em uma máquina real.

## Para desenvolvedores

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

O código-fonte está em `forge/`; `tools/build-single.py` produz a ferramenta de arquivo único em `dist/`. Os modelos estão em `forge/templates/` e o site público em `site/`.

## Licença

MIT.
