import logging
from mopidy import config, ext

__version__ = '0.1.0'

logger = logging.getLogger(__name__)

class Extension(ext.Extension):

    dist_name = 'Mopidy-HomeAssistant'
    ext_name = 'homeassistant'
    version = __version__

    def get_default_config(self):
        return """
        [homeassistant]
        enabled = true
        api_url = http://your-home-assistant-url:8123
        api_token = your-long-lived-access-token
        media_player_entity = media_player.your_media_player_entity
        """

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['api_url'] = config.String()
        schema['api_token'] = config.Secret()
        schema['media_player_entity'] = config.String()
        return schema

    def setup(self, registry):
        from .mixer import HomeAssistantMixer
        registry.add('mixer', HomeAssistantMixer)
