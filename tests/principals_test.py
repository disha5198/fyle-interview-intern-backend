from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    Failure case: If an assignment is in Draft state, it cannot be graded by the principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    """
    Test grading functionality for a submitted assignment
    """
    # Create and submit an assignment first
    response = client.post(
        '/student/assignments',
        headers=h_principal,
        json={
            'content': 'Test assignment content'
        }
    )
    assert response.status_code == 200
    assignment_id = response.json['data']['id']

    # Submit the assignment
    response = client.post(
        '/student/assignments/submit',
        headers=h_principal,
        json={
            'id': assignment_id,
            'teacher_id': 1
        }
    )
    assert response.status_code == 200

    # Now grade the submitted assignment
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment_id,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.A


def test_regrade_assignment(client, h_principal):
    """
    Test regrading functionality for a graded assignment
    """
    # Create and submit an assignment first
    response = client.post(
        '/student/assignments',
        headers=h_principal,
        json={
            'content': 'Test assignment content'
        }
    )
    assert response.status_code == 200
    assignment_id = response.json['data']['id']

    # Submit the assignment
    response = client.post(
        '/student/assignments/submit',
        headers=h_principal,
        json={
            'id': assignment_id,
            'teacher_id': 1
        }
    )
    assert response.status_code == 200

    # Grade the submitted assignment
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment_id,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    # Now regrade the assignment
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': assignment_id,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.A

def test_grade_assignment_success(client, h_principal):
    # Assign a grade to a submitted assignment
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,  # Assuming assignment ID 1 exists and is in a submitted state
            'grade': 'A'  # Assigning grade A
        },
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    assert data['state'] == 'GRADED'
    assert data['grade'] == 'A'


def test_grade_assignment_invalid_assignment_id(client, h_principal):
    # Attempt to grade an assignment with an invalid ID
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 9999,  # Assuming assignment ID 9999 does not exist
            'grade': 'A'
        },
        headers=h_principal
    )

    assert response.status_code == 404


def test_grade_assignment_invalid_grade(client, h_principal):
    # Attempt to assign an invalid grade to an assignment
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,  # Assuming assignment ID 1 exists
            'grade': 'Z'  # Assuming 'Z' is not a valid grade
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment_draft_assignment(client, h_principal):
    # Attempt to grade an assignment that is still in draft state
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 2,  # Assuming assignment ID 2 is in draft state
            'grade': 'A'
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment_unauthorized(client):
    # Attempt to grade an assignment without authentication
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,  # Assuming assignment ID 1 exists
            'grade': 'A'
        }
    )

    assert response.status_code == 401


