from .immutable_meta_class import ImmutableMeta

class GlobalConstants(metaclass=ImmutableMeta):
    MONGO_ID_FIELD_NAME = "_id"