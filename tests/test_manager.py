from auth.service_layer import manager

def test_create_user(
        fake_validate_func, fake_hash_pass_func, fake_users_repo, fake_advs_repo, fake_unit_of_work, test_date
):
    user_data = {
        "name": "test_name", "email": "test@email.test", "password": "test_password", "creation_date": test_date
    }
    fuow = fake_unit_of_work(users=fake_users_repo([]), advs=fake_advs_repo([]))
    result = manager.create_user(
        user_data=user_data, validate_func=fake_validate_func, hash_pass_func=fake_hash_pass_func,
        uow=fuow
    )
    data_from_repo = fuow.users.instances.pop()
    assert type(result) is int
    assert 0 <= result <= 9
    assert result == data_from_repo.id
    assert data_from_repo.name == user_data["name"]
    assert data_from_repo.email == user_data["email"]
    assert data_from_repo.password == user_data["password"]
    assert data_from_repo.creation_date == user_data["creation_date"]
