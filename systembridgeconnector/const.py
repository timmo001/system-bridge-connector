"""Constants."""

from enum import StrEnum


class QueryParameter(StrEnum):
    """Query Parameter."""

    ALBUM = "album"
    API_PORT = "apiPort"
    ARTIST = "artist"
    AUTOPLAY = "autoplay"
    BASE = "base"
    FILENAME = "filename"
    PATH = "path"
    TITLE = "title"
    TOKEN = "token"
    URL = "url"
    VOLUME = "volume"


class EventKey(StrEnum):
    """Event Key."""

    APP_ICON = "app_icon"
    APP_NAME = "app_name"
    BASE = "base"
    DATA = "data"
    DIRECTORIES = "directories"
    EVENT = "event"
    FILE = "file"
    FILENAME = "filename"
    FILES = "files"
    ID = "id"
    KEY = "key"
    MESSAGE = "message"
    MODULE = "module"
    MODULES = "modules"
    PATH = "path"
    SETTING = "setting"
    SUBTYPE = "subtype"
    TEXT = "text"
    TIMEOUT = "timeout"
    TITLE = "title"
    TOKEN = "token"
    TYPE = "type"
    URL = "url"
    VALUE = "value"
    VERSION = "version"
    VERSIONS = "versions"


class EventType(StrEnum):
    """Event Type."""

    APPLICATION_UPDATE = "APPLICATION_UPDATE"
    APPLICATION_UPDATING = "APPLICATION_UPDATING"
    DATA_GET = "DATA_GET"
    DATA_LISTENER_REGISTERED = "DATA_LISTENER_REGISTERED"
    DATA_LISTENER_UNREGISTERED = "DATA_LISTENER_UNREGISTERED"
    DATA_UPDATE = "DATA_UPDATE"
    DIRECTORIES = "DIRECTORIES"
    ERROR = "ERROR"
    EXIT_APPLICATION = "EXIT_APPLICATION"
    FILE = "FILE"
    FILES = "FILES"
    GET_DATA = "GET_DATA"
    GET_DIRECTORIES = "GET_DIRECTORIES"
    GET_FILE = "GET_FILE"
    GET_FILES = "GET_FILES"
    GET_SETTINGS = "GET_SETTINGS"
    KEYBOARD_KEY_PRESSED = "KEYBOARD_KEY_PRESSED"
    KEYBOARD_KEYPRESS = "KEYBOARD_KEYPRESS"
    KEYBOARD_TEXT = "KEYBOARD_TEXT"
    KEYBOARD_TEXT_SENT = "KEYBOARD_TEXT_SENT"
    MEDIA_CONTROL = "MEDIA_CONTROL"
    NOTIFICATION = "NOTIFICATION"
    NOTIFICATION_SENT = "NOTIFICATION_SENT"
    OPEN = "OPEN"
    OPENED = "OPENED"
    POWER_HIBERNATE = "POWER_HIBERNATE"
    POWER_HIBERNATING = "POWER_HIBERNATING"
    POWER_LOCK = "POWER_LOCK"
    POWER_LOCKING = "POWER_LOCKING"
    POWER_LOGGINGOUT = "POWER_LOGGINGOUT"
    POWER_LOGOUT = "POWER_LOGOUT"
    POWER_RESTART = "POWER_RESTART"
    POWER_RESTARTING = "POWER_RESTARTING"
    POWER_SHUTDOWN = "POWER_SHUTDOWN"
    POWER_SHUTTINGDOWN = "POWER_SHUTTINGDOWN"
    POWER_SLEEP = "POWER_SLEEP"
    POWER_SLEEPING = "POWER_SLEEPING"
    REGISTER_DATA_LISTENER = "REGISTER_DATA_LISTENER"
    SETTINGS_UPDATED = "SETTINGS_UPDATED"
    SETTINGS_RESULT = "SETTINGS_RESULT"
    UNREGISTER_DATA_LISTENER = "UNREGISTER_DATA_LISTENER"
    UPDATE_SETTINGS = "UPDATE_SETTINGS"


class EventSubType(StrEnum):
    """Event SubType."""

    BAD_TOKEN = "BAD_TOKEN"
    BAD_DIRECTORY = "BAD_DIRECTORY"
    BAD_FILE = "BAD_FILE"
    BAD_JSON = "BAD_JSON"
    BAD_KEY = "MISSING_KEY"
    BAD_PATH = "BAD_PATH"
    BAD_REQUEST = "BAD_REQUEST"
    INVALID_ACTION = "INVALID_ACTION"
    LISTENER_ALREADY_REGISTERED = "LISTENER_ALREADY_REGISTERED"
    LISTENER_NOT_REGISTERED = "LISTENER_NOT_REGISTERED"
    MISSING_ACTION = "MISSING_ACTION"
    MISSING_TOKEN = "MISSING_TOKEN"
    MISSING_BASE = "MISSING_BASE"
    MISSING_KEY = "MISSING_KEY"
    MISSING_MODULES = "MISSING_MODULES"
    MISSING_PATH = "MISSING_PATH"
    MISSING_PATH_URL = "MISSING_PATH_URL"
    MISSING_SETTING = "MISSING_SETTING"
    MISSING_TEXT = "MISSING_TEXT"
    MISSING_TITLE = "MISSING_TITLE"
    MISSING_VALUE = "MISSING_VALUE"
    UNKNOWN_EVENT = "UNKNOWN_EVENT"
