from contextlib import ExitStack
from pathlib import Path
from typing import Any, TypedDict

import orjson
from flask import Flask, request
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from loguru import logger

from simbot_offline_inference.controller import SimBotInferenceController


class WrappedCDF(TypedDict):
    """Wrapped CDF.

    I'm not sure why this exists, but it does.
    """

    id: str
    text: str
    cdf: dict[str, Any]


class BackendController:
    """Controller for the backend of the web app."""

    def __init__(self, inference_controller: SimBotInferenceController, cdf_dir: Path) -> None:
        self._inference_controller = inference_controller

        self._cdf_dir = cdf_dir

        self._stack = ExitStack()

    def __enter__(self) -> None:
        """Initialise the server."""
        return self.start_server()  # type: ignore[return-value]

    def __exit__(self, *args: Any, **kwargs: Any) -> bool:
        """Close the server."""
        return self._stack.__exit__(*args, **kwargs)  # noqa: WPS609

    def start_server(self) -> ExitStack:
        """Initialise the server."""
        self._stack.enter_context(self._inference_controller)

        cdf_path = next(self._cdf_dir.iterdir())
        raw_cdf = orjson.loads(cdf_path.read_bytes())
        self._inference_controller.launch_game(raw_cdf)

        logger.info("Server initialisation complete.")
        return self._stack.__enter__()  # noqa: WPS609

    def load_cdfs(self) -> dict[str, list[WrappedCDF]]:
        """Load all the CDFs."""
        cdfs: list[WrappedCDF] = []

        for cdf_path in self._cdf_dir.iterdir():
            raw_cdf = orjson.loads(cdf_path.read_bytes())
            cdfs.append(
                {
                    "id": raw_cdf["scene"]["scene_id"],
                    "text": raw_cdf["scene"]["scene_id"],
                    "cdf": raw_cdf,
                }
            )

        logger.info(f"Loaded {len(cdfs)} CDFs.")
        return {"cdfs": cdfs}

    def ping(self) -> str:
        """Ping."""
        return "pong"

    def start_session(self) -> dict[str, str]:
        """Start a session."""
        return {"uid": "Robot", "text": "Hey, What's up?"}

    def start_game(self) -> str:
        """Start a new game."""
        request_data = request.json()  # type: ignore[misc]
        cdf_data = request_data["cdf_data"]
        self._inference_controller.launch_game(cdf_data)
        return "Ok"

    def process_utterance(self) -> dict[str, str]:
        """Process an utterance."""
        request_data = request.json()  # type: ignore[misc]
        utterance = request_data["utterance"]
        session_id = request_data["session_id"]
        response = self._inference_controller.handle_utterance(session_id, utterance)
        logger.debug(response)

        return {"uid": "Robot", "text": "Actions completed."}


class SimBotWebBackendApp:
    """Run the backend app."""

    def __init__(
        self, inference_controller: SimBotInferenceController, cdf_dir: Path, port: int = 11000
    ):
        self._flask_app = Flask(__name__)
        CORS(self._flask_app)
        self.controller = BackendController(inference_controller, cdf_dir)

        self.http_server = WSGIServer(("", port), self._flask_app)

    def configure(self) -> None:
        """Configure routing for the app."""
        self._flask_app.add_url_rule("/ping", "ping", self.controller.ping, methods=["GET"])
        self._flask_app.add_url_rule(
            "/begin_session", "begin_session", self.controller.start_session, methods=["POST"]
        )
        self._flask_app.add_url_rule(
            "/process_utterance",
            "process_utterance",
            self.controller.process_utterance,
            methods=["POST"],
        )
        self._flask_app.add_url_rule(
            "/get_cdfs", "get_cdfs", self.controller.load_cdfs, methods=["POST"]
        )
        self._flask_app.add_url_rule(
            "/start_game", "start_game", self.controller.start_game, methods=["POST"]
        )

    def get_flask_app(self) -> Flask:  # noqa: WPS615
        """Get the Flask app."""
        return self._flask_app

    def run(self) -> None:
        """Run the app."""
        self.configure()
        self.http_server.serve_forever()
