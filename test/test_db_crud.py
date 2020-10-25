import pytest
from sqlalchemy import Column, String

from fastapi_simple_login.db.mixin import Base
from fastapi_simple_login.db.mixin import CRUD


class SampleModel(Base, CRUD["TestModel"]):
    col1 = Column(String)


def test_create(session):
    col1_value = "col1_value"
    instance = SampleModel.create(col1=col1_value)

    assert isinstance(instance, SampleModel)
    assert instance.col1 == col1_value

    assert SampleModel.query.count() == 1
    found = SampleModel.query.first()

    assert found.col1 == col1_value
    SampleModel.query.delete()
    session.commit()


@pytest.mark.usefixtures("session")
def test_get():
    col1_value = "col1_value"
    instance = SampleModel.create(col1=col1_value)
    found = SampleModel.get(field="id", value=instance.id)

    assert SampleModel.query.count() == 1
    assert found.col1 == col1_value


@pytest.mark.usefixtures("session")
def test_update():
    new_value = "new_value"
    instance = SampleModel.create(col1="old_value")
    SampleModel.update(field="id", value=instance.id, col1=new_value)
    updated = SampleModel.get(field="id", value=instance.id)

    assert updated.col1 == new_value


@pytest.mark.usefixtures("session")
def test_delete():
    col1_value = "col1_value"
    instance = SampleModel.create(col1=col1_value)

    SampleModel.delete(field="id", value=instance.id)

    assert SampleModel.get(field="id", value=instance.id) is None
