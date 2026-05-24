import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
exec(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "pages", "chat.py"), encoding="utf-8").read())
