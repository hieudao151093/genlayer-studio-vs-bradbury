# =============================================================================
# header_gotcha.py
#
# DEMONSTRATION: the #1 reason newcomers fail their first deploy on hosted Studio.
#
# The first line below is the DEPENDENCY HEADER. It pins the genvm/SDK version.
#
#   - Tutorials and blog posts often use:   # { "Depends": "py-genlayer:test" }
#     -> On hosted Studio (studio.genlayer.com, v0.2.16) this FAILS at schema load
#        with: "Could not load contract schema" / gen_getContractSchemaForCode:
#        execution failed.  The `:test` tag is for local CLI/localnet, not hosted.
#
#   - The working header on hosted studionet pins the exact version hash, e.g.:
#         # { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
#
#   - IMPORTANT: the correct hash can DIFFER per environment. Before deploying to
#     Bradbury, copy the header from a known-good example contract IN THAT
#     environment, or check the docs for the current Bradbury genvm version.
#     Document the exact hash you used for each environment in the README.
#
# The two header lines below are the canonical "always put these first" lines.
# Keep this version (the hash) — swap the hash if Bradbury requires a different one.
# =============================================================================

# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


# A minimal deterministic contract — identical logic to the canonical storage example,
# used here only so the header behavior is what's being demonstrated, not the logic.
class HeaderGotcha(gl.Contract):
    storage_str: str

    def __init__(self, initial_str_storage: str):
        self.storage_str = initial_str_storage

    @gl.public.view
    def get_storage(self) -> str:
        return self.storage_str

    @gl.public.write
    def update_storage(self, new_storage: str) -> None:
        self.storage_str = new_storage
