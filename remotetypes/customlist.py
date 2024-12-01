from typing import Optional  # noqa: D100

class StringList(set):  # noqa: D101

    def __init__(
        self,
        *args: tuple[object],
        force_upper_case: Optional[bool] = False,
        **kwargs: dict[str, object],
    ) -> None:

        self.upper_case = force_upper_case
        super().__init__(*args, **kwargs)

        for item in self:
            if not isinstance(item, str):
                raise ValueError(f"All elements must be of type str, but got {type(item).__name__}")

    def append (self, item: str) -> None:  # noqa: D102
        if not isinstance(item, str):
            raise ValueError(item)

        if self.upper_case:
            item = item.upper()

        return super().add(item)

    def __contains__(self, o: object) -> bool:
        """Overwrite the `in` operator.

        x.__contains__(y) <==> y in x.
        """
        if not isinstance(o, str):
            o = str(o)

        if self.upper_case:
            o = o.upper()

        return super().__contains__(o)
