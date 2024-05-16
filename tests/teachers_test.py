def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'

def test_grade_assignment_valid(client, h_teacher_1):
    """
    Test grading a valid assignment.
    """
    # Create a new assignment to be graded
    response = client.post(
        '/student/assignments',
        headers=h_teacher_1,
        json={
            'content': 'Test assignment content',
            'teacher_id': 1,
            'state': 'SUBMITTED'  # Assuming the assignment is already submitted
        })

    assert response.status_code == 200
    assignment_id = response.json['data']['id']

    # Grade the assignment
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            'id': assignment_id,
            'grade': 'A'
        })

    assert response.status_code == 200

    # Check if the assignment is graded and has the correct grade
    response = client.get(
        f'/student/assignments/{assignment_id}',
        headers=h_teacher_1
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == 'GRADED'
    assert response.json['data']['grade'] == 'A'


def test_grade_assignment_invalid_assignment_id(client, h_teacher_1):
    """
    Test grading an assignment with an invalid assignment ID.
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            'id': 9999,  # Assuming an invalid assignment ID
            'grade': 'A'
        })

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_invalid_grade(client, h_teacher_1):
    """
    Test grading an assignment with an invalid grade.
    """
    # Create a new assignment to be graded
    response = client.post(
        '/student/assignments',
        headers=h_teacher_1,
        json={
            'content': 'Test assignment content',
            'teacher_id': 1,
            'state': 'SUBMITTED'  # Assuming the assignment is already submitted
        })

    assert response.status_code == 200
    assignment_id = response.json['data']['id']

    # Grade the assignment with an invalid grade
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            'id': assignment_id,
            'grade': 'Z'  # Assuming 'Z' is an invalid grade
        })

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'

