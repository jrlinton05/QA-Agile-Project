from Source.Helpers.random_id_helper import generate_random_id
import uuid

def test_generate_random_id_returns_valid_uuid():
    random_id = generate_random_id()
    val = uuid.UUID(random_id)
    assert str(val) == random_id
