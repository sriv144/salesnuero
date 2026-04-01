import sys
import importlib

packages = [
    "fastapi",
    "crewai",
    "chromadb",
    "langchain",
    "langchain_anthropic",
]

def test_imports():
    success = True
    print(f"Testing environment with Python {sys.version.split()[0]}...\n")
    for pkg in packages:
        try:
            importlib.import_module(pkg)
            print(f"✅ Successfully imported {pkg}")
        except ImportError as e:
            print(f"❌ Failed to import {pkg}: {e}")
            success = False
            
    if success:
        print("\nAll dependencies imported successfully!")
    else:
        print("\nThere were import errors.")
        sys.exit(1)

if __name__ == "__main__":
    test_imports()
