from flask import Blueprint

from src.api.controllers.poll import PollController
from src.core.config import settings


polls_blueprint = Blueprint(
    'polls',
    __name__,
    url_prefix=f"{settings.API_PREFIX}/{settings.API_VERSION}/polls"
)

poll_controller = PollController()

polls_blueprint.add_url_rule(
    '',
    view_func=poll_controller.get_polls,
    methods=['GET']
)

polls_blueprint.add_url_rule(
    '',
    view_func=poll_controller.create_poll,
    methods=['POST']
)

polls_blueprint.add_url_rule(
    '/<int:poll_id>',
    view_func=poll_controller.get_poll,
    methods=['GET']
)

polls_blueprint.add_url_rule(
    '/<int:poll_id>',
    view_func=poll_controller.update_poll,
    methods=['PUT', 'PATCH']
)

polls_blueprint.add_url_rule(
    '/<int:poll_id>',
    view_func=poll_controller.delete_poll,
    methods=['DELETE']
)