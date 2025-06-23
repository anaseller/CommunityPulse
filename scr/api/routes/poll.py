from flask import Blueprint

from src.api.controllers.poll import PollController


polls_blueprint = Blueprint(
    'polls',
    __name__,
    url_prefix="/api/v1/polls"
)

polls_blueprint.add_url_rule(
    '',
    view_func=PollController.get_polls,
    methods=['GET']
)

polls_blueprint.add_url_rule(
    '',
    view_func=PollController.create_poll,
    methods=['POST']
)

polls_blueprint.add_url_rule(
    '/<int:poll_id>',
    view_func=PollController.get_poll_by_id,
    methods=['GET']
)

polls_blueprint.add_url_rule(
    '/<int:poll_id>',
    view_func=PollController.update_poll,
    methods=['PUT']
)

polls_blueprint.add_url_rule(
    '/<int:poll_id>',
    view_func=PollController.delete_poll,
    methods=['DELETE']
)