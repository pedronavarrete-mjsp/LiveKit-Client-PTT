import reflex as rx
import logging
import asyncio
from livekit import rtc


class LiveKitState(rx.State):
    """State management for LiveKit connection."""

    livekit_url: str = ""
    token: str = ""
    connection_status: str = "disconnected"
    status_message: str = "Ready to connect"
    is_talking: bool = False
    camera_active: bool = False
    remote_participants: list[dict[str, str | bool]] = []
    _monitoring: bool = False
    _room: rtc.Room | None = None
    _audio_publication: rtc.LocalTrackPublication | None = None
    _video_publication: rtc.LocalTrackPublication | None = None
    _audio_track: rtc.LocalAudioTrack | None = None
    _video_track: rtc.LocalVideoTrack | None = None

    @rx.var
    def is_connected(self) -> bool:
        return self.connection_status == "connected"

    @rx.var
    def is_connecting(self) -> bool:
        return self.connection_status == "connecting"

    @rx.var
    def status_color(self) -> str:
        if self.connection_status == "connected":
            return "bg-emerald-500"
        elif self.connection_status == "connecting":
            return "bg-yellow-500"
        elif self.connection_status == "error":
            return "bg-red-500"
        else:
            return "bg-gray-400"

    @rx.event
    def set_url(self, url: str):
        self.livekit_url = url

    @rx.event
    def set_token(self, token: str):
        self.token = token

    @rx.event
    async def connect_to_room(self):
        """Connects to the LiveKit room using the provided credentials."""
        if not self.livekit_url or not self.token:
            self.connection_status = "error"
            self.status_message = "URL and Token are required."
            return
        self.connection_status = "connecting"
        self.status_message = "Establishing connection..."
        yield
        try:
            if self._room is None:
                self._room = rtc.Room()
            options = rtc.RoomOptions(auto_subscribe=False)
            logging.info(f"Connecting to {self.livekit_url}...")
            await self._room.connect(self.livekit_url, self.token, options=options)
            self.connection_status = "connected"
            room_name = (
                self._room.name if self._room and self._room.name else "Unknown Room"
            )
            self.status_message = f"Connected to room: {room_name}"
            logging.info("Successfully connected to LiveKit room.")
            self._monitoring = True
            yield LiveKitState.monitor_room
            yield LiveKitState.setup_media
        except Exception as e:
            logging.exception(f"Failed to connect to LiveKit: {e}")
            self.connection_status = "error"
            self.status_message = f"Connection failed: {str(e)}"
            if self._room:
                try:
                    await self._room.disconnect()
                except Exception as e:
                    logging.exception(
                        f"Error disconnecting after failed connection: {e}"
                    )
                self._room = None

    @rx.event
    async def setup_media(self):
        """Sets up local media tracks after connection."""
        if not self._room or not self.is_connected:
            return
        try:
            self.status_message = "Setting up media devices..."
            self._audio_track = rtc.LocalAudioTrack.create_from_microphone(
                name="mic_main"
            )
            self._audio_publication = await self._room.local_participant.publish_track(
                self._audio_track
            )
            await self._audio_publication.mute()
            self._video_track = rtc.LocalVideoTrack.create_from_camera(
                name="camera_main"
            )
            self._video_publication = await self._room.local_participant.publish_track(
                self._video_track
            )
            self.camera_active = True
            self.status_message = "Connected & Ready"
        except Exception as e:
            logging.exception(f"Media setup failed: {e}")
            self.status_message = f"Media Error: {e}"

    @rx.event
    async def start_talking(self):
        """Enables the microphone track (PTT Press)."""
        if self._audio_publication:
            try:
                await self._audio_publication.unmute()
                self.is_talking = True
            except Exception as e:
                logging.exception(f"Failed to unmute: {e}")

    @rx.event
    async def stop_talking(self):
        """Disables the microphone track (PTT Release)."""
        if self._audio_publication:
            try:
                await self._audio_publication.mute()
            except Exception as e:
                logging.exception(f"Failed to mute: {e}")
        self.is_talking = False

    @rx.event
    async def disconnect_from_room(self):
        """Disconnects from the current room."""
        self.is_talking = False
        self.camera_active = False
        self._monitoring = False
        self.remote_participants = []
        if self._room:
            try:
                await self._room.disconnect()
            except Exception as e:
                logging.exception(f"Error during disconnect: {e}")
            finally:
                self._room = None
                self._audio_publication = None
                self._video_publication = None
                self._audio_track = None
                self._video_track = None
        self.connection_status = "disconnected"
        self.status_message = "Disconnected"

    @rx.event(background=True)
    async def monitor_room(self):
        """Background task to monitor remote participants and tracks."""
        while self.is_connected and self._monitoring:
            async with self:
                if not self._room:
                    break
                try:
                    new_participants = []
                    for sid, p in self._room.remote_participants.items():
                        has_audio = False
                        audio_sub = False
                        for pub in p.track_publications.values():
                            if pub.source == rtc.TrackSource.SOURCE_MICROPHONE:
                                has_audio = True
                                audio_sub = pub.subscribed
                                break
                        has_video = False
                        video_sub = False
                        for pub in p.track_publications.values():
                            if pub.source == rtc.TrackSource.SOURCE_CAMERA:
                                has_video = True
                                video_sub = pub.subscribed
                                break
                        new_participants.append(
                            {
                                "sid": sid,
                                "identity": p.identity or "Unknown",
                                "has_audio": has_audio,
                                "audio_subscribed": audio_sub,
                                "has_video": has_video,
                                "video_subscribed": video_sub,
                            }
                        )
                    self.remote_participants = new_participants
                except Exception as e:
                    logging.exception(f"Error monitoring room: {e}")
            await asyncio.sleep(0.5)

    @rx.event
    async def toggle_subscription(self, sid: str, track_type: str):
        """Toggles subscription for a specific remote track."""
        if not self._room:
            return
        p = self._room.remote_participants.get(sid)
        if not p:
            logging.warning(f"Participant {sid} not found.")
            return
        target_source = (
            rtc.TrackSource.SOURCE_MICROPHONE
            if track_type == "audio"
            else rtc.TrackSource.SOURCE_CAMERA
        )
        for pub in p.track_publications.values():
            if pub.source == target_source:
                try:
                    new_state = not pub.subscribed
                    await pub.set_subscribed(new_state)
                    logging.info(
                        f"Set subscription for {p.identity} {track_type} to {new_state}"
                    )
                except Exception as e:
                    logging.exception(f"Failed to toggle subscription: {e}")
                break