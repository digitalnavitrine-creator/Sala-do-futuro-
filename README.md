# Sala do Futuro 🤖💡

Bot do Discord para controle inteligente de dispositivos da "Sala do Futuro",
construído em Python com [discord.py](https://discordpy.readthedocs.io/).

Permite ligar, desligar, ativar, desativar, cadastrar e remover dispositivos
inteligentes diretamente pelo Discord, com persistência de estado em disco
(arquivo `dispositivos.json`), garantindo que as informações sobrevivam a
reinicializações do container.

## ✨ Funcionalidades

- Cadastro e remoção de dispositivos (luzes, ar-condicionado, projetores, etc)
- Controle de ligar/desligar por nome
- Ativação/desativação de dispositivos
- Consulta de status individual ou de todos os dispositivos
- Persistência automática em JSON (salva a cada alteração)
- Mensagens amigáveis em português, com emojis

## 📜 Comandos

| Comando | Descrição |
|---|---|
| `!status [nome]` | Mostra o status de um dispositivo específico ou de todos |
| `!dispositivos` | Lista todos os dispositivos cadastrados |
| `!ligar <nome>` | Liga um dispositivo |
| `!desligar <nome>` | Desliga um dispositivo |
| `!adicionar <nome> <tipo> <localização>` | Cadastra um novo dispositivo |
| `!remover <nome>` | Remove um dispositivo cadastrado |
| `!ativar <nome>` | Ativa um dispositivo |
| `!desativar <nome>` | Desativa um dispositivo |
| `!salvar` | Salva manualmente o estado atual dos dispositivos |
| `!carregar` | Recarrega o estado salvo dos dispositivos |
| `!ajuda` | Mostra a lista de comandos disponíveis |

## 🚀 Como rodar localmente

1. Clone o repositório e acesse a pasta do projeto.
2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Copie o arquivo de exemplo de variáveis de ambiente e configure o seu token:
   ```bash
   cp .env.example .env
   ```
   Edite `.env` e defina `DISCORD_TOKEN` com o token do seu bot, obtido em
   https://discord.com/developers/applications.
5. Rode o bot:
   ```bash
   python main.py
   ```

## 🚂 Deploy no Railway

1. Crie um novo serviço no Railway apontando para este repositório.
2. O Railway detectará o `Dockerfile` e fará o build automaticamente.
3. Defina a variável de ambiente `DISCORD_TOKEN` nas configurações do serviço
   (Settings → Variables).
4. Opcionalmente, defina `COMMAND_PREFIX` para customizar o prefixo dos
   comandos (padrão: `!`).
5. Faça o deploy. O bot ficará online assim que se conectar ao Discord.

> ⚠️ O arquivo `dispositivos.json` é criado automaticamente na primeira
> execução. Para persistência entre deploys, considere anexar um volume
> no Railway apontando para o diretório `/app`.
