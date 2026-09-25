# CyberSec

SyberSec

Este README serve para explicar rapidamente onde cada parte do projeto deve ser desenvolvida.

Antes de começar a programar, veja qual área é responsabilidade da sua função e trabalhe dentro da pasta correspondente.

Estrutura

"tools/"

Aqui ficam as ferramentas do SyberSec.

Se você estiver desenvolvendo uma ferramenta de análise, automação ou cybersecurity, provavelmente ela ficará aqui.

Categorias:

- "file_analysis/" — análise de arquivos
- "metadata/" — extração de metadados
- "hashes/" — geração de hashes
- "strings/" — extração de strings, URLs, IPs, e-mails etc.
- "archives/" — análise de arquivos compactados
- "executable_analysis/" — informações de executáveis
- "web_analysis/" — análise de informações públicas de sites e domínios
- "code_analysis/" — análise de código
- "network_analysis/" — ferramentas relacionadas a redes
- "vulnerability_analysis/" — análise de vulnerabilidades em ambientes autorizados
- "automation/" — automações
- "reports/" — geração de relatórios

Se sua tarefa é criar uma ferramenta, comece procurando aqui.

"backend/"

Aqui fica a parte que faz o sistema funcionar por trás da interface.

Responsabilidades:

- API
- rotas
- comunicação entre ferramentas
- regras da aplicação
- serviços
- autenticação
- conexão com o banco
- integração entre módulos

Se você está trabalhando na lógica interna da plataforma, provavelmente deve mexer aqui.

"frontend/"

Aqui fica tudo que o usuário vê e utiliza na plataforma.

Responsabilidades:

- páginas
- menus
- botões
- formulários
- componentes
- estilos
- resultados das ferramentas
- comunicação com o backend

HTML, CSS, JavaScript e TypeScript serão utilizados principalmente nessa parte.

"database/"

Aqui fica a estrutura do banco de dados.

Responsabilidades:

- tabelas
- schemas
- migrations
- queries
- dados iniciais
- relacionamento entre dados

Não coloque senhas, tokens ou outras credenciais reais no repositório.

"tests/"

Aqui ficam os testes do projeto.

Responsabilidades:

- testes unitários
- testes de integração
- testes da API
- testes das ferramentas
- testes de segurança

Sempre que possível, uma nova função deve possuir testes.

"docs/"

Aqui fica a documentação para os desenvolvedores.

Pode conter:

- explicação da arquitetura
- funcionamento das ferramentas
- documentação da API
- guias de desenvolvimento
- decisões técnicas

Se você criar algo complexo que outro desenvolvedor precise entender, documente aqui.

"scripts/"

Aqui ficam scripts auxiliares do projeto.

Exemplos:

- configuração do ambiente
- instalação
- desenvolvimento
- testes
- deploy

".github/"

Aqui ficam as configurações relacionadas ao GitHub.

Pode conter:

- workflows
- templates de Issues
- templates de Pull Request
- automações do projeto

Como trabalhar

Não faça alterações diretamente na branch principal.

Fluxo padrão:

Escolher uma tarefa
       ↓
Criar uma branch
       ↓
Desenvolver
       ↓
Testar
       ↓
Commit
       ↓
Push
       ↓
Pull Request
       ↓
Revisão
       ↓
Merge

Exemplo de branch:

feature/file-analysis

ou:

feature/sha256

Importante

Antes de criar uma nova ferramenta ou modificar uma parte importante:

1. Verifique se alguém já está trabalhando nela.
2. Veja as Issues relacionadas.
3. Mantenha o código dentro da pasta correta.
4. Teste suas alterações.
5. Não envie senhas, tokens ou chaves privadas.
6. Explique na Pull Request o que foi alterado.

A ideia é manter o projeto organizado desde o começo para que todos consigam trabalhar nele sem atrapalhar o trabalho dos outros.

## Observação

A estrutura e a organização deste README foram elaboradas com auxílio de inteligência artificial e revisadas antes de serem adicionadas ao projeto.
