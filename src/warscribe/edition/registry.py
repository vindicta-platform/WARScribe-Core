"""
Edition Registry.

Manages discovery and registration of edition plugins.
"""

from typing import Optional

from warscribe.edition.plugin import EditionPlugin


class EditionRegistry:
    """
    Registry for edition plugins.
    
    Provides discovery and access to installed edition plugins.
    """
    
    def __init__(self) -> None:
        self._editions: dict[str, EditionPlugin] = {}
        self._default: Optional[str] = None
    
    def register(self, plugin: EditionPlugin, set_default: bool = False) -> None:
        """Register an edition plugin."""
        self._editions[plugin.edition_code] = plugin
        if set_default or self._default is None:
            self._default = plugin.edition_code
    
    def get(self, edition_code: str) -> Optional[EditionPlugin]:
        """Get an edition plugin by code."""
        return self._editions.get(edition_code)
    
    def get_default(self) -> Optional[EditionPlugin]:
        """Get the default edition plugin."""
        if self._default:
            return self._editions.get(self._default)
        return None
    
    @property
    def available_editions(self) -> list[str]:
        """List available edition codes."""
        return list(self._editions.keys())
    
    def __len__(self) -> int:
        return len(self._editions)
    
    def __contains__(self, edition_code: str) -> bool:
        return edition_code in self._editions
