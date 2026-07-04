from app.fhe_compute.benchmarking import measure_operation
from app.fhe_compute.primitives.encrypted_add import encrypted_add


if __name__ == "__main__":
    with measure_operation() as stats:
        encrypted_add(b"left", b"right")
    print(stats["elapsed_seconds"])
