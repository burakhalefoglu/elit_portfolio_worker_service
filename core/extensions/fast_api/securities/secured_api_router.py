from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    Union,
)
from fastapi.datastructures import Default
from fastapi.routing import APIRoute
from fastapi.utils import (
    generate_unique_id,
)
from starlette import routing
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute
from starlette.routing import Mount as Mount  # noqa
from starlette.types import ASGIApp
from fastapi import APIRouter, Depends, params

from core.extensions.fast_api.securities.jwt_bearer import JWTBearer


class SecuredApiRouter(APIRouter):
    """
        SecuredApiRouter has JWTBearer dependencies
    """
    def __init__(self,
                 *,
                 prefix: str = "",
                 tags: Optional[List[Union[str, Enum]]] = None,
                 dependencies: Optional[Sequence[params.Depends]] = None,
                 default_response_class: Type[Response] = Default(JSONResponse),
                 responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
                 callbacks: Optional[List[BaseRoute]] = None,
                 routes: Optional[List[routing.BaseRoute]] = None,
                 redirect_slashes: bool = True,
                 default: Optional[ASGIApp] = None,
                 dependency_overrides_provider: Optional[Any] = None,
                 route_class: Type[APIRoute] = APIRoute,
                 on_startup: Optional[Sequence[Callable[[], Any]]] = None,
                 on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
                 deprecated: Optional[bool] = None,
                 include_in_schema: bool = True,
                 generate_unique_id_function: Callable[[APIRoute], str] = Default(
                     generate_unique_id
                 )):
        self.dependencies = dependencies
        if dependencies is None:
            self.dependencies = Depends(JWTBearer())
        else:
            self.dependencies.append(Depends(JWTBearer()))

        super(SecuredApiRouter, self).__init__(prefix=prefix,
                                               tags=tags,
                                               default_response_class=default_response_class,
                                               dependencies=dependencies,
                                               responses=responses,
                                               callbacks=callbacks,
                                               routes=routes,
                                               redirect_slashes=redirect_slashes,
                                               default=default,
                                               dependency_overrides_provider=dependency_overrides_provider,
                                               route_class=route_class,
                                               on_startup=on_startup,
                                               on_shutdown=on_shutdown,
                                               deprecated=deprecated,
                                               include_in_schema=include_in_schema,
                                               generate_unique_id_function=generate_unique_id_function)
