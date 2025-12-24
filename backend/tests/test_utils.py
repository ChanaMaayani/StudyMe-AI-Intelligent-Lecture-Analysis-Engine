def calculate_score(correct, total):
    if total == 0:
        return 0
    return round((correct / total) * 100)


def test_calculate_score():
    assert calculate_score(3, 5) == 60
    assert calculate_score(0, 5) == 0
    assert calculate_score(5, 5) == 100
