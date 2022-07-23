
# Clonechat

Clona todas as postagens de um Canal/Grupo do telegram para um outro Canal/Grupo.

Backup seguro. Guarda e protege as postagens no chat destino de eventual derrubada de postagens no chat de origem.

## Configuração
- Instale o Python
  - Acesse o site python.org e [baixe](https://www.python.org/downloads/) a versão estável mais nova
  - Instale. No form 'Advanced Options', marque `Add python 3.?? to PATH`
- Atualize as dependências
  - Execute o arquivo `update_libs.bat` para atualizar as dependências
  - Se aparecer a mensagem
- Cadastre suas credenciais
  - Abra o bloco de notas ou qualquer editor de texto
  - Arraste o arquivo `credentials.py` para dentro do editor
    - Registre suas credenciais de acesso a API (api_id e api_hash) do telegram
    - Exemplo de preenchimento:
      - `api_id = 1111111`
      - `api_hash = "sKwrdX7tb2xFDkPU9h0AsKwrdX7tb2xF"`
    - Os valores informados acima são apenas exemplos. Os valores são inválidos
    - Salve e feche o arquivo
  - Se você desejar usar o clonechat em maior velocidade, gere um bot token e registre na flag bot_token

> Não sabe obter api_id, api_hash ou bot_token? Veja o tópico "Perguntas frequentes"

## USO

### Opção 1: Via menu em terminal

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

Aguarde a clonagem terminar!

> Importante: Clonagem via usuário (mode=user) possui uma pausa de 10 segundos entre posts. Já clonagem via bot (mode=bot) é mais rápido, possuindo uma pausa de apenas 1 segundo entre posts.

### Opção 2: via linha de comando

> Abra o terminal do windows na pasta do clone chat e digite:

Comando: python clonechat.py --orig={chat_id do canal/grupo de origem} --dest=-{chat_id do canal/grupo de destino}

Exemplo: `python clonechat.py --orig=-100222222 --dest=-10011111111`

### Finalização

- Ao terminar a clonagem, apague o arquivo `posted.json`.

> Observação: Caso este arquivo não seja apagado, na próxima vez que executar o script via linha de comando a clonagem será continuada de onde parou.

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
- Vale ressaltar que canais começam com o número '-100'. O kotatogram não informa o prefixo '-100', então você deve o digitar manualmente.
> Exemplo de um código de canal: `-1001623956859`

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
- No arquivo `config.ini`, a flag `mode` precisa ser alterada para `bot`
- O bot precisa ser administrador do canal de origem
- Sua conta do telegram precisa fazer parte do canal de origem

### Como gerar um bot token e ativar?

Geração:
- Abra seu app do Telegram, busque por: @BotFather e clique sobre ele;
- Envie o comando: `/newbot`;
- Insira um nome para o seu bot;
- Insira um username. O username obrigatoriamente tem que terminar com a palavra bot. Ex: eusouumbot, tambemsouum_bot.
- Feito isso, você receberá o código bot_token.

Ativação:
- Cadastre o bot_token na flag bot_token do arquivo `credentials.py`. Remova o '#' no início da linha.
