"""Custom Type for Autonomous System Number."""

# Standard Library
from typing import Any, Callable, Generator


class Asn(int):
    """Custom ASN Type."""

    is_private: bool
    is_4byte: bool
    size: int

    @staticmethod
    def _validate_private(asn: int) -> bool:
        is_private = False
        if asn in range(64512, 65535) or asn in range(4200000000, 4294967296):
            is_private = True
        return is_private

    @staticmethod
    def _validate_size(asn: int) -> int:
        size = 16
        if asn in range(65536, 4294967296):
            size = 32
        return size

    def __init__(self, asn: int) -> None:
        """Set attributes."""
        self.is_private = self._validate_private(asn)
        self.size = self._validate_size(asn)
        self.is_4byte = self.size == 32

    def prefixed(self) -> str:
        """Stringify ASN with AS prefix."""
        return f"AS{self}"

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        """Get Pydantic validators."""
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> int:
        """Validate ASN."""
        if not isinstance(v, int):
            raise TypeError("integer required")

        if v not in range(1, 4294967295):
            raise ValueError("Public ASNs must be a number between 1-4294967295.")

        return cls(v)

    def __str__(self) -> str:
        """Stringify ASN."""
        return str(super().__repr__())

    def __repr__(self) -> str:
        """Represent class with attributes."""
        parts = (
            super().__repr__(),
            f"is_private={self.is_private}",
            f"is_4byte={self.is_4byte}",
            f"size={self.size}",
        )
        return f"ASN({', '.join(parts)})"
