"""git-dit package

Minimal package metadata and exported version.
"""

__version__ = "1.0.0"

# 尽量避免在包初始化时立即导入可能不存在或导致循环导入的子模块。
# 如果 `core` 不存在或导入失败，只做弱化处理，不阻塞包的其他导入。
try:
	from . import core  # re-export for convenience (stubs)
except Exception:
	core = None

__all__ = ["__version__"]
if core is not None:
	__all__.append("core")
