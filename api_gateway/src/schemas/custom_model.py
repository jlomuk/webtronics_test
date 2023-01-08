from typing import TypeVar, Type, Any, Optional

import sqlalchemy
from pydantic import BaseModel

_Model = TypeVar('_Model', bound='BaseModel')


class CustomBaseModel(BaseModel):
    @classmethod
    def parse_obj(cls: Type[_Model], obj: Any) -> Optional[_Model] | list[_Model]:
        if isinstance(obj, list):
            return [cls.parse_obj(i) for i in obj]

        if not isinstance(obj, dict) and not isinstance(obj, sqlalchemy.engine.row.RowMapping):
            return super().parse_obj(obj)

        child_values = {}
        has_data = False
        obj = dict(obj)

        for member_name, field in cls.__fields__.items():
            if getattr(field.type_, 'parse_obj', None):
                child_values[member_name] = field.type_.parse_obj(obj)
            else:
                alias = field.alias or field.name
                has_data = has_data or obj.get(alias) is not None

        if not has_data:
            return None

        obj.update(child_values)
        return cls(**obj)  # type: ignore[call-arg]
