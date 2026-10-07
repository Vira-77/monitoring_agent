"""Module providing main entrypoint."""
import os
import click
import uvicorn
from pathlib import Path
from core.config import get_config

# Setup cli parameter for main command (main.py --debug --env local)
@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "prod"], case_sensitive=False),
    default="prod",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)
def main(env: str, debug: bool) -> None:
    """
    Start main function.

    Args:
        env (str): The environment name.
        debug (bool): Debug mode flag.
    """
    # Inject click option in envionment variable for config
    os.environ["AGENT_ENV"] = env
    os.environ["AGENT_DEBUG"] = str(debug)

    config = get_config()
    # Start Webserver
    uvicorn.run(
        app="server:app",
        host=config.app_host,
        port=config.app_port,
        reload=config.env == "local",
        workers=1,
        log_config=str(Path(__file__).absolute().parent.parent / "log.ini"),
        log_level="info"
    )


# Main entrypoint, click will mutate main() with cli options
if __name__ == "__main__":
    main()