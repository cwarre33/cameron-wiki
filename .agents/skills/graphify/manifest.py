# re-export manifest helpers from detect for backwards compatibility
from graphify.detect import detect_incremental, load_manifest, save_manifest

__all__ = ["detect_incremental", "load_manifest", "save_manifest"]
