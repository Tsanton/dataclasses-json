from dataclasses import field, dataclass
from typing import List

from dataclasses_json import config, dataclass_json
from .test_letter_case import FieldNamePerson

expected_ignore_json='{"given_name": "Alice"}'
expected_json='{"givenName": "Alice"}'
expected_ignore_dict={"given_name": "Alice"}
expected_dict={"givenName": "Alice"}



@dataclass_json()
@dataclass
class Child:
    child_id:int = field(metadata=config(field_name="id"))
    child_name:str = field(metadata=config(field_name="name"))

@dataclass_json()
@dataclass
class ParentWithChildren:
    parent_id:int = field(metadata=config(field_name="id"))
    parent_name:str = field(metadata=config(field_name="name"))
    children:List[Child] = field(metadata=config(field_name="children"))

@dataclass_json()
@dataclass
class ParentWithChild:
    parent_id:int = field(metadata=config(field_name="id"))
    parent_name:str = field(metadata=config(field_name="name"))
    child:Child = field(metadata=config(field_name="child"))



class TestSerializationIgnore:

    def test_to_json_ignore_custom_naming(self):
        assert expected_ignore_json == FieldNamePerson("Alice").to_json(ignore_custom_naming=True)

    def test_to_json_include_custom_naming(self):
        assert expected_json == FieldNamePerson("Alice").to_json(ignore_custom_naming=False)

    def test_to_json_ignore_custom_naming_option(self):
        assert expected_json == FieldNamePerson("Alice").to_json()

    def test_to_dict_ignore_custom_naming(self):
        assert expected_ignore_dict == FieldNamePerson("Alice").to_dict(ignore_custom_naming=True)

    def test_to_dict_include_custom_naming(self):
        assert expected_dict == FieldNamePerson("Alice").to_dict(ignore_custom_naming=False)

    def test_to_dict_ignore_custom_naming_option(self):
        assert expected_dict == FieldNamePerson("Alice").to_dict()

    def test_dump_one_ignore_custom_naming(self):
        person = FieldNamePerson('Alice')
        dump = FieldNamePerson.schema(ignore_field_name_on_serialization=True).dump(person, many=False)
        assert expected_ignore_dict == dump

    def test_dump_one_include_custom_naming(self):
        person = FieldNamePerson('Alice')
        dump = FieldNamePerson.schema(ignore_field_name_on_serialization=False).dump(person, many=False)
        assert expected_dict == dump

    def test_dump_one_ignore_custom_naming_option(self):
        person = FieldNamePerson('Alice')
        dump = FieldNamePerson.schema().dump(person, many=False)
        assert expected_dict == dump

    def test_dumps_one_ignore_custom_naming(self):
        person = FieldNamePerson('Alice')
        dump = FieldNamePerson.schema(ignore_field_name_on_serialization=True).dumps(person, many=False)
        assert expected_ignore_json == dump

    def test_dumps_one_include_custom_naming(self):
        person = FieldNamePerson('Alice')
        dump = FieldNamePerson.schema(ignore_field_name_on_serialization=False).dumps(person, many=False)
        assert expected_json == dump

    def test_dumps_one_ignore_custom_naming_option(self):
        person = FieldNamePerson('Alice')
        dump = FieldNamePerson.schema().dumps(person, many=False)
        assert expected_json == dump

    def test_dump_many_ignore_custom_naming(self):
        p1 = FieldNamePerson('Alice')
        p2 = FieldNamePerson('Alex')
        dump = FieldNamePerson.schema(ignore_field_name_on_serialization=True).dump([p1,p2], many=True)
        p1_dict = p1.to_dict(ignore_custom_naming=True)
        p2_dict = p2.to_dict(ignore_custom_naming=True)
        assert len(dump) == 2
        assert p1_dict in dump
        assert p2_dict in dump

    def test_dump_many_include_custom_naming(self):
        p1 = FieldNamePerson('Alice')
        p2 = FieldNamePerson('Alex')
        dump = FieldNamePerson.schema(ignore_field_name_on_serialization=False).dump([p1,p2], many=True)
        p1_dict = p1.to_dict(ignore_custom_naming=False)
        p2_dict = p2.to_dict(ignore_custom_naming=False)
        assert len(dump) == 2
        assert p1_dict in dump
        assert p2_dict in dump

    def test_dump_many_ignore_custom_naming_option(self):
        p1 = FieldNamePerson('Alice')
        p2 = FieldNamePerson('Alex')
        dump = FieldNamePerson.schema().dump([p1,p2], many=True)
        p1_dict = p1.to_dict()
        p2_dict = p2.to_dict()
        assert len(dump) == 2
        assert p1_dict in dump
        assert p2_dict in dump

    def test_dumps_many_ignore_custom_naming(self):
        p1 = FieldNamePerson('Alice')
        p2 = FieldNamePerson('Alex')
        dump = FieldNamePerson.schema(ignore_field_name_on_serialization=True).dumps([p1,p2], many=True)
        p1_json = p1.to_json(ignore_custom_naming=True)
        p2_json = p2.to_json(ignore_custom_naming=True)
        assert p1_json in dump
        assert p2_json in dump

    def test_dumps_many_include_custom_naming(self):
        p1 = FieldNamePerson('Alice')
        p2 = FieldNamePerson('Alex')
        dump = FieldNamePerson.schema(ignore_field_name_on_serialization=False).dumps([p1,p2], many=True)
        p1_json = p1.to_json(ignore_custom_naming=False)
        p2_json = p2.to_json(ignore_custom_naming=False)
        assert p1_json in dump
        assert p2_json in dump

    def test_dumps_many_ignore_custom_naming_option(self):
        p1 = FieldNamePerson('Alice')
        p2 = FieldNamePerson('Alex')
        dump = FieldNamePerson.schema().dumps([p1,p2], many=True)
        p1_json = p1.to_json()
        p2_json = p2.to_json()
        assert p1_json in dump
        assert p2_json in dump


    def test_dump_with_nested_list_object(self):
        data = """[
        {
            "id": 1,
            "name": "Parent1",
            "children": [
                {
                    "id": 2,
                    "name": "child2"
                },
                {
                    "id": 3,
                    "name": "child3"
                }
            ]
        }]"""
        parent = ParentWithChildren.schema().loads(data, many=True)
        serialized_data = ParentWithChildren.schema(ignore_field_name_on_serialization=False).dump(parent,many=True)
        assert "id" in serialized_data[0]
        assert "name" in serialized_data[0]
        assert "name" in serialized_data[0]["children"][0]
        assert "name" in serialized_data[0]["children"][1]
        assert "id" in serialized_data[0]["children"][0]
        assert "id" in serialized_data[0]["children"][1]


    def test_dump_with_nested_list_object_ignore_custom_naming(self):
        data = """[
        {
            "id": 1,
            "name": "Parent1",
            "children": [
                {
                    "id": 2,
                    "name": "child2"
                },
                {
                    "id": 3,
                    "name": "child3"
                }
            ]
        }]"""
        parent = ParentWithChildren.schema().loads(data, many=True)
        serialized_data = ParentWithChildren.schema(ignore_field_name_on_serialization=True).dump(parent,many=True)
        assert "parent_id" in serialized_data[0]
        assert "parent_name" in serialized_data[0]
        assert "child_name" in serialized_data[0]["children"][0]
        assert "child_name" in serialized_data[0]["children"][1]
        assert "child_id" in serialized_data[0]["children"][0]
        assert "child_id" in serialized_data[0]["children"][1]




    def test_dump_with_nested_object(self):
        data = """[
        {
            "id": 1,
            "name": "Parent1",
            "child": {
                "id": 2,
                "name": "child2"
            }
        }]"""
        parent = ParentWithChild.schema().loads(data, many=True)
        serialized_data = ParentWithChild.schema(ignore_field_name_on_serialization=False).dump(parent,many=True)
        assert "id" in serialized_data[0]
        assert "name" in serialized_data[0]
        assert "name" in serialized_data[0]["child"]
        assert "id" in serialized_data[0]["child"]


    def test_dump_with_nested_list_object_ignore_custom_naming(self):
        data = """[
                {
                    "id": 1,
                    "name": "Parent1",
                    "child": {
                        "id": 2,
                        "name": "child2"
                    }
                }]"""
        parent = ParentWithChild.schema().loads(data, many=True)
        serialized_data = ParentWithChild.schema(ignore_field_name_on_serialization=True).dump(parent, many=True)
        print(serialized_data)
        assert "parent_id" in serialized_data[0]
        assert "parent_name" in serialized_data[0]
        assert "child_name" in serialized_data[0]["child"]
        assert "child_id" in serialized_data[0]["child"]