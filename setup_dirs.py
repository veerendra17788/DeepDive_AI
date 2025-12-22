
import os

dirs = [
    "templates/auth",
    "templates/components",
    "templates/layouts",
    "static/css",
    "static/js",
    "static/img"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"Created: {d}")
