import importlib
import sys
import types

# Integration tests using fake Streamlit module — I identified UI state bugs, agent built mock framework

class FakeExpander:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeColumn:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeStreamlit(types.ModuleType):
    def __init__(self, name="streamlit"):
        super().__init__(name)
        # session state must support both key containment checks and attribute access
        class SessionState(dict):
            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(name)

            def __setattr__(self, name, value):
                self[name] = value

            def __delattr__(self, name):
                del self[name]

        self.session_state = SessionState()
        self._button_map = {}
        self._text_inputs = {}
        self._selectbox_value = "Normal"
        self._checkbox_map = {}
        self.calls = []

    # basic UI functions used by app.py
    def set_page_config(self, **kwargs):
        self.calls.append(("set_page_config", kwargs))

    def title(self, *args, **kwargs):
        self.calls.append(("title", args, kwargs))

    def caption(self, *args, **kwargs):
        self.calls.append(("caption", args, kwargs))

    class Sidebar:
        def __init__(self, parent):
            self.parent = parent

        def header(self, *args, **kwargs):
            self.parent.calls.append(("sidebar.header", args, kwargs))

        def selectbox(self, label, options, index=0):
            # return configured selectbox value
            return self.parent._selectbox_value

        def caption(self, *args, **kwargs):
            self.parent.calls.append(("sidebar.caption", args, kwargs))

    @property
    def sidebar(self):
        return FakeStreamlit.Sidebar(self)

    def subheader(self, *args, **kwargs):
        self.calls.append(("subheader", args, kwargs))

    def info(self, *args, **kwargs):
        self.calls.append(("info", args, kwargs))

    def expander(self, *args, **kwargs):
        return FakeExpander()

    def write(self, *args, **kwargs):
        self.calls.append(("write", args, kwargs))

    def text_input(self, label, key=None):
        # try key first, then label
        if key and key in self._text_inputs:
            return self._text_inputs[key]
        return self._text_inputs.get(label, "")

    def columns(self, n):
        return (FakeColumn(),) * n

    def button(self, label):
        return self._button_map.get(label, False)

    def checkbox(self, label, value=True):
        return self._checkbox_map.get(label, value)

    def warning(self, *args, **kwargs):
        self.calls.append(("warning", args, kwargs))

    def success(self, *args, **kwargs):
        self.calls.append(("success", args, kwargs))

    def error(self, *args, **kwargs):
        self.calls.append(("error", args, kwargs))

    def balloons(self):
        self.calls.append(("balloons",))

    def rerun(self):
        self.calls.append(("rerun",))

    def stop(self):
        # emulate streamlit stopping the script by raising a custom exception
        raise SystemExit("st.stop called")

    def divider(self):
        self.calls.append(("divider",))


def import_app_with_fake(st_fake):
    # inject fake streamlit into sys.modules and import/ reload app
    sys.modules["streamlit"] = st_fake
    if "app" in sys.modules:
        del sys.modules["app"]
    return importlib.import_module("app")


def test_app_initial_state():
    st_fake = FakeStreamlit()
    # ensure buttons default to False
    st_fake._button_map = {"Submit Guess 🚀": False, "New Game 🔁": False}
    app = import_app_with_fake(st_fake)

    ss = st_fake.session_state
    assert "secret" in ss
    assert ss["attempts"] == 1
    assert ss["score"] == 100
    assert ss["status"] == "playing"
    assert ss["history"] == []


def test_app_new_game_resets():
    st_fake = FakeStreamlit()
    # simulate pressing New Game on import
    st_fake._button_map = {"Submit Guess 🚀": False, "New Game 🔁": True}
    # preset a previous status to ensure new_game path runs
    st_fake.session_state.update({"secret": 1, "attempts": 5, "score": 10, "status": "lost", "history": [1,2,3]})

    app = import_app_with_fake(st_fake)
    ss = st_fake.session_state

    # app's current behavior sets attempts to 0 when New Game pressed
    assert ss["attempts"] == 0
    assert ss["status"] == "playing"
    assert isinstance(ss["secret"], int)


def test_app_submit_guess_win_flow():
    st_fake = FakeStreamlit()
    # configure sidebar difficulty selection
    st_fake._selectbox_value = "Normal"
    # preset session state so app won't randomize secret
    st_fake.session_state.update({"secret": 50, "attempts": 1, "score": 100, "status": "playing", "history": []})
    # configure widgets: submit pressed, provide guess via key
    st_fake._button_map = {"Submit Guess 🚀": True, "New Game 🔁": False}
    st_fake._text_inputs = {"guess_input_Normal": "50"}

    app = import_app_with_fake(st_fake)
    ss = st_fake.session_state

    # After submitting the correct guess, attempts should increment, status set to won
    assert ss["attempts"] == 2
    assert ss["status"] == "won"
    assert ss["history"][-1] == 50
    assert ss["score"] == 100
