from .config import ConfigBuilder

config = ConfigBuilder().env().build()

__all__ = ["ConfigBuilder", "config"]