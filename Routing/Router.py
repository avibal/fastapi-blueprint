from general.FastAPI import app
from general.FastAPI import appDepends
from general.FastAPI import appHTTPException
from fastapi import Response
import logiclayer.math as math
import logiclayer.auth as auth


def RegisterRoutingFastAPI(): 

    @app.post("/token")
    async def login_for_access_token(TokenData:auth.TokenData = appDepends()):
        user = auth.authenticate_user(auth.fake_users_db, TokenData.username, TokenData.password)        
        if not user:
            raise appHTTPException(
                status_code=appHTTPException.status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
        )
        access_token_expires = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Response(
            headers={"Authorization": f"Bearer {access_token}"},
            status_code=200,
        )
    
    @app.get("/GetMathData")
    #async def get_recipes(RecipesTitle: str = None,  credentials:auth.HTTPAuthorizationCredentials = appDepends(auth.oauth2_scheme)):
        # Extract the token from the credentials object
    #    token = credentials.credentials
    #    payload = auth.Validate_jwt_token(token)  # Decode the token
    async def GetMathData(RecipesTitle: str = None):    
        return math.GetMathData(RecipesTitle)       

    @app.get("/CreateMathData")    
    #async def CreateMathData(credentials:auth.HTTPAuthorizationCredentials = appDepends(auth.oauth2_scheme)):
    #    # Extract the token from the credentials object
    #    token = credentials.credentials
    #    payload = auth.Validate_jwt_token(token)  # Decode the token
    async def CreateMathData():        
        return math.CreateMathData()    



    @app.get("/")
    async def root():
        return {"message": "Welcome to my FastAPI app!"}

 