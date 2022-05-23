from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config, dataclass_json, Undefined

@dataclass_json()
@dataclass
class AnnouncementSubType:
    filter_id:int = field(metadata=config(field_name="id"))
    filter_name:str = field(metadata=config(field_name="namn"))

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class AnnouncementType:
    announcement_type_id:int = field(metadata=config(field_name="id"))
    announcement_type_name:str = field(metadata=config(field_name="namn"))
    announcement_sub_types:List[AnnouncementSubType] = field(metadata=config(field_name="underrubriker"))


if __name__ == "__main__":
    data = """[
            {
                "id": 58,
                "namn": "EGTS",
                "lanRegel": "obligatorisk",
                "underrubriker": [
                    {
                        "id": 53,
                        "namn": "Nyregistreringar"
                    },
                    {
                        "id": 54,
                        "namn": "Ändringar"
                    }
                ]
            }]"""

    ### Act ###
    announcement_type = AnnouncementType.schema().loads(data, many=True)
    serialized_data = AnnouncementType.schema(ignore_field_name_on_serialization=True).dumps(announcement_type, many=True)
    print(serialized_data)