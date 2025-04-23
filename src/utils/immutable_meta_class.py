class ImmutableMeta(type):
    """
    Meta class used for non-pydantic objects that should not be modifiable at runtime.
    
    Methods:
        __setattr__(cls, key, value): Raises an AttributeError since attributes of this class cannot be modified.
    """
    def __setattr__(cls, key, value):
        raise AttributeError(f"Cannot modify immutable class '{cls.__name__}'")