"""Fixture for notification."""
from systembridgeconnector.models.notification import Action, Audio, Notification

FIXTURE_NOTIFICATION = Notification(
    title="Title",
    message="Message",
    icon="https://www.example.com/icon.png",
    image="https://www.example.com/image.png",
    actions=[Action(command="COMMAND_TEST", label="LABEL_TEST", data={"test": "test"})],
    timeout=1000,
    audio=Audio(
        source="https://www.example.com/audio.mp3",
        volume=100,
    ),
)
