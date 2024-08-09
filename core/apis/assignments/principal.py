from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

# List all submitted and graded assignments
@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    principal_assignments = Assignment.get_assignments_by_principal()
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)

@principal_assignments_resources.route('/assignments', methods=['DELETE'], strict_slashes=False)
@decorators.authenticate_principal
def delete_all_assignments(p):
    """Delete all assignments ever created"""
    try:
        # Query to delete all assignments in the database
        deleted_assignments = Assignment.query.delete()
        
        # Commit the changes to the database
        db.session.commit()

        if deleted_assignments == 0:
            return APIResponse.respond(data={'message': 'No assignments found in the system'})

        return APIResponse.respond(data={'message': f'{deleted_assignments} assignments have been deleted'})
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of an error
        return APIResponse.respond(data={'error': 'Failed to delete assignments', 'details': str(e)})

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    graded_assignment = Assignment.mark_grade_by_principal(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p,
       
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)