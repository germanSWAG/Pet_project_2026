from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from app.services.router import router as router_service
import logging 
import traceback
import time

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s "
                    "[%(levelname)s] %(message)s", 
                    handlers=[logging.StreamHandler(),
                    logging.FileHandler("server_errors.log", encoding="utf-8")])


logger = logging.getLogger("api_logger")

app = FastAPI()


@app.middleware("http")
async def cathc_exceptions_middleware(request : Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        process_time = (time.time() - start_time) * 1000
    
        error_tracebak = traceback.format_exc()
        logger.error(  
        f"Краш сервера 500! URL {request.url.path} | Метод: {request.method} \n" 
        f"время обработки {process_time:.2f} \n"
        f"Текст ошибки: {str(e)} \n"
        f" Трейсбек ошибки {error_tracebak}")

        return JSONResponse(status_code=500, 
                            content={"detail": "Внутрення ошибка сервера"})
        

app.include_router(router=router_service)




if __name__ == "__main__":

    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)