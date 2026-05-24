"""
Start ngrok tunnels and print public URLs.
Run: python tunnel.py
"""
import time
from pyngrok import ngrok, conf

# Kill any stale tunnels
ngrok.kill()

# Create tunnels
frontend_tunnel = ngrok.connect(8501, "http")
backend_tunnel = ngrok.connect(8000, "http")

frontend_url = frontend_tunnel.public_url
backend_url = backend_tunnel.public_url

print()
print("=" * 50)
print("   PUBLIC URLS (share these!)")
print("=" * 50)
print(f"   Frontend:  {frontend_url}")
print(f"   Backend:   {backend_url}")
print("=" * 50)
print()
print(f"Update frontend/api.py API_URL to: {backend_url}")
print()
print("Press Ctrl+C to stop.")
print()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down...")
    ngrok.kill()
