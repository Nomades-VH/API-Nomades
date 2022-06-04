if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(".env")

    # TODO: Algumas urls ainda permitem acesso sem o token de acesso

    from bootstrap.database import ensure_all_entities

    ensure_all_entities()

    import uvicorn
    print("Funcionou?")
    uvicorn.run(app="bootstrap.server:app", host="", port=8000)
