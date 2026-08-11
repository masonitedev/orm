from .TimeStampsScope import TimeStampsScope


class TimeStampsMixin:
    """Global scope class to add automatic timestamps to models."""

    def boot_TimeStampsMixin(self, builder):
        if not self.__timestamps__:
            return

        if not self.date_created_at and not self.date_updated_at:
            raise AttributeError(
                "Timestamps are enabled but not defined in the model. "
                "Please define at least one of the 'date_created_at' or 'date_updated_at' attributes. "
                "If you want to disable timestamps, set the '__timestamps__' attribute to False."
            )

        builder.set_global_scope(TimeStampsScope())

    def activate_timestamps(self, boolean=True):
        self.__timestamps__ = boolean
        return self
