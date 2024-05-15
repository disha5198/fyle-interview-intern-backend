from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

principal_resources = Blueprint('principal_resources', __name__)

@principal_resources.route('/assignments', methods=['GET'])
@decorators.authenticate_principal
def list_assignments(p):
    """List all submitted and graded assignments"""
    # Add logic to fetch assignments and return them
    return APIResponse.respond(data=assignments_data)

@principal_resources.route('/teachers', methods=['GET'])
@decorators.authenticate_principal
def list_teachers(p):
    """List all the teachers"""
    # Add logic to fetch teachers and return them
    return APIResponse.respond(data=teachers_data)

@principal_resources.route('/assignments/grade', methods=['POST'])
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    # Add logic to grade or re-grade an assignment
    return APIResponse.respond(data=graded_assignment_data)
  
