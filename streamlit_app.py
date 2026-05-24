"""Entry point for Streamlit Community Cloud deployment."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# Run the frontend app directly
runfile = os.path.join(os.path.dirname(__file__), "frontend", "app.py")
with open(runfile, encoding="utf-8") as f:
    exec(compile(f.read(), runfile, "exec"), {"__name__": "__main__"})
