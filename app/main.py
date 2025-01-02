from fastapi import FastAPI
from app.routers.router import router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

# Initialize tags before creating FastAPI app
all_tags = settings.get_all_tags()
endpoint_tags = settings.get_endpoint_tags("main_api")
service_tags = settings.get_tags_by_name("service:")
main_api_tags = settings.endpoints["main_api"].tags

app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
    #openapi_tags=[{"name": tag.name, "description": tag.description} for tag in all_tags]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routes
app.include_router(router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)