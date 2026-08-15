"""Defer direct-runner stdin tempfile deletion on Windows.

genlayer-test 0.29.2 unlinks its temporary fd-0 backing file before fd 0 is
restored. Windows rejects that operation. Installing this shim changes only
the cleanup timing; message encoding and contract execution remain unchanged.
"""

import os
import tempfile


def install() -> None:
    from gltest.direct import loader
    from gltest.direct.vm import VMContext

    if getattr(loader, "_cargo_fact_graph_windows_fix", False):
        return

    def inject_message_windows_safe(vm: VMContext) -> None:
        try:
            from genlayer.py import calldata
            from genlayer.py.types import Address
        except ImportError:
            return

        sender_addr = Address(vm.sender) if isinstance(vm.sender, bytes) else vm.sender
        contract_addr = (
            Address(vm._contract_address)
            if isinstance(vm._contract_address, bytes)
            else vm._contract_address
        )
        origin_addr = Address(vm.origin) if isinstance(vm.origin, bytes) else vm.origin
        message_data = {
            "contract_address": contract_addr,
            "sender_address": sender_addr,
            "origin_address": origin_addr,
            "stack": [],
            "value": vm._value,
            "datetime": vm._datetime,
            "is_init": False,
            "chain_id": vm._chain_id,
            "entry_kind": 0,
            "entry_data": b"",
            "entry_stage_data": None,
        }
        encoded = calldata.encode(message_data)
        fd, path = tempfile.mkstemp()
        try:
            os.write(fd, encoded)
            os.lseek(fd, 0, os.SEEK_SET)
            vm._original_stdin_fd = os.dup(0)
            os.dup2(fd, 0)
            vm._cargo_fact_graph_stdin_path = path
        finally:
            os.close(fd)

    original_cleanup = VMContext._cleanup_after_deactivate

    def cleanup_with_tempfile(self: VMContext) -> None:
        original_cleanup(self)
        path = getattr(self, "_cargo_fact_graph_stdin_path", None)
        if path:
            try:
                os.unlink(path)
            except FileNotFoundError:
                pass
            self._cargo_fact_graph_stdin_path = None

    loader._inject_message_to_fd0 = inject_message_windows_safe
    VMContext._cleanup_after_deactivate = cleanup_with_tempfile
    loader._cargo_fact_graph_windows_fix = True
