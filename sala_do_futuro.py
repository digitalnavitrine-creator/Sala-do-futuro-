"""
SalaDoFuturo - Core logic for the smart room control Discord bot.

This module implements the SalaDoFuturo class, which manages a collection
of smart devices (dispositivos) inside the room. It supports turning
devices on/off, activating/deactivating them, adding/removing devices,
and persisting the room state to a JSON file so it survives restarts.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class SalaDoFuturo:
    """Represents the smart room and manages all of its devices."""

    def __init__(self, storage_file: str = "dispositivos.json"):
        self.storage_file = storage_file
        self.dispositivos: Dict[str, Dict] = {}
        self.carregar()

    # ------------------------------------------------------------------
    # Device management
    # ------------------------------------------------------------------
    def adicionar_dispositivo(
        self,
        nome: str,
        tipo: str = "generico",
        localizacao: str = "sala",
        status: bool = False,
    ) -> str:
        """Add a new device to the room."""
        chave = nome.lower().strip()

        if chave in self.dispositivos:
            return f"⚠️ O dispositivo **{nome}** já existe."

        self.dispositivos[chave] = {
            "nome": nome,
            "status": status,
            "ativo": True,
            "tipo": tipo,
            "localizacao": localizacao,
            "criado_em": datetime.now().isoformat(),
        }
        self.salvar()
        return f"✅ Dispositivo **{nome}** adicionado com sucesso em **{localizacao}**."

    def remover_dispositivo(self, nome: str) -> str:
        """Remove a device from the room."""
        chave = nome.lower().strip()

        if chave not in self.dispositivos:
            return f"❌ Dispositivo **{nome}** não encontrado."

        del self.dispositivos[chave]
        self.salvar()
        return f"🗑️ Dispositivo **{nome}** removido com sucesso."

    # ------------------------------------------------------------------
    # Device control
    # ------------------------------------------------------------------
    def ligar(self, nome: str) -> str:
        """Turn a device on."""
        dispositivo = self._get_dispositivo(nome)
        if dispositivo is None:
            return f"❌ Dispositivo **{nome}** não encontrado."

        if not dispositivo["ativo"]:
            return f"⚠️ O dispositivo **{nome}** está desativado. Ative-o primeiro com !ativar."

        dispositivo["status"] = True
        self.salvar()
        return f"💡 Dispositivo **{dispositivo['nome']}** foi ligado."

    def desligar(self, nome: str) -> str:
        """Turn a device off."""
        dispositivo = self._get_dispositivo(nome)
        if dispositivo is None:
            return f"❌ Dispositivo **{nome}** não encontrado."

        dispositivo["status"] = False
        self.salvar()
        return f"🌑 Dispositivo **{dispositivo['nome']}** foi desligado."

    def ativar(self, nome: str) -> str:
        """Activate (enable) a device so it can be controlled."""
        dispositivo = self._get_dispositivo(nome)
        if dispositivo is None:
            return f"❌ Dispositivo **{nome}** não encontrado."

        dispositivo["ativo"] = True
        self.salvar()
        return f"✅ Dispositivo **{dispositivo['nome']}** foi ativado."

    def desativar(self, nome: str) -> str:
        """Deactivate (disable) a device, turning it off in the process."""
        dispositivo = self._get_dispositivo(nome)
        if dispositivo is None:
            return f"❌ Dispositivo **{nome}** não encontrado."

        dispositivo["ativo"] = False
        dispositivo["status"] = False
        self.salvar()
        return f"⛔ Dispositivo **{dispositivo['nome']}** foi desativado."

    # ------------------------------------------------------------------
    # Status / reporting
    # ------------------------------------------------------------------
    def status(self, nome: Optional[str] = None) -> str:
        """Return a human readable status report for one or all devices."""
        if nome:
            dispositivo = self._get_dispositivo(nome)
            if dispositivo is None:
                return f"❌ Dispositivo **{nome}** não encontrado."
            return self._formatar_dispositivo(dispositivo)

        if not self.dispositivos:
            return "📭 Nenhum dispositivo cadastrado na Sala do Futuro."

        linhas = ["📊 **Status da Sala do Futuro**\n"]
        for dispositivo in self.dispositivos.values():
            linhas.append(self._formatar_dispositivo(dispositivo))
        return "\n".join(linhas)

    def listar_dispositivos(self) -> List[Dict]:
        """Return a list with the info of all devices."""
        return list(self.dispositivos.values())

    def get_dispositivos_info(self) -> str:
        """Return a formatted string listing all registered devices."""
        if not self.dispositivos:
            return "📭 Nenhum dispositivo cadastrado."

        linhas = ["📋 **Dispositivos cadastrados:**\n"]
        for dispositivo in self.dispositivos.values():
            estado = "🟢 Ligado" if dispositivo["status"] else "🔴 Desligado"
            ativo = "Ativo" if dispositivo["ativo"] else "Inativo"
            linhas.append(
                f"• **{dispositivo['nome']}** ({dispositivo['tipo']}) "
                f"- {dispositivo['localizacao']} - {estado} - {ativo}"
            )
        return "\n".join(linhas)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def salvar(self) -> str:
        """Persist the current room state to the JSON storage file."""
        try:
            with open(self.storage_file, "w", encoding="utf-8") as arquivo:
                json.dump(self.dispositivos, arquivo, ensure_ascii=False, indent=4)
            return "💾 Estado da Sala do Futuro salvo com sucesso."
        except OSError as erro:
            return f"❌ Erro ao salvar o estado: {erro}"

    def carregar(self) -> str:
        """Load the room state from the JSON storage file, if it exists."""
        if not os.path.exists(self.storage_file):
            self.dispositivos = {}
            return "📭 Nenhum arquivo de estado encontrado. Iniciando com sala vazia."

        try:
            with open(self.storage_file, "r", encoding="utf-8") as arquivo:
                self.dispositivos = json.load(arquivo)
            return "📂 Estado da Sala do Futuro carregado com sucesso."
        except (OSError, json.JSONDecodeError) as erro:
            self.dispositivos = {}
            return f"❌ Erro ao carregar o estado: {erro}"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_dispositivo(self, nome: str) -> Optional[Dict]:
        return self.dispositivos.get(nome.lower().strip())

    @staticmethod
    def _formatar_dispositivo(dispositivo: Dict) -> str:
        estado = "🟢 Ligado" if dispositivo["status"] else "🔴 Desligado"
        ativo = "Ativo" if dispositivo["ativo"] else "Inativo"
        return (
            f"• **{dispositivo['nome']}** ({dispositivo['tipo']}) "
            f"- {dispositivo['localizacao']} - {estado} - {ativo}"
        )
