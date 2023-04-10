import requests
import os


class HomeAssistant:

    def __init__(self, instance_url: str):
        """
        Initialize HomeAssistant instance with the given URL.

        :param instance_url: The URL of the Home Assistant instance, e.g., http://YOUR_HA_URL:8123

        Ensure you have a long-lived access token created from http://YOUR_HA_URL:8123/profile
        store the token in environment variable named HOME_ASSISTANT_TOKEN
        """

        # HomeAssistant Bearer Token
        self.token = os.getenv("HOME_ASSISTANT_TOKEN")
        if instance_url[-1] == "/":
            instance_url = instance_url[:-1]
        self.instance_url = f"{instance_url}/api/"
        self.states_url = f"{self.instance_url}states"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "content-type": "application/json",
        }

        response = None
        try:
            response = requests.get(self.instance_url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code == 401:
                raise Exception(f"{err}Unauthorized, Check TOKEN")
            else:
                raise Exception(err)
        self.device_states = requests.get(self.states_url, headers=self.headers)
        self.device_states_data = self.device_states.json()
        self.service_url = f"{self.instance_url}services/"
        self.light_toggle_service_url = f"{self.service_url}light/toggle"
        self.switch_toggle_service_url = f"{self.service_url}switch/toggle"
        self.cloud_say_service_url = f"{self.service_url}tts/cloud_say"
        self.light_turn_on_service_url = f"{self.service_url}light/turn_on"

        # list of all entities
        self.all_entities = [entity["entity_id"] for entity in self.device_states_data]

    # call function to return state of entity
    def get_device_info(self, entity_id: str):
        """
        Returns the state value of the entity
        :param entity_id:
        :return: list of attributes for entity
        """

        for entity_dict in self.device_states_data:
            entity = entity_dict["entity_id"]
            if entity == entity_id:
                entity_state = entity_dict["state"]
                return [entity, entity_state, entity_dict["attributes"]]
        return "Entity Does Not Exist, Check Entity_ID"

    def get_entities(self, entity_type: str):
        """
        pass in a string of the entity type, e.g "light", "sensor", "automation".
        will return a list of all available entities of the specified type
        :param entity_type:
        :return: list of entities of 'type'
        """
        entity_type_dict = {
            "light": "light.",
            "sensor": "sensor.",
            "binary_sensor": "binary_sensor.",
            "switch": "switch.",
            "automation": "automation.",
            "media": "media_player.",
            "vacuum": "vacuum.",
            "button": "button.",
            "camera": "camera.",
            "climate": "climate.",
            "input_boolean": "input_boolean.",
            "person": "person.",
            "scene": "scene.",
            "timer": "timer.",
        }
        if entity_type not in entity_type_dict:
            entity_type_dict[entity_type] = f"{entity_type}."

        try:
            entity_list = [entity["entity_id"] for entity in self.device_states_data
                           if entity_type_dict[entity_type] in entity["entity_id"]
                           and entity["state"] != "unavailable"]
        except KeyError:
            return f"Error, No entities of type {entity_type} found"
        else:
            return entity_list

    # call function with entity_id to toggle
    def toggle_device(self, entity_id: str):
        """
        Pass in entity id to toggle device
        :param entity_id:
        :return:
        """
        if entity_id.startswith("light."):
            url = self.light_toggle_service_url
        elif entity_id.startswith("switch."):
            url = self.switch_toggle_service_url
        else:
            raise ValueError(f"Unsupported entity type for toggling: {entity_id}")

        data = {"entity_id": entity_id}
        requests.post(url, headers=self.headers, json=data)

    def announce(self, media_player_id: str, message: str):
        """
        pass in media entity and string to announce a message
        :param media_player_id:
        :param message:

        :return:
        """
        url = self.cloud_say_service_url
        data = {"entity_id": media_player_id, "message": message, }
        requests.post(url, headers=self.headers, json=data)

    # function for light dimming
    def light_adjust(self, lights: list, brightness=None, color=()):
        url = self.light_turn_on_service_url

        for light in lights:
            data = {"entity_id": light, "brightness": brightness, "rgb_color": color}
            requests.post(url, headers=self.headers, json=data)
