from general.FastAPI import app
from Routing.Router import RegisterRoutingFastAPI
import uvicorn


if __name__ == "__main__":    
    import uvicorn
    RegisterRoutingFastAPI()
    uvicorn.run(app=app, host="127.0.0.1", port=8000)