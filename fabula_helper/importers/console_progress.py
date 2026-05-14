import sys


class ConsoleProgress:
    def __init__(
        self,
        total: int,
        label: str,
        width: int = 30,
    ) -> None:
        self._total = total
        self._label = label
        self._width = width
        self._current = 0

    def update(self, current: int) -> None:
        self._current = current

        if self._total <= 0:
            return

        filled = int(self._width * self._current / self._total)
        empty = self._width - filled

        bar = "█" * filled + "░" * empty

        sys.stdout.write(
            f"\r[{bar}] {self._current}/{self._total} {self._label}"
        )
        sys.stdout.flush()

    def finish(self) -> None:
        if self._total > 0:
            self.update(self._total)
            sys.stdout.write("\n")
            sys.stdout.flush()