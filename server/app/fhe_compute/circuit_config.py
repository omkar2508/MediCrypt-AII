from dataclasses import dataclass


@dataclass(frozen=True)
class CircuitConfig:
    bit_width: int = 8
    precision: int = 4
    param_set: str = "concrete-demo"
