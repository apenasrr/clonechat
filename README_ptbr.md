# Clonechat

Clonagem de todas as postagens de um Canal/Grupo do telegram para um outro Canal/Grupo.

Backup seguro. Guarda e protege as postagens no chat destino de eventual derrubada de postagens do chat de origem.

## Configuração
- Execute o arquivo `update_libs.bat` para atualizar as dependências
- Registre suas credenciais de acesso a API do telegram no arquivo `credentials.py`

## USO

### via linha de comando

Comando: python clonechat.py --orig={chat_id do canal/grupo de origem} --dest=-{chat_id do canal/grupo de destino}

Exemplo: python clonechat.py --orig=-100222222 --dest=-10011111111

### Via menu em terminal

- Execute o arquivo `exec_clonechat.bat`
- Digite o chat_id do canal/grupo de origem
- Confirme com [ENTER]
- Digite o chat_id do canal/grupo de destino
- Confirme com [ENTER]

### Finalização

- Apague o arquivo `posted.json` ao terminar a clonagem.

Observação: Caso este arquivo não seja apagado, na próxima vez que executar o script a clonagem será continuada de onde parou.

## Dúvidas

### Como conseguir o chat_id de um canal ou grupo

Existem várias formas de obter o chat_id de um canal. Mostraremos duas delas:
- Usando o telegram client [Kotatogram](https://kotatogram.github.io/download/):
  - Acesse a tela de descrição do canal
  - Copie o `chat_id` que aparece abaixo do nome do canal
- Usando bot Find_TGIDbot:
  - Acesse a janela do bot [@Find_TGIDbot](http://t.me/Find_TGIDbot) e o inicie
  - Encaminhe qualquer postagem do canal para este bot
  - O bot responderá com o ID do remetente da mensagem. Neste caso, o ID do canal.
- Copie o `chat_id` (incluindo o sinal de subtração). Vale ressaltar que canais começam com o número '-100'.

### Como gerar credenciais de acesso a API do telegram?

- Leia o tópico "Configuração de token" do tutorial encontrado em: https://github.com/apenasrr/zimatise_docs#configura%C3%A7%C3%A3o-de-token
