import pykka
import requests
import logging
import threading
import asyncio
import websockets
import json
import time
from mopidy import mixer

logger = logging.getLogger(__name__)

class HomeAssistantMixer(pykka.ThreadingActor, mixer.Mixer):
    name = "HomeAssistant"

    def __init__(self, config):
        super(HomeAssistantMixer, self).__init__()
        self.api_url = config['homeassistant']['api_url']
        self.api_token = config['homeassistant']['api_token']
        self.entity_id = config['homeassistant']['media_player_entity']
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        self.current_volume = None
        self.websocket_thread = threading.Thread(target=self.run_websocket)
        self.websocket_thread.daemon = True
        self.websocket_thread.start()

    def run_websocket(self):
        """Create a new asyncio event loop and run the WebSocket connection."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connect_websocket())

    async def connect_websocket(self):
        """Connect to Home Assistant's WebSocket API and subscribe to state changes for the specific entity."""
        websocket_url = f"{self.api_url.replace('http', 'ws')}/api/websocket"
        logger.info(f"Connecting to WebSocket URL: {websocket_url}")
        while True:
            try:
                # Establish WebSocket connection
                async with websockets.connect(websocket_url) as websocket:
                    logger.info("WebSocket connection established. Waiting for 'auth_required'...")

                    # Wait for the 'auth_required' message
                    response = json.loads(await websocket.recv())
                    logger.info(f"Received WebSocket authentication initiation message: {response}")
                    if response.get('type') != 'auth_required':
                        logger.error("Expected 'auth_required', but received something else.")
                        return

                    # Authenticate with Home Assistant
                    auth_message = {
                        "type": "auth",
                        "access_token": self.api_token
                    }
                    logger.info(f"Sending WebSocket authentication message: {auth_message}")
                    await websocket.send(json.dumps(auth_message))

                    # Wait for the 'auth_ok' message
                    response = json.loads(await websocket.recv())
                    logger.info(f"Received WebSocket authentication response: {response}")
                    if response.get('type') != 'auth_ok':
                        logger.error("WebSocket authentication failed")
                        return

                    logger.info("WebSocket authenticated successfully.")

                    # Subscribe to state changes for the media player entity (platform: state)
                    await websocket.send(json.dumps({
                        "id": 1,
                        "type": "subscribe_trigger",
                        "trigger": {
                            "platform": "state",
                            "entity_id": self.entity_id
                        }
                    }))

                    logger.info(f"Subscribed to state changes for {self.entity_id}")

                    # Listen for events
                    while True:
                        message = await websocket.recv()
                        data = json.loads(message)
                        logger.info(f"Received WebSocket event: {data}")
                        self.handle_event(data)

            except Exception as e:
                logger.error(f"WebSocket connection failed: {e}")
                # Reconnect after a short delay if the connection fails
                time.sleep(5)

    def handle_event(self, event_data):
        """Handle state_changed events for volume_level changes."""
        logger.info(f"Handling event: {event_data}")
        trigger_data = event_data.get('event', {}).get('variables', {}).get('trigger', {})
        
        # Extract the 'to_state' and 'from_state' information
        to_state = trigger_data.get('to_state', {})
        from_state = trigger_data.get('from_state', {})
        
        # Extract the volume level from 'to_state'
        to_volume_level = to_state.get('attributes', {}).get('volume_level')
        from_volume_level = from_state.get('attributes', {}).get('volume_level')

        # Log the volume levels for debugging
        logger.info(f"From volume level: {from_volume_level}, To volume level: {to_volume_level}")

        # Check if the volume level has actually changed and update Mopidy if necessary
        if to_volume_level is not None and from_volume_level != to_volume_level:
            new_volume_percentage = int(to_volume_level * 100)
            logger.info(f"Updating volume in Mopidy to {new_volume_percentage}%")
            self.current_volume = new_volume_percentage
            self.trigger_volume_changed(new_volume_percentage)

    def get_volume(self):
        """Return the current volume."""
        return self.current_volume if self.current_volume is not None else 0

    def set_volume(self, volume):
        """Set the volume in Home Assistant."""
        try:
            volume_level = volume / 100.0
            payload = {
                "entity_id": self.entity_id,
                "volume_level": volume_level
            }
            response = requests.post(
                f"{self.api_url}/api/services/media_player/volume_set",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            logger.info(f"Volume set to {volume}% in Home Assistant")
            self.current_volume = volume
            self.trigger_volume_changed(volume)
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to set volume in Home Assistant: {e}")
            return False
