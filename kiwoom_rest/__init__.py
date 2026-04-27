from .core import KiwoomCore, KiwoomException
from .client import KiwoomClient
from .generated import KiwoomGeneratedClient, API_ID_TO_RES_MODEL, API_ID_TO_REQ_MODEL, API_ID_TO_METHOD

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

__all__ = [
    "KiwoomClient",
    "KiwoomCore",
    "KiwoomException",
    "KiwoomGeneratedClient",
    "API_ID_TO_RES_MODEL",
    "API_ID_TO_REQ_MODEL",
    "API_ID_TO_METHOD",
    "__version__"
]