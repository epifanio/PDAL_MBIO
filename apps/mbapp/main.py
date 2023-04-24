import fastapi
from starlette.middleware.cors import CORSMiddleware
from mbapi import mbio
import uvicorn
# from views import dashboard


app = fastapi.FastAPI(title="MB-System PDAL IO API",
                      description="Prototype API for reading MBES data with PDAL and MB-System",
                      version="0.0.1",
                      )

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_PROCESSING_SECOND = 600


def configure_routing():
    app.include_router(mbio.router)
    # app.include_router(dashboard.router)


def configure():
    configure_routing()


if __name__ == '__main__':
    configure()
    uvicorn.run(app, port=9000, host='10.0.0.100')
else:
    configure()
