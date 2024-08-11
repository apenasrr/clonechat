# ReleaseNotes

**v118 2024-08-11**
- Feat: Para grupo com função de tópicos, agora existe capacidade de baixar todos os arquivos de um tópico específico através do `exec_downloadall.bat` e colando o link de uma mensagem do tópico. Também funciona para grupo com conteúdo protegido.

**v117 2024-08-09**
- Fix: Erro "KeyError file_name" ao executar clonechat_protect_dw.

**v116 2024-08-08**
- Fix: clonechat_protect_up gerava erro "`json.decoder.JSONDecodeError`" ao executar a função show_history_overview. Causado por o histórico estar em processo de download. Agora emite mensagem de espera pelo download do histórico.

**v115 2024-07-18**
- Fix: clonechat_protect_up não encontrava arquivo de histórico do chat
- Fix: DownloadAll gerando NotADirectoryError em chats com título contendo caracteres especiais

**v114 2024-07-16**
- Feat: clonechat_protect aceita identificação de canal ou grupo por link de mensagem

**v113 2024-07-15**
- Fix: Chats com título contendo caracteres especiais não geram mais erro no sistema de arquivos

**v112 2024-07-14**
- Refact: clonechat_protect com esteira de download separada da esteira de upload
- Feat: Scripts de execução baseado em ambiente virtual. Script de criar ambiente virtual (install.bat)