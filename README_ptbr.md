
# Clonechat

Clona todas as postagens de um Canal/Grupo do telegram para um outro Canal/Grupo.

Backup seguro. Guarda e protege as postagens no chat destino de eventual derrubada de postagens no chat de origem.

**O que é clonar uma postagem e porque isso é importante?**

Clonar uma postagem é encaminhar uma mensagem de um chat para outro enquanto se remove o remetente original. Isso é importante pois protege a mensagem encaminhada caso o canal de origem da mensagem seja excluído ou até derrubado internamente pelo telegram. Ao clonar uma mensagem, a versão clonada se torna independente de sua origem. Assim ao clonar um canal inteiro para um canal pessoal seu, você terá uma cópia segura **sem risco** de "sumir" misteriosamente algum dia.

**Talvez você não precise do Clonechat, sabia?**

Se você deseja clonar apenas 1 ou poucos canais, use o aplicativo **64gram** que será mais rápido e fácil para clonar grupos e canais. Ele é uma versão modificada do telegram desktop muito popular e que possui várias funções extras, incluindo obter o ID de qualquer chat (canal ou grupo) e usuário. Além disso, tem a função de clonar conjuntos de até 100 postagens por vez.

[Acesse o github](https://github.com/TDesktop-x64/tdesktop/releases) ou o [canal do telegram](http://t.me/tg_x64) e baixe a versão "x64.zip" mais recente do 64gram.
Após baixar, instale e abra o aplicativo. Faça login com sua conta do telegram e siga as instruções para clonar o canal desejado:
- Crie um canal novo para receber os posts clonados
- Vá no canal que você deseja clonar
- Selecione os posts, clique com o botão direito em um deles, clique em "Forward selected w/o quote"
- Agora selecione o canal ou grupo criado para ser o destino da clonagem e clicar em "Send".

**E quando o Clonechat vale a pena ser usado?**

Em duas situações:
- Quando o canal que você deseja clonar, está com "conteúdo protegido", impedindo que se encaminhe mensagens.
- Ou quando você deseja clonar muitos canais, ou canais com milhares de postagens, sendo assim interessante automatizar o processo.

Se essa for sua situação, o CloneChat pode te ajudar. 😁

**Funções**

- Clonar as postagens de um canal/grupo para outro canal/grupo. Use o `exec_clonechat.bat`
- Clonar as postagens de um canal/grupo com **conteúdo protegido** (mas é bem lento). Use `exec_clonechat_protect_dw.bat` e `exec_clonechat_protect_up.bat`
- Baixar TODOS os arquivos de um canal (fotos, vídeos, áudios, documentos, etc) e salva em ordem de postagem. Use `exec_downloadall.bat`

**Problemas conhecidos**
- No clonechat_protect, sem usar conta premium do telegram, ao tentar clonar uma postagem com texto muito longo ou arquivos com mais de 2000 MiB, vai resultar em erro. Isso ocorre porque postagem com essas características só podem ser criadas por uma conta premium do telegram. No futuro a situação será contornada com uma postagem particionada do texto ou documento.
- Grupo habilitado com "tópicos" não é suportado pelo Clonechat. Ainda...

## Configuração
- Instale o Python
  - Acesse o site python.org e [baixe](https://www.python.org/downloads/) a versão estável mais nova
  - Instale. No form "Advanced Options", marque `Add python 3.?? to PATH`
- Será que funcionou? Teste:
  - Abra um terminal e digite `python --version`
    - Se aparecer a versão do python, está tudo certo
    - Se não aparecer. Peça ajuda com humildade e educação no grupo do telegram que está ao final deste tutorial.
  - Abra um terminal e digite `where pip`
    - Se aparecer o caminho do gerenciador de pacote pip, está tudo certo.
    - Se não aparecer, chore por 1 minuto 😭. Agora vá na seção de ["Perguntas frequentes"](#perguntas-frequentes) e procure por "Instalar o PIP".
- Crie o ambiente virtual e instale as dependências
  - Execute o arquivo `install.bat`
  - No futuro, se o clonechat gerar muitos erros, execute o arquivo `update_libs.bat` para atualizar as dependências.


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

Se for a primeira vez que você está usando o clonechat, é preciso instalar um ambiente virtual.
- Execute o arquivo `install.bat`

> Deu erro? No final do tutorial tem uma seção de perguntas frequentes que pode te ajudar. Também existe um tutorial alternativo mais detalhado. E até um grupo cheio de pessoas que podem tirar dúvidas 😁

### Clonar canal/grupo que aceita encaminhamento

Você precisa ter o api_id e api_hash da sua conta antes de executar o clonechat.

- Execute o arquivo `exec_clonechat.bat`
- Digite o chat_id, link de convite ou username do canal/grupo de origem. Se o `ctrl+v` não funcionar, clique com o botão direito do mouse no terminal
- Confirme com [ENTER]
- Digite o chat_id, link de convite ou username do canal/grupo de destino
- Confirme com [ENTER]
- No menu de escolha de tipos de arquivos
  - Digite uma opção de filtro, de arquivos
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
  - Por fim, se você tiver "segurança de 2 fatores" (2fa) ativado na sua conta, será solicitado sua senha.
  - Ao executar o `exec_clonechat.bat`, será solicitado seu api_id e api_hash. Você só precisa os informar uma vez, pois as demais conexões serão realizadas por um arquivo de sessão que será criado na pasta do clonechat.

Aguarde a clonagem terminar!

> Importante: Clonagem via usuário (mode=user) possui uma pausa de 10 segundos entre posts. Já clonagem via bot (mode=bot) é mais rápido, possuindo uma pausa de apenas 1 segundo entre posts. Se você desejar usar o clonechat em maior velocidade, gere um bot token e mude flag "mode" de "user" para "bot" no arquivo de configuração em `user/config.ini`. Este modo funciona apenas para clonagem de canal que você é dono e pode por seu bot pessoal como administrador.

### Clonar canal/grupo com conteúdo protegido

Um Canal/Grupo tem conteúdo protegido quando você **não consegue** encaminhar mensagens dele.

Você precisa ter o api_id e api_hash da sua conta antes de executar o clonechat.

- Execute o arquivo `exec_clonechat_protect_dw.bat` e também o `exec_clonechat_protect_up.bat`

> *Por que precisa executar os 2? Por que um vai baixando as postagens da origem enquanto o outro vai enviando as postagens pro destino. Trabalham juntos.*

- O passo a passo para o uso de cada um dos dois scripts é bem parecido com o que foi descrito no tópico anterior. Apenas siga as instruções do terminal.

### Opção 2: via linha de comando (desatualizado)

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

### Instalar o PIP

PIP é um gerenciador de pacotes do python. Normalmente ele já vem instalado com o python. Para verificar se você tem o pip instalado, abra um terminal e digite `where pip`. Se aparecer o caminho do pip, está tudo certo.
Se não aparecer, você pode instalar o pip com:
- o comando `python -m ensurepip`.
- Se não funcionar, abra o terminal como administrador.
- Execute o comando: `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
- Em seguida, digite: `python get-pip.py`
- Feche o terminal. Abra novamente, digite `where pip`.
- Se aparecer o caminho do pip, está tudo certo.
- Se não aparecer, peça ajuda pelo link do grupo do telegram que está ao final deste tutorial.

### Como conseguir o chat_id de um canal ou grupo

Existem várias formas de obter o chat_id de um canal. Mostraremos algumas delas:
- Usando o telegram client [64gram](https://github.com/TDesktop-x64/tdesktop/releases):
  - Acesse a tela de descrição do canal
  - Copie o `chat_id` que aparece abaixo do nome do canal
- Opção 2 - Através do link de postagem
  - Clique com o botão direito numa postagem do canal ou grupo que deseja clonar e clique em "Copiar link".
  - Cole num editor de texto.
  - Remove o texto `https://t.me/c/` do início.
  - Remova a barra e número que aparecer ao final. Exemplo: de `2031251722/1612` para `2031251722`. Esse número ao final representa o ID da mensagem, que não é útil
  - Prévia: O link `https://t.me/c/2031251722/1612` se tornou `2031251722`.
  - Agora adicione o prefixo `-100` ao número. Exemplo: `2031251722` se torna `-1002031251722`. Esse é o chat_id do canal ou grupo.
- Opção 3 - Através de um bot que informa chat_id de canal, mas não de grupo.
  - Acesse e inicie bot [@myidbot](http://t.me/myidbot)
  - Encaminhe qualquer postagem do canal para este bot
  - O bot responderá com o ID do remetente da mensagem. Neste caso, o ID do canal.
  - Copie o `chat_id` (incluindo o sinal de subtração).
  - *Atenção:* Se você encaminhar mensagem de um grupo ao invés de canal, o bot vai informar o user_id da pessoa que escreveu a mensagem. Então não é útil para ser usado no clonechat.
- Opção 4 -  Pede pra um amigo que tem 64gram 😅

### Qual a diferença de "Grupo" e "Canal" no telegram?

- Grupo: Qualquer pessoa pode entrar e participar. O administrador pode definir quem pode enviar mensagens e quem não pode.
- Canal: É uma plataforma de transmissão. Apenas o administrador pode enviar mensagens. Os membros do canal não podem enviar mensagens.

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
    - Salve em um local seguro e **não compartilhe com ninguém**. Estes códigos são como senha de acesso a sua conta do telegram.
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

Salve o bot_token em um local seguro.

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

O erro `[400 CHAT_FORWARDS_RESTRICTED] - The chat restricts forwarding content (caused by "messages.SendMedia")` é causado por o chat de origem estar configurado com restrição ao encaminhamento de conteúdo. Mas isso não é problema! O clonechat possui uma função específica para essa situação. Leia as instruções no tópico "Clonar canal/grupo com conteúdo protegido".

### Entendi nada... Tem tutorial mais detalhado?

Tutorial alternativo: [Guia wandrey7](https://wandrey7.github.io/guiaclonechat/)

### Ainda tenho dúvidas... Alguém pode me ajudar?

Entra no grupo do canal abaixo, que talvez outros usuários possam te ajudar
[https://t.me/joinchat/AAAAAE1XGm4ll8QDuMojOg](https://t.me/joinchat/AAAAAE1XGm4ll8QDuMojOg)
