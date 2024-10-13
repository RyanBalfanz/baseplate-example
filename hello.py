import typing

from baseplate import Baseplate, Span
from baseplate.clients.sqlalchemy import SQLAlchemySession
from baseplate.frameworks.pyramid import BaseplateConfigurator, BaseplateRequest
from pyramid.config import Configurator
from pyramid.view import view_config
from sqlalchemy import text
from sqlalchemy.orm import Session


class BaseplateRequestContextObjectFactory[T](typing.Protocol):
    def make_object_for_context(self, name: str, span: Span) -> T: ...


class BaseplateContextSpec(typing.TypedDict):
    """Context object specification for Baseplate."""

    db: SQLAlchemySession


class RequestContext(typing.Protocol):
    """Context object for Baseplate."""

    db: Session

    # class BaseplateContextSpec(typing.TypedDict):
    #     """Context object specification for Baseplate."""
    #     db: SQLAlchemySession


@view_config(route_name="hello_world", renderer="json")
def hello_world(request: BaseplateRequest | RequestContext):
    # result = request.db.execute("SELECT date('now');")
    # sqlalchemy.exc.ArgumentError: Textual SQL expression "SELECT date('now');" should be explicitly declared as text("SELECT date('now');")
    result = request.db.execute(text("SELECT date('now');"))
    return {"Hello": "World", "Now": result.scalar()}


def make_wsgi_app(app_config):
    baseplate = Baseplate(app_config)
    baseplate.configure_observers()
    context_spec = BaseplateContextSpec(db=SQLAlchemySession())
    baseplate.configure_context(context_spec)

    configurator = Configurator(settings=app_config)
    configurator.include(BaseplateConfigurator(baseplate).includeme)
    configurator.add_route("hello_world", "/", request_method="GET")
    configurator.scan()

    return configurator.make_wsgi_app()
