from starlette.responses import RedirectResponse
from fastapi import FastAPI

from app.routers import identity, wallet, template, credential, trust_registry

app = FastAPI(
    title="Snapbrillia",
    description="Wallet API",
    version="0.0.1",
)

# Include routers
routers = [wallet.router, credential.router, identity.router, template.router, trust_registry.router]
for router in routers:
    app.include_router(router)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=5040, reload=True, access_log=True)
