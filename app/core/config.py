from typing import Dict, List
from pydantic_settings import BaseSettings
from pydantic import BaseModel

class Tag(BaseModel):
    name: str
    description: str = ""

class EndpointConfig(BaseModel):
    url: str
    description: str
    version: str
    tags: List[Tag]  # Changed from Dict to List[Tag]

class Settings(BaseSettings):
    app_name: str = "Shoonit bot server"
    version: str = "1.0.0"
    description: str = "This is a sample FastAPI application for Shoonit bot server."
    contact_name: str = "Avi Balali"
    contact_email: str = "avi.balali@gmail.com"
    
    environment: str = "development"
    
    # Changed tags to List[Tag] format
    tags: List[Tag] = [
        Tag(name="project:shoonit-bot", description="Project identifier"),
        Tag(name="environment:development", description="Environment type"),
        Tag(name="owner:avi.balali", description="Project owner"),
        Tag(name="service:bot-server", description="Service identifier")
    ]
    
    endpoints: Dict[str, EndpointConfig] = {
        "main_api": EndpointConfig(
            url="/api/v1",
            description="Main API endpoint",
            version="1.0.0",
            tags=[
                Tag(name="service:main-api", description="Main API service"),
                Tag(name="type:rest", description="REST API endpoint")
            ]
        ),
        "health_check": EndpointConfig(
            url="/health",
            description="Health check endpoint",
            version="1.0.0",
            tags=[
                Tag(name="Health", description="Health check service"),
                
            ]
        )
    }

    class Config:
        env_prefix = "SHOONIT_"
        case_sensitive = False

    def get_endpoint_config(self, endpoint_name: str) -> EndpointConfig:
        """Get configuration for a specific endpoint"""
        return self.endpoints.get(endpoint_name)

    def get_all_tags(self) -> List[Tag]:
        """Get all global tags"""
        return self.tags

    def get_endpoint_tags(self, endpoint_name: str) -> List[Tag]:
        """Get tags for a specific endpoint"""
        endpoint = self.get_endpoint_config(endpoint_name)
        if endpoint:
            # Combine global and endpoint tags
            return self.tags + endpoint.tags
        return []

    def get_tags_by_name(self, tag_name: str) -> List[Tag]:
        """Get tags that match a specific name"""
        return [tag for tag in self.tags if tag_name in tag.name]

# Initialize settings
settings = Settings()
