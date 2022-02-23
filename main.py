if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(".env")

    from bootstrap.database import ensure_all_entities

    ensure_all_entities()

    import uvicorn

    uvicorn.run(app="bootstrap.server:app", host="127.0.0.1", port=8000)
