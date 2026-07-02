from fastapi import FastAPI
import asyncio
import uvicorn


app = FastAPI(description="Data from parser")


app.get('/items')








if __name__ == "__main__":
    uvicorn.run('api:parsed', host='127.0.0.1', port=8081)