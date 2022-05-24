from typing import Any
import punq as punq

container = punq.Container()


class PunqCoreModule:

    @staticmethod
    def add_dependencies_to_resolve(abstract: Any, concrete: Any):
        container.register(abstract, concrete)

    @staticmethod
    def resolve_dependency(abstract: Any) -> Any:
        return container.resolve(abstract)
