class ImmutableMeta(type):
    """
    Class used for non-pydantic objects that should not be modifiable at runtime.
    """
    def __setattr__(cls, key, value):
        raise AttributeError(f"Cannot modify immutable class '{cls.__name__}'")