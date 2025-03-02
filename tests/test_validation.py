import pytest

from domain import custom_errors
from auth.validation_and_pass_hashing.validation import validate_data, CreateUser, Login


@pytest.mark.parametrize(
    "input_data, validation_model",
    (
            ({"name": "test_name", "email": "test@email.com", "password": "test_pass"}, CreateUser),
    )
)
def test_validate_data_if_correct_data_is_provided(input_data, validation_model):
    result = validate_data(validation_model=validation_model, data=input_data)
    assert result == input_data


@pytest.mark.parametrize(
    "input_data, missed_field, validation_model",
    (
            ({"email": "test@email.com", "password": "test_password"}, "name", CreateUser),
            ({"name": "test_name", "password": "test_password"}, "email", CreateUser),
            ({"name": "test_name", "email": "test@email.com"}, "password", CreateUser),
    )
)
def test_validate_data_if_incomplete_data_is_provided(input_data, missed_field, validation_model):
    with pytest.raises(custom_errors.ValidationError) as e:
        validate_data(validation_model=validation_model, data=input_data)
    assert e.value.message[0]["input"] == input_data
    assert e.value.message[0]["loc"][0] == missed_field
    assert e.value.message[0]["msg"] == "Field required"
    assert e.value.message[0]["type"] == "missing"
    assert e.value.message[0]["url"] == "https://errors.pydantic.dev/2.10/v/missing"


@pytest.mark.parametrize(
    "input_data, incorrect_field, validation_model",
    (
            ({"incorrect_field": "value", "email": "test@email.com", "password": "test_password"}, "name", CreateUser),
            ({"name": "test_name", "password": "test_password"}, "email", CreateUser),
            ({"name": "test_name", "email": "test@email.com"}, "password", CreateUser),
            ({"email": "test_2@email.com", "password": True}, "password", Login),
    )
)
def test_validate_data_if_incorrect_data_is_provided(input_data, incorrect_field, validation_model):
    with pytest.raises(custom_errors.ValidationError) as e:
        validate_data(validation_model=validation_model, data=input_data)
    assert e.value.message[0]["input"] in (input_data, input_data.get(incorrect_field))
    assert e.value.message[0]["loc"][0] == incorrect_field
    assert e.value.message[0]["msg"] in (
        "Field required",
        "Input should be a valid string",
        "Input should be 'column_value' or 'search_text'",
        "Input should be 'id', 'title', 'description', 'creation_date' or 'user_id'",
        "Input should be 'id', 'name', 'email' or 'creation_date'"
    )
    assert e.value.message[0]["type"] in ("missing", "string_type", "enum")
    assert e.value.message[0]["url"] in ("https://errors.pydantic.dev/2.10/v/missing",
                                         "https://errors.pydantic.dev/2.10/v/string_type",
                                         "https://errors.pydantic.dev/2.10/v/enum")
