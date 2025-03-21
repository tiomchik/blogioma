from typing import Any

from main.context import get_base_context


class DataMixin():
    login_url = "log_in"

    def get_base_context(self, name: str, **kwargs) -> dict[str, Any]:
        return get_base_context(self.request, name, **kwargs)
