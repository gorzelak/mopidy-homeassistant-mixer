
# Mopidy Home Assistant Mixer

The **Mopidy Home Assistant Mixer** is an extension that allows Mopidy to interface with Home Assistant's media player entities for volume control. By using the power of Home Assistant and its WebSocket API, this mixer extension ensures that volume changes made in Home Assistant are reflected in Mopidy and vice versa.

With this extension, Mopidy can seamlessly control the volume of any Home Assistant-supported media player entity, such as smart speakers, AV receivers, or TV audio systems, allowing full integration between the two platforms.

## Features

- **Two-Way Volume Sync**: Mopidy automatically syncs its volume with the volume level of the specified media player entity in Home Assistant.
- **Real-Time Volume Updates**: Any volume changes in Home Assistant are instantly reflected in Mopidy via WebSocket updates.
- **Mopidy Volume Control**: Changes made in Mopidy are sent to Home Assistant to adjust the volume of the specified media player.
- **Easy Configuration**: Just point the mixer to a Home Assistant media player entity, and you're ready to go.

## Demo

Home Assistant entity (media_player) is on the left and Mopidy web interface (IRIS) on the right.

![Demo GIF](https://github.com/gorzelak/mopidy-homeassistant-mixer/raw/main/demo.gif)


## Requirements

- **Mopidy >= 3.0**
- **Home Assistant (with a configured media player entity)**
- **Python >= 3.6**

## Installation

To install the Mopidy Home Assistant Mixer, run:

```bash
pip install mopidy-homeassistant-mixer
```

## Configuration

Once the extension is installed, you need to configure it by adding the following section to your Mopidy configuration file (`mopidy.conf`):

```ini
[homeassistant]
enabled = true
api_url = http://your-homeassistant-url:8123
api_token = your-long-lived-access-token
media_player_entity = media_player.your_entity_id

api_url: The URL of your Home Assistant instance, including the port.
api_token: A long-lived access token generated in Home Assistant. You can create one by going to Profile > Long-Lived Access Tokens.
media_player_entity: The entity ID of the media player in Home Assistant that you want to control (e.g., media_player.onkyo_receiver).
```

### Usage

Once configured, Mopidy will automatically sync its volume with the specified Home Assistant media player entity. Volume changes made in either Mopidy or Home Assistant will be reflected in both systems.

- **To control volume from Mopidy**: Use Mopidy's normal volume control commands (e.g., via MPD, Iris, or another front-end). Mopidy will send the new volume level to Home Assistant.
- **To control volume from Home Assistant**: Adjust the volume in Home Assistant's UI for the specified media player. The change will be sent to Mopidy, and the volume will sync in real-time.

### Changelog

## v0.1.2
- Initial release of the Mopidy Home Assistant Mixer.
- Support for real-time volume sync between Mopidy and Home Assistant media players.
- Added WebSocket-based communication for efficient updates.
