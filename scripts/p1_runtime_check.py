"""Print P1 optional ML runtime availability and device selection."""
from backend.core.ml_runtime import runtime_status, select_device

if __name__ == "__main__":
    print("SCI-DOC AI P1 runtime")
    print(f"device: {select_device()}")
    for package, available in runtime_status().items():
        print(f"{package}: {'available' if available else 'missing'}")