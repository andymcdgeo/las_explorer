from streamlit.report_thread import get_report_ctx
from streamlit.hashing import _CodeHasher
from streamlit.server.server import Server
from prometheus_client.registry import REGISTRY
from prometheus_client import Counter


class _SessionState:
    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(
                self._state["data"], None
            ):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session

def get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)
    return session._custom_session_state


def _get_names(collector_name, collector_type):
        result = []
        type_suffixes = {
            'counter': ['_total', '_created'],
            'summary': ['_sum', '_count', '_created'],
            'histogram': ['_bucket', '_sum', '_count', '_created'],
            'gaugehistogram': ['_bucket', '_gsum', '_gcount'],
            'info': ['_info'],
        }
        for suffix in type_suffixes.get(collector_type, []):
            result.append(collector_name + suffix)
        return result


def get_or_create_metric(metric_type, *, name, **kwargs):
    names =  _get_names(name, metric_type.__name__.lower())
    if any(name in REGISTRY._names_to_collectors for name in names):
        return REGISTRY._names_to_collectors[names[0]]
    else:
        return metric_type(name=name, **kwargs)



def provide_state(func):
    def wrapper(*args, **kwargs):
        state = get_state(hash_funcs={})
        count_sessions()
        return_value = func(state=state, *args, **kwargs)
        state.sync()
        return return_value

    return wrapper

def count_sessions():
    state = get_state(hash_funcs={})
    session_counter = get_or_create_metric(Counter, name='session_count', documentation='Unique Sessions')

    if not state._is_session_reused:
        session_counter.inc()
        state._is_session_reused = True