"""
Discord bot entry point for the Sala do Futuro smart room controller.

Loads the DISCORD_TOKEN from the environment (optionally via a .env file),
registers all command handlers, and starts the bot.
"""

import os
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

from sala_do_futuro import SalaDoFuturo

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("sala-do-futuro-bot")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)
sala = SalaDoFuturo()


# ----------------------------------------------------------------------
# Events
# ----------------------------------------------------------------------
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user} (id: {bot.user.id})")
    print(f"🏠 Sala do Futuro pronta com {len(sala.dispositivos)} dispositivo(s) carregado(s).")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            f"❓ Comando não reconhecido. Use `{COMMAND_PREFIX}ajuda` para ver a lista de comandos."
        )
        return

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ Falta um argumento obrigatório: `{error.param.name}`.")
        return

    logger.exception("Erro ao executar comando %s", ctx.command, exc_info=error)
    await ctx.send(f"❌ Ocorreu um erro ao executar o comando: {error}")


# ----------------------------------------------------------------------
# Commands
# ----------------------------------------------------------------------
@bot.command(name="status")
async def status(ctx, *, nome: str = None):
    """Mostra o status de um dispositivo específico ou de todos."""
    await ctx.send(sala.status(nome))


@bot.command(name="dispositivos")
async def dispositivos(ctx):
    """Lista todos os dispositivos cadastrados na sala."""
    await ctx.send(sala.get_dispositivos_info())


@bot.command(name="ligar")
async def ligar(ctx, *, nome: str):
    """Liga um dispositivo. Uso: !ligar <nome>"""
    await ctx.send(sala.ligar(nome))


@bot.command(name="desligar")
async def desligar(ctx, *, nome: str):
    """Desliga um dispositivo. Uso: !desligar <nome>"""
    await ctx.send(sala.desligar(nome))


@bot.command(name="adicionar")
async def adicionar(ctx, nome: str, tipo: str = "generico", *, localizacao: str = "sala"):
    """Adiciona um novo dispositivo. Uso: !adicionar <nome> <tipo> <localizacao>"""
    await ctx.send(sala.adicionar_dispositivo(nome, tipo, localizacao))


@bot.command(name="remover")
async def remover(ctx, *, nome: str):
    """Remove um dispositivo. Uso: !remover <nome>"""
    await ctx.send(sala.remover_dispositivo(nome))


@bot.command(name="ativar")
async def ativar(ctx, *, nome: str):
    """Ativa um dispositivo. Uso: !ativar <nome>"""
    await ctx.send(sala.ativar(nome))


@bot.command(name="desativar")
async def desativar(ctx, *, nome: str):
    """Desativa um dispositivo. Uso: !desativar <nome>"""
    await ctx.send(sala.desativar(nome))


@bot.command(name="salvar")
async def salvar(ctx):
    """Salva o estado atual da sala em disco."""
    await ctx.send(sala.salvar())


@bot.command(name="carregar")
async def carregar(ctx):
    """Recarrega o estado da sala a partir do disco."""
    await ctx.send(sala.carregar())


@bot.command(name="ajuda")
async def ajuda(ctx):
    """Mostra a lista de comandos disponíveis."""
    mensagem = (
        "🤖 **Comandos da Sala do Futuro**\n\n"
        f"`{COMMAND_PREFIX}status [nome]` - Mostra o status de um dispositivo ou de todos\n"
        f"`{COMMAND_PREFIX}dispositivos` - Lista todos os dispositivos cadastrados\n"
        f"`{COMMAND_PREFIX}ligar <nome>` - Liga um dispositivo\n"
        f"`{COMMAND_PREFIX}desligar <nome>` - Desliga um dispositivo\n"
        f"`{COMMAND_PREFIX}adicionar <nome> <tipo> <localizacao>` - Adiciona um novo dispositivo\n"
        f"`{COMMAND_PREFIX}remover <nome>` - Remove um dispositivo\n"
        f"`{COMMAND_PREFIX}ativar <nome>` - Ativa um dispositivo\n"
        f"`{COMMAND_PREFIX}desativar <nome>` - Desativa um dispositivo\n"
        f"`{COMMAND_PREFIX}salvar` - Salva o estado atual em disco\n"
        f"`{COMMAND_PREFIX}carregar` - Recarrega o estado salvo em disco\n"
        f"`{COMMAND_PREFIX}ajuda` - Mostra esta mensagem de ajuda\n"
    )
    await ctx.send(mensagem)


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------
def main():
    if not DISCORD_TOKEN:
        raise RuntimeError(
            "DISCORD_TOKEN não definido. Configure a variável de ambiente DISCORD_TOKEN antes de iniciar o bot."
        )

    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
