import uvicorn

from webapp.server import container


if __name__ == "__main__":
    webapp_config = container.config.webapp

    uvicorn.run(
        "webapp.server:app",
        host=webapp_config.hostname(),
        port=webapp_config.port(),
        log_level=webapp_config.log_level(),
        reload=webapp_config.debug(),
    )
