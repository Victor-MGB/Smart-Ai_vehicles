from fastapi import FastAPI
from api.routes import predict, status, recommend

app = FastAPI(title="Smart Transport AI Backend")

app.include_router(predict.router, prefix="/predict-failure")
app.include_router(status.router, prefix="/get-component-status")
app.include_router(recommend.router, prefix="/recommend-maintenance")
