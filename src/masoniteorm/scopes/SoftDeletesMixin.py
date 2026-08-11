from typing import TYPE_CHECKING

from .SoftDeleteScope import SoftDeleteScope

if TYPE_CHECKING:
    from ..query import QueryBuilder


class SoftDeletesMixin:
    """Global scope class to add soft deleting to models."""

    __deleted_at__ = "deleted_at"

    def boot_SoftDeletesMixin(self, builder):
        builder.set_global_scope(SoftDeleteScope(self.__deleted_at__))

    if TYPE_CHECKING:

        @classmethod
        def with_trashed(cls) -> QueryBuilder:
            """Include records flagged as deleted"""
            ...

        @classmethod
        def only_trashed(cls) -> QueryBuilder:
            """Filter for records marked as deleted"""
            ...

        @classmethod
        def force_delete(cls) -> QueryBuilder:
            """Remove the record from the table"""
            ...

        @classmethod
        def restore(cls) -> QueryBuilder:
            """Mark the record as not deleted"""
            ...

    def get_deleted_at_column(self):
        return self.__deleted_at__
