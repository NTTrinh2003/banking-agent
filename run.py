import os
import uvicorn
from dotenv import load_dotenv

def main():
    load_dotenv()

    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "8080"))

    reload = os.getenv("RELOAD", "false").lower() == "true"

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
    )

if __name__ == "__main__":
    main()  