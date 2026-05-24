"""
One-click public deployment via ngrok.

First time setup:
  1. Sign up (free): https://dashboard.ngrok.com/signup
  2. Copy your authtoken: https://dashboard.ngrok.com/get-started/your-authtoken
  3. Run: $env:NGROK_AUTHTOKEN="your-token"; python launch_public.py

Usage:
  python launch_public.py

Prerequisites:
  - Backend running on port 8000
  - pyngrok installed (pip install pyngrok)
  - NGROK_AUTHTOKEN environment variable set
"""
import os, sys, time, subprocess
from pyngrok import ngrok, conf

auth_token = os.getenv("NGROK_AUTHTOKEN", "")
if not auth_token:
    print("ERROR: NGROK_AUTHTOKEN not set.")
    print()
    print("First time setup:")
    print("  1. Sign up (free): https://dashboard.ngrok.com/signup")
    print("  2. Get your token: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("  3. Set: $env:NGROK_AUTHTOKEN='your-token-here'")
    print("  4. Run again: python launch_public.py")
    sys.exit(1)

conf.get_default().auth_token = auth_token

# Kill any existing tunnels
ngrok.kill()

# Create tunnels
print("Creating ngrok tunnels...")
fe_tunnel = ngrok.connect(8501, "http")
be_tunnel = ngrok.connect(8000, "http")

fe_url = fe_tunnel.public_url
be_url = be_tunnel.public_url

print()
print("=" * 55)
print("  PUBLIC URLS - share these with anyone!")
print(f"  Frontend: {fe_url}")
print(f"  Backend:  {be_url}")
print("=" * 55)
print()

# Kill old streamlit, restart with ngrok backend URL
subprocess.run("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq *streamlit*\"",
               shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)

env = os.environ.copy()
env["API_URL"] = be_url

print("Starting Streamlit...")
proc = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "frontend/app.py",
     "--server.port", "8501", "--server.headless", "true",
     "--browser.gatherUsageStats", "false", "--server.address", "0.0.0.0"],
    env=env,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

time.sleep(4)
print(f"Streamlit running (PID {proc.pid})")
print(f"Open {fe_url} on any device!")
print()
print("Press Ctrl+C to stop.")
print()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down...")
    ngrok.kill()
    proc.terminate()
    print("Done.")
