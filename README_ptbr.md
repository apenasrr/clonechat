
# Clonechat

Clona todas as postagens de um Canal/Grupo do telegram para um outro Canal/Grupo.

Backup seguro. Guarda e protege as postagens no chat destino de eventual derrubada de postagens no chat de origem.

Para clonagem padrão, use o executável `exec_clonechat.bat`.

Para clonar canal de conteúdo protegido, use o `exec_clonechat_protect.bat`.

Para apenas fazer download de todo o canal, use o `exec_downloadall.bat`.
## Quer clonar sem instalar nada?

Experimente a versão via colab, criada por outra pessoa:

[https://github.com/Drrivao/Clonechat-Telegram-Colab](https://github.com/Drrivao/Clonechat-Telegram-Colab)

## Quer clonar numa instância própria?

**Continue a leitura**

## Configuração
- Instale o Python
  - Acesse o site python.org e [baixe](https://www.python.org/downloads/) a versão estável mais nova
  - Instale. No form 'Advanced Options', marque `Add python 3.?? to PATH`
- Atualize as dependências
  - Execute o arquivo `update_libs.bat` para atualizar as dependências
  - Se aparecer uma mensagem falando sobre pip desatualizado, execute novamente o arquivo de update após executar o seguinte comando no terminal: `python -m pip install --upgrade pip`
  - Se você desejar usar o clonechat em maior velocidade, gere um bot token e registre na flag bot_token do arquivo de configuração em `user/config.ini`

> Não sabe obter api_id, api_hash ou bot_token? Veja o tópico ["Perguntas frequentes"](#perguntas-frequentes)

## Download

Para baixar o clonechat no seu PC:
- [acesse seu repositório](https://github.com/apenasrr/clonechat/)
- Clique no botão verde "**<> Code**"
- Finalize clicando em "Download ZIP"
- Extraia o conteúdo numa nova pasta vazia

## USO

Primeiro uma dica para sua segurança.

É recomendado encaminhar no máximo 1.000 posts por dia, não alterando as configurações de velocidade no encaminhamento. Estes limites servem para o telegram não classificar sua conta como praticante de abuso e acabar aplicando punição e levando até ao banimento da conta. Se você quer se manter seguro, clone no máximo 1.000 posts por dia e não mexa nas configurações de velocidade (delay) de clonagem.

Agora vamos as opções de uso. :)
### Opção 1: Via menu em terminal

Você precisa ter o api_id e api_hash da sua conta antes de executar o clonechat.

- Execute o arquivo `exec_clonechat.bat`
- Digite o chat_id do canal/grupo de origem. Se o `ctrl+v` não funcionar, clique com o botão direito do mouse no terminal
- Confirme com [ENTER]
- Digite o chat_id do canal/grupo de destino
- Confirme com [ENTER]
- No menu de escolha de tipos de arquivos
  - Digite uma opção de filtro de arquivos
  - Se quiser clonar todos os arquivos, digite zero
  - Você pode selecionar múltiplas opções as separando com vírgulas. Ex.: `1,3` para clonar apenas fotos e documentos.
- Informe se deseja iniciar uma nova clonagem ou continuar uma clonagem iniciada anteriormente
  - Digite `1` para nova clonada
  - ou `2` para continuar
- Confirme com [ENTER]

- Na primeira vez que você for usar, será preciso autenticar uma conexão com o telegram. Mas será só da primeira vez! E depois nunca mais. :) Autenticar é simple, segue os passos:
  > `"Enter phone number or bot token:"`
  - Aparecerá esta mensagem pedindo o número de seu telefone em formato internacional.
  - Digite seu número de telefone com prefixo `+55` para o caso de telefone brasileiro, seguido do DDD local e seu número de telefone.
    - Exemplo: Para telefone de São Paulo, com ddd 11, deverá ser digitado algo como: `+5511995429405`
  - Na mensagem perguntando se o número está correto, digite `y`.
  - Será enviado um código para seu telegram, que você deve digitar no terminal.
  - Por fim, se você tiver 'segurança de 2 fatores' (2fa) ativado na sua conta, será solicitado sua senha.
  - Ao executar o `exec_clonechat.bat`, será solicitado seu api_id e api_hash. Você só precisa os informar uma vez, pois as demais conexões serão realizadas por um arquivo de sessão que será criado na pasta do clonechat.

Aguarde a clonagem terminar!

> Importante: Clonagem via usuário (mode=user) possui uma pausa de 10 segundos entre posts. Já clonagem via bot (mode=bot) é mais rápido, possuindo uma pausa de apenas 1 segundo entre posts.

### Opção 2: via linha de comando

> Abra o terminal do windows na pasta do clone chat e digite:

Comando: python clonechat.py --orig={chat_id do canal/grupo de origem} --dest=-{chat_id do canal/grupo de destino}

Exemplo: `python clonechat.py --orig=-100222222 --dest=-10011111111`

Caso queira fazer a clonagem via bot:

Exemplo: `python clonechat.py --orig=-100222222 --dest=-10011111111 --mode=bot`

Caso queira continuar uma tarefa de clonagem ao invés de iniciar. Útil para atualizar um canal clonado ou retomar uma tarefa de clonagem interrompida anteriormente:

Exemplo: `python clonechat.py --orig=-100222222 --dest=-10011111111 --new=2`

Para verificar todos comendos de terminal:
Comando: `python clonechat.py --help`

## Perguntas frequentes

### Como conseguir o chat_id de um canal ou grupo

Existem várias formas de obter o chat_id de um canal. Mostraremos duas delas:
- Usando o telegram client [Kotatogram](https://kotatogram.github.io/download/):
  - Acesse a tela de descrição do canal
  - Copie o `chat_id` que aparece abaixo do nome do canal
- Usando bot Find_TGIDbot:
  - Acesse e inicie bot [@Find_TGIDbot](http://t.me/Find_TGIDbot) ou [@myidbot](http://t.me/myidbot)
  - Encaminhe qualquer postagem do canal para este bot
  - O bot responderá com o ID do remetente da mensagem. Neste caso, o ID do canal.
- Copie o `chat_id` (incluindo o sinal de subtração).

Atenção:
- Vale ressaltar que o Kotatogram não informa o início '-100' no chat_id. Mas todos os canais e grupos devem possuir o '-100' no início. Se for coletar o `chat_id` pelo kotatogaram, lembre de digitar manualmente o `-100` no início.
> Exemplo de um código de canal: `-1001623956859`
- Para coletar o `chat_id` de um grupo com o [@Find_TGIDbot](http://t.me/Find_TGIDbot) é mais trabalhoso, pois se você encaminhar a mensagem de um membro, o bot informará o ID do usuário e não o id do grupo. Assim, ou você deve encaminhar uma mensagem de um "ADM Anônimo" ou recomendamos usar o kotatogram para pegar o chat_id da tela de deescrição do canal.

### Como gerar credenciais de acesso a API do telegram?

- Leia o tópico "Configuração de token" do tutorial encontrado em: https://github.com/apenasrr/zimatise_docs#configura%C3%A7%C3%A3o-de-token

- Para obter as credenciais para a API do Telegram:
  - Acesse a área de [gestão de apps](https://my.telegram.org/auth?to=apps) no site do telegram.
  - Entre com seu número de telefone em modelo internacional. Com prefixo `+55` para o caso de telefone brasileiro, seguido do DDD local e seu número de telefone.
    - Exemplo: Para telefone de São Paulo, com ddd 11, deverá ser digitado algo como: `+5511995429405`
  - Você receberá um código de autenticação no app do telegram pelo celular. Digite o código no local solicitado e prossiga.
  - Na nova página há um formulário que deve ser preenchido
    - Título do aplicativo: digite qualquer coisa
    - Nome curto: digite qualquer coisa entre 5 e 12 letras
    - URL: ignore
    - Plataforma: Ignore. Pode deixar marcado o padrão Android.
    - Finalize o formulário e aparecerá seus códigos de `api_id` e `api_hash`
  - Para assistir o processo em detalhes, assista [este vídeo](https://www.youtube.com/watch?v=8naENmP3rg4) que exemplifica tudo rapidamente.

### O que é bot token e por que usar?

Bot token é a credencial de acesso para controlar um bot de telegram.

O encaminho de mensagens por bot é mais rápido. O telegram limita a permissão sobre volume de postagens de forma diferente entre a interface de usuário e a interface de bots. Para manter a segurança e ficar livre de punições do telegram, é recomendável que a conta do usuário não encaminhe mais que 6 mensagens por minuto. Já para bots, o limite sobe para 60 mensagens por minuto. Assim, o Clonechat opera 10 vezes mais rápido quando em `mode=bot`.

O uso em modo bot possui algumas exigências:
- O bot precisa ser administrador do canal de origem e destino
- Sua conta do telegram precisa fazer parte do canal de origem
- Caso use a interface Menu, no arquivo `user/config.ini`, a flag `mode` precisa estar como `bot`

### Como gerar um bot token e ativar?

Geração:
- Abra seu app do Telegram, busque por: @BotFather e clique sobre ele;
- Envie o comando: `/newbot`;
- Insira um nome para o seu bot;
- Insira um username. O username obrigatoriamente tem que terminar com a palavra bot. Ex: eusouumbot, tambemsouum_bot.
- Feito isso, você receberá o código bot_token.

Ativação:
- Cadastre o bot_token na flag bot_token do arquivo `credentials.py`. Remova o '#' no início da linha.

### O que é blank_id que aparece no terminal enquanto to clonando?

Isto não é um problema. ID é um código de identificação de postagem. Blank_id significa que o post vinculado aquele ID, não existe mais no canal. Por não existir, você sequer o enxerga no canal.

Imagine que um canal após ter sido criado fez 3 postagens e apagou as 2 primeiras. Você só verá 1 postagem no canal. Mas ao tentar clonar, aparecerá a mensagem de blank_id para o id 1 e para o id 2, até que a clonagem do post de id 3 é executado com sucesso.

Dessa forma, tudo o que estava visível no canal foi clonado, onde o clonechat foi apenas mais informativo, te informando no terminal haviam 2 mensagens que foram deletadas no passado.

### Dá pra usar o clonechat sem ter python instalado?

Existe uma versão independente do clonechat desenvolvida por outra pessoa com implementação online, que pode ser executado por um pc ou celular, sem precisar instalar nada.

Acesse: [https://github.com/Drrivao/Clonechat-Telegram-Colab](https://github.com/Drrivao/Clonechat-Telegram-Colab)


### Posso clonar 2 canais diferentes ao mesmo tempo abrindo outro clonechat?

Não é recomendado pois o telegram pode banir sua conta. O telegram classifica excesso de requisição no uso de sua API como abuso por flood e aplica punição em quem faz isso. O clonechat é configurado para encaminhar mensagens a cada 10 segundos e assim “se comportar” para não ser classificado como flood. Se alguém copia o clone chat em várias pastas diferentes e clona vários canais ao mesmo tempo, o número de requisições enviadas pela mesma conta se multiplicará por 2, 3, 4... Isso eventualmente resultará num banimento da conta por excesso de requisição.

### Existe forma segura de clonar 2 canais ao mesmo tempo?

É possível clonar 2 canais diferentes ao mesmo tempo de forma segura. Para isso tem que usar 2 contas diferentes do telegram. O login de cada conta deve ser realizado numa pasta diferente do clonechat. Para isso,  é preciso fazer uma cópia da pasta do clonechat e nesta nova pasta se certificar que não existe o arquivo `user.session` , pois ele representa o login. Daí é só usar o clonechat dessa nova pasta com uma conta secundária. Não tente usar 2 instâncias do clonechat com a mesma conta do telegram, pois você corre risco de ser banido do telegram por excesso de requisição (flood).

### Apareceu o erro "400 CHAT_FORWARDS_RESTRICTED" quando tentei usar. Como resolver?

O erro `[400 CHAT_FORWARDS_RESTRICTED] - The chat restricts forwarding content (caused by "messages.SendMedia")` é causado por o chat de origem estar configurado com restrição ao encaminhamento de conteúdo. No momento, o clonechat (v109) não é capaz de clonar um canal com essa proteção. Senta e chora. 🙁

### Entendi nada... Tem tutorial mais detalhado?

Tutorial do Polar: [https://upolar.github.io/clonechats-docs/](https://upolar.github.io/clonechats-docs/)

Versão via notebook: [https://github.com/Drrivao/Clonechat-Telegram-Colab](https://github.com/Drrivao/Clonechat-Telegram-Colab)

### Ainda tenho dúvidas... Alguém pode me ajudar?

Entra no grupo do canal abaixo, que talvez outros usuários possam te ajudar
[https://t.me/joinchat/AAAAAE1XGm4ll8QDuMojOg](https://t.me/joinchat/AAAAAE1XGm4ll8QDuMojOg)
