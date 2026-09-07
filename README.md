# Sala do Futuro - Discord Bot

Smart room control Discord bot built with `discord.py`. Manages virtual
devices (lights, sensors, appliances, etc.) for the "Sala do Futuro" project,
with state persisted to disk so it survives restarts.

## Commands

| Command | Description |
| --- | --- |
| `!status [nome]` | Shows the status of a device, or all devices if no name is given |
| `!dispositivos` | Lists all registered devices |
| `!ligar <nome>` | Turns a device on |
| `!desligar <nome>` | Turns a device off |
| `!adicionar <nome> <tipo> <localizacao>` | Registers a new device |
| `!remover <nome>` | Removes a device |
| `!ativar <nome>` | Activates a device |
| `!desativar <nome>` | Deactivates a device |
| `!salvar` | Persists the current state to disk |
| `!carregar` | Reloads the state from disk |
| `!ajuda` | Shows the help message |

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your DISCORD_TOKEN
python main.py
```

## Deployment (Railway)

This service is deployed via the included `Dockerfile`. Set the
`DISCORD_TOKEN` environment variable in Railway before deploying; the bot
will fail fast with a clear error if it is missing.
