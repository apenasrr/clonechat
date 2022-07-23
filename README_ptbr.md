
# Clonechat

Clona todas as postagens de um Canal/Grupo do telegram para um outro Canal/Grupo.

Backup seguro. Guarda e protege as postagens no chat destino de eventual derrubada de postagens no chat de origem.

## Configuração
- Instale o Python
  - Acesse o site python.org e [baixe](https://www.python.org/downloads/) a versão estável mais nova
  - IMPORTANTE: Antes de clicar para instalar marque a opção `Add python 3.?? to PATH` no final do instalador (no lugar de `??` vão ser números)
  - Instale.
- Atualize as dependências
  - Execute o arquivo `update_libs.bat` para atualizar as dependências
  - Espere terminar e aperte qualquer tecla para continuar.
- Cadastre suas credenciais
  - Abra o bloco de notas ou outro editor de texto
  - Arraste o arquivo `credentials.py` para dentro do bloco de notas ou do editor de texto
    - Registre suas credenciais de acesso a API (api_id e api_hash) do Telegram
    > Não sabe obter api_id e api_hash? Veja o tópico ["Perguntas frequentes"](#perguntas-frequentes)
    - Caso seu api_id seja `1111123` e o api_hash seja `sKwrdX7tb2xFDkPU9h0AsKwrdX7tb2xF` o arquivo deve ficar preenchido da seguinte maneira:
    ~~~python
      api_id = 1111123
      api_hash = "sKwrdX7tb2xFDkPU9h0AsKwrdX7tb2xF"
    ~~~
    - Os valores informados acima são apenas exemplos. Os valores são inválidos
    - Salve e feche o arquivo
    


## USO

Para usar você precisa do chat_id do canal de origem e o chat_id do canal de destino.

> Não sabe obter chat_id de um grupo/canal? Veja o tópico ["Como conseguir o chat id de um canal ou grupo"](#como-conseguir-o-chatid-de-um-canal-ou-grupo)

### Opção 1: Via menu em terminal

- Execute o arquivo `exec_clonechat.bat`
- Digite o chat_id do canal/grupo de origem. Se o `ctrl+v` não funcionar, clique com o botão direito do mouse no terminal
- Confirme com [ENTER]
- Digite o chat_id do canal/grupo de destino.
- Confirme com [ENTER]
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

### Opção 2: via linha de comando

- Abra o terminal do windows na pasta do clone chat e digite:

Comando: python clonechat.py --orig={chat_id do canal/grupo de origem} --dest=-{chat_id do canal/grupo de destino}

Exemplo: `python clonechat.py --orig=-100222222 --dest=-10011111111`

### Finalização

- Ao terminar a clonagem, apague o arquivo `posted.json` caso não vá mais copiar o canal!

> Observação: Caso este arquivo não seja apagado, na próxima vez que executar o script via linha de comando a clonagem será continuada de onde parou (desde que escolhida a opção `2` ao iniciar o programa).

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
- Copie o `chat_id` (incluindo o sinal de subtração). Vale ressaltar que canais começam com o número '-100'.

### Como gerar credenciais de acesso a API do telegram?

- Leia o tópico "Configuração de token" do tutorial encontrado em: https://github.com/apenasrr/zimatise_docs#configura%C3%A7%C3%A3o-de-token

- Para obter as credenciais para a API do Telegram:
  - Acesse a área de [gestão de apps](https://my.telegram.org/auth?to=apps) no site do telegram.
  - Entre com seu número de telefone em modelo internacional. Com prefixo `+55` para o caso de telefone brasileiro, seguido do DDD local e seu número de telefone.
    - Exemplo: Para telefone de São Paulo, com ddd 11, deverá ser digitado algo como: `+5511995429405`
  - Preencha o formulário
    - Título do aplicativo: digite qualquer coisa
    - Nome curto: digite qualquer coisa entre 5 e 12 letras
    - URL: ignore
    - Plataforma: Ignore. Pode deixar marcado o padrão Android.
    - Finalize o formulário e aparecerá seus códigos de `api_id` e `api_hash`
  - Para assistir o processo em detalhes, assista [este vídeo](https://www.youtube.com/watch?v=8naENmP3rg4) que exemplifica tudo rapidamente.
