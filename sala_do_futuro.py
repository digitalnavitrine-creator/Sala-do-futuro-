"""
Sala do Futuro - Núcleo de controle inteligente de dispositivos.

Este módulo define a classe `SalaDoFuturo`, responsável por gerenciar
o estado de todos os dispositivos inteligentes da sala (luzes, ar
condicionado, projetores, etc), incluindo persistência em disco via
arquivo JSON.
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional


class SalaDoFuturo:
    """
    Gerencia os dispositivos inteligentes da "Sala do Futuro".

    Cada dispositivo é representado por um dicionário com as chaves:
        - nome: str
        - tipo: str
        - localizacao: str
        - status: bool (ligado/desligado)
        - ativo: bool (ativado/desativado)
        - criado_em: str (timestamp ISO)
        - atualizado_em: str (timestamp ISO)
    """

    def __init__(self, arquivo_dados: str = "dispositivos.json"):
        self.arquivo_dados = arquivo_dados
        self.dispositivos: Dict[str, dict] = {}
        self.carregar()

    # ------------------------------------------------------------------ #
    # Persistência
    # ------------------------------------------------------------------ #
    def salvar(self) -> str:
        """Salva o estado atual dos dispositivos em um arquivo JSON."""
        try:
            with open(self.arquivo_dados, "w", encoding="utf-8") as f:
                json.dump(self.dispositivos, f, ensure_ascii=False, indent=4)
            return "💾 Dados salvos com sucesso!"
        except Exception as e:
            return f"❌ Erro ao salvar dados: {e}"

    def carregar(self) -> str:
        """Carrega o estado dos dispositivos a partir do arquivo JSON."""
        if not os.path.exists(self.arquivo_dados):
            self.dispositivos = {}
            return "ℹ️ Nenhum dado salvo encontrado. Iniciando com lista vazia."

        try:
            with open(self.arquivo_dados, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                self.dispositivos = json.loads(conteudo) if conteudo else {}
            return "📂 Dados carregados com sucesso!"
        except Exception as e:
            self.dispositivos = {}
            return f"❌ Erro ao carregar dados: {e}"

    def _chave(self, nome: str) -> str:
        return nome.strip().lower()

    def _timestamp(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    # ------------------------------------------------------------------ #
    # Gerenciamento de dispositivos
    # ------------------------------------------------------------------ #
    def adicionar_dispositivo(self, nome: str, tipo: str, localizacao: str) -> str:
        """Registra um novo dispositivo na Sala do Futuro."""
        chave = self._chave(nome)

        if chave in self.dispositivos:
            return f"⚠️ O dispositivo **{nome}** já existe."

        self.dispositivos[chave] = {
            "nome": nome,
            "tipo": tipo,
            "localizacao": localizacao,
            "status": False,
            "ativo": True,
            "criado_em": self._timestamp(),
            "atualizado_em": self._timestamp(),
        }
        self.salvar()
        return (
            f"✅ Dispositivo **{nome}** ({tipo}) adicionado em "
            f"**{localizacao}** com sucesso!"
        )

    def remover_dispositivo(self, nome: str) -> str:
        """Remove um dispositivo cadastrado."""
        chave = self._chave(nome)

        if chave not in self.dispositivos:
            return f"❌ Dispositivo **{nome}** não encontrado."

        del self.dispositivos[chave]
        self.salvar()
        return f"🗑️ Dispositivo **{nome}** removido com sucesso!"

    def get_dispositivos_info(self) -> str:
        """Retorna uma lista formatada com informações de todos os dispositivos."""
        if not self.dispositivos:
            return "📭 Nenhum dispositivo cadastrado até o momento."

        linhas = ["📋 **Dispositivos da Sala do Futuro:**\n"]
        for dado in self.dispositivos.values():
            status_emoji = "🟢 Ligado" if dado["status"] else "🔴 Desligado"
            ativo_emoji = "✅ Ativo" if dado["ativo"] else "🚫 Inativo"
            linhas.append(
                f"• **{dado['nome']}** ({dado['tipo']}) — {dado['localizacao']}\n"
                f"   {status_emoji} | {ativo_emoji}"
            )
        return "\n".join(linhas)

    # ------------------------------------------------------------------ #
    # Controle de status (ligar / desligar)
    # ------------------------------------------------------------------ #
    def ligar(self, nome: str) -> str:
        """Liga um dispositivo pelo nome."""
        chave = self._chave(nome)

        if chave not in self.dispositivos:
            return f"❌ Dispositivo **{nome}** não encontrado."

        dispositivo = self.dispositivos[chave]

        if not dispositivo["ativo"]:
            return f"🚫 O dispositivo **{dispositivo['nome']}** está desativado e não pode ser ligado."

        if dispositivo["status"]:
            return f"ℹ️ O dispositivo **{dispositivo['nome']}** já está ligado."

        dispositivo["status"] = True
        dispositivo["atualizado_em"] = self._timestamp()
        self.salvar()
        return f"💡 Dispositivo **{dispositivo['nome']}** foi ligado com sucesso!"

    def desligar(self, nome: str) -> str:
        """Desliga um dispositivo pelo nome."""
        chave = self._chave(nome)

        if chave not in self.dispositivos:
            return f"❌ Dispositivo **{nome}** não encontrado."

        dispositivo = self.dispositivos[chave]

        if not dispositivo["status"]:
            return f"ℹ️ O dispositivo **{dispositivo['nome']}** já está desligado."

        dispositivo["status"] = False
        dispositivo["atualizado_em"] = self._timestamp()
        self.salvar()
        return f"🌙 Dispositivo **{dispositivo['nome']}** foi desligado com sucesso!"

    # ------------------------------------------------------------------ #
    # Controle de ativação (ativar / desativar)
    # ------------------------------------------------------------------ #
    def ativar(self, nome: str) -> str:
        """Ativa (habilita) um dispositivo para uso."""
        chave = self._chave(nome)

        if chave not in self.dispositivos:
            return f"❌ Dispositivo **{nome}** não encontrado."

        dispositivo = self.dispositivos[chave]

        if dispositivo["ativo"]:
            return f"ℹ️ O dispositivo **{dispositivo['nome']}** já está ativado."

        dispositivo["ativo"] = True
        dispositivo["atualizado_em"] = self._timestamp()
        self.salvar()
        return f"✅ Dispositivo **{dispositivo['nome']}** foi ativado com sucesso!"

    def desativar(self, nome: str) -> str:
        """Desativa (desabilita) um dispositivo, desligando-o se necessário."""
        chave = self._chave(nome)

        if chave not in self.dispositivos:
            return f"❌ Dispositivo **{nome}** não encontrado."

        dispositivo = self.dispositivos[chave]

        if not dispositivo["ativo"]:
            return f"ℹ️ O dispositivo **{dispositivo['nome']}** já está desativado."

        dispositivo["ativo"] = False
        dispositivo["status"] = False
        dispositivo["atualizado_em"] = self._timestamp()
        self.salvar()
        return f"🚫 Dispositivo **{dispositivo['nome']}** foi desativado com sucesso!"

    # ------------------------------------------------------------------ #
    # Status
    # ------------------------------------------------------------------ #
    def status(self, nome: Optional[str] = None) -> str:
        """Retorna o status de um dispositivo específico ou de todos."""
        if nome is None:
            return self.get_dispositivos_info()

        chave = self._chave(nome)
        if chave not in self.dispositivos:
            return f"❌ Dispositivo **{nome}** não encontrado."

        dado = self.dispositivos[chave]
        status_emoji = "🟢 Ligado" if dado["status"] else "🔴 Desligado"
        ativo_emoji = "✅ Ativo" if dado["ativo"] else "🚫 Inativo"

        return (
            f"📊 **Status de {dado['nome']}**\n"
            f"Tipo: {dado['tipo']}\n"
            f"Localização: {dado['localizacao']}\n"
            f"Estado: {status_emoji}\n"
            f"Situação: {ativo_emoji}"
        )
