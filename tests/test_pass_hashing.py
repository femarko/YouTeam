from auth.validation_and_pass_hashing import pass_hashing


def test_hash_password():
    password = "test_password"
    hashed_password = pass_hashing.hash_password(password=password)
    assert pass_hashing.check_password(hashed_password=hashed_password, password=password)
    assert not pass_hashing.check_password(hashed_password=hashed_password, password="test_password_2")

