from enum import Enum


class DType(Enum):
    STRING = "string"
    INT64 = "int64"
    FLOAT64 = "float64"
    BOOL = "boolean"
    DATE = "datetime64[ns]"
    OBJECT = "object"
