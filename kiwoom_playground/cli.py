import sys


def run_playground():
    try:
        import uvicorn
    except ImportError:
        print("❌ Error: Web dependencies are not installed.")
        print("👉 Please install them using: pip install 'kiwoom-rest[playground]'")
        sys.exit(1)

    print("🚀 Starting Kiwoom API Playground...")
    uvicorn.run("kiwoom_playground.server:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run_playground()
