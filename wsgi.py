import os
from app import app

if __name__ == "__main__":
    port = int(os.environment.get("PORT,4000"))
    app.run(host="0.0.0.0", port=port)
    