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
    failure case: If an assignment is in Draft state, it cannot be graded by principal
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
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

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

