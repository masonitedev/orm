from ..expressions.expressions import UpdateQueryExpression
from .BaseScope import BaseScope


class TimeStampsScope(BaseScope):
    """Global scope class to add automatic timestamps to a builder query."""

    def on_boot(self, builder):
        if not builder._model.__timestamps__:
            return

        created_column = builder._model.date_created_at
        updated_column = builder._model.date_updated_at
        if created_column or updated_column:
            builder.set_global_scope(
                "_timestamps", self.set_timestamp_create, action="insert"
            )

        if updated_column:
            builder.set_global_scope(
                "_timestamp_update", self.set_timestamp_update, action="update"
            )

    def on_remove(self, builder):
        pass

    def set_timestamp(owner_cls, query):
        if owner_cls.date_updated_at:
            column = owner_cls.date_updated_at
            setattr(owner_cls, column, "now")

    def set_timestamp_create(self, builder):
        if not builder._model.__timestamps__:
            return

        columns = {}
        created_column = builder._model.date_created_at
        if created_column:
            columns[created_column] = (
                builder._model.get_new_date().to_datetime_string()
            )

        updated_column = builder._model.date_updated_at
        if updated_column:
            columns[updated_column] = (
                builder._model.get_new_date().to_datetime_string()
            )

        builder._creates.update(columns)

    def set_timestamp_update(self, builder):
        if not builder._model.__timestamps__:
            return

        updated_column = builder._model.date_updated_at
        if not updated_column:
            return

        for update in builder._updates:
            if updated_column in update.column:
                return

        builder._updates += (
            UpdateQueryExpression(
                {
                    updated_column: builder._model.get_new_date().to_datetime_string()
                }
            ),
        )
