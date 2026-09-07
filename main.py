"""
Sala do Futuro - Bot do Discord

Ponto de entrada principal do bot. Registra os comandos e conecta ao
Discord utilizando o token definido na variável de ambiente
`DISCORD_TOKEN`.
"""

import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from sala_do_futuro import SalaDoFuturo

# ---------------------------------------------------------------------- #
# Configuração de ambiente e logging
# ---------------------------------------------------------------------- #
# `load_dotenv()` só tem efeito quando existe um arquivo `.env` no diretório
# atual, o que é útil para desenvolvimento local. Em produção (ex.: Railway),
# as variáveis de ambiente já são injetadas diretamente pelo provedor, então
# a ausência de um `.env` não deve impedir o bot de iniciar.
try:
    load_dotenv()
except Exception:
    # Não é crítico se o carregamento do .env falhar (ex.: arquivo ausente
    # ou sem permissão de leitura). As variáveis de ambiente do sistema
    # continuam disponíveis normalmente via os.getenv().
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("sala-do-futuro")

# Lê diretamente do ambiente do processo. Isso funciona tanto para variáveis
# carregadas de um `.env` local quanto para variáveis injetadas pela
# plataforma de deploy (Railway, Docker, etc.).
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", "!")

# ---------------------------------------------------------------------- #
# Instâncias principais
# ---------------------------------------------------------------------- #
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)
sala = SalaDoFuturo()


# ---------------------------------------------------------------------- #
# Eventos
# ---------------------------------------------------------------------- #
@bot.event
async def on_ready():
    logger.info("Bot conectado como %s (ID: %s)", bot.user, bot.user.id)
    print(f"✅ {bot.user} está online e pronto na Sala do Futuro!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "❓ Comando não reconhecido. Digite `!ajuda` para ver a lista de comandos."
        )
        return

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f"⚠️ Faltam argumentos para este comando. Use `!ajuda` para mais detalhes."
        )
        return

    logger.exception("Erro ao executar comando '%s': %s", ctx.command, error)
    await ctx.send(f"❌ Ocorreu um erro ao executar o comando: `{error}`")


# ---------------------------------------------------------------------- #
# Comandos
# ---------------------------------------------------------------------- #
@bot.command(name="status")
async def status(ctx, *, nome: str = None):
    """Mostra o status de um dispositivo específico ou de todos."""
    await ctx.send(sala.status(nome))


@bot.command(name="dispositivos")
async def dispositivos(ctx):
    """Lista todos os dispositivos cadastrados."""
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
async def adicionar(ctx, nome: str, tipo: str, *, localizacao: str):
    """Cadastra um novo dispositivo. Uso: !adicionar <nome> <tipo> <localização>"""
    await ctx.send(sala.adicionar_dispositivo(nome, tipo, localizacao))


@bot.command(name="remover")
async def remover(ctx, *, nome: str):
    """Remove um dispositivo cadastrado. Uso: !remover <nome>"""
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
    """Salva manualmente o estado dos dispositivos."""
    await ctx.send(sala.salvar())


@bot.command(name="carregar")
async def carregar(ctx):
    """Recarrega o estado dos dispositivos a partir do arquivo salvo."""
    await ctx.send(sala.carregar())


@bot.command(name="ajuda")
async def ajuda(ctx):
    """Mostra a lista de comandos disponíveis."""
    mensagem = (
        "🤖 **Sala do Futuro — Comandos disponíveis**\n\n"
        "`!status [nome]` — Mostra o status de um dispositivo ou de todos\n"
        "`!dispositivos` — Lista todos os dispositivos cadastrados\n"
        "`!ligar <nome>` — Liga um dispositivo\n"
        "`!desligar <nome>` — Desliga um dispositivo\n"
        "`!adicionar <nome> <tipo> <localização>` — Cadastra um novo dispositivo\n"
        "`!remover <nome>` — Remove um dispositivo cadastrado\n"
        "`!ativar <nome>` — Ativa um dispositivo\n"
        "`!desativar <nome>` — Desativa um dispositivo\n"
        "`!salvar` — Salva o estado atual dos dispositivos\n"
        "`!carregar` — Recarrega o estado salvo dos dispositivos\n"
        "`!ajuda` — Mostra esta mensagem de ajuda"
    )
    await ctx.send(mensagem)


# ---------------------------------------------------------------------- #
# Inicialização
# ---------------------------------------------------------------------- #
def main():
    if not DISCORD_TOKEN:
        logger.error(
            "A variável de ambiente DISCORD_TOKEN não está definida. "
            "Configure-a antes de iniciar o bot."
        )
        raise SystemExit(1)

    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
