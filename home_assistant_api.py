import requests
import os
import json


class HomeAssistant:

    def __init__(self, instance_url: str):
        """
        Initialize HomeAssistant instance with the given URL.

        :param instance_url: The URL of the Home Assistant instance, e.g., http://YOUR_HA_URL:8123/

        Ensure you have a long-lived access token created from http://YOUR_HA_URL:8123/profile
        store the token in environment variable named HOME_ASSISTANT_TOKEN
        """

        # HomeAssistant Bearer Token
        self.token = os.getenv("HOME_ASSISTANT_TOKEN")
        if instance_url[-1] == "/":
            instance_url = instance_url[:-1]  # remove the "/"
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
        # print(self.device_states_data)
        self.service_url = f"{self.instance_url}services/"
        self.light_toggle_service_url = f"{self.service_url}light/toggle"
        self.switch_toggle_service_url = f"{self.service_url}switch/toggle"
        self.cloud_say_service_url = f"{self.service_url}tts/cloud_say"
        self.light_turn_on_service_url = f"{self.service_url}light/turn_on"
        self.light_turn_off_service_url = f"{self.service_url}light/turn_off"

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
        if entity_type == "all":
            entity_list = [entity["entity_id"] for entity in self.device_states_data
                           if entity["state"] != "unavailable"
                           and any(value in entity["entity_id"] for value in entity_type_dict.values())]
            return entity_list

        elif entity_type not in entity_type_dict:
            entity_type_dict[entity_type] = f"{entity_type}."

        try:
            entity_list = [entity["entity_id"] for entity in self.device_states_data
                           if entity_type_dict[entity_type] in entity["entity_id"]
                           and entity["state"] != "unavailable"]
        except KeyError:
            return f"Error, No entities of type {entity_type} found"
        else:
            return entity_list

    def get_light_entities(self):
        """Returns a list of all available light entities"""
        entity_list = [entity["entity_id"] for entity in self.device_states_data
                       if "light." in entity["entity_id"]
                       and entity["state"] != "unavailable"]

        entity_json = {
            "light_entities": entity_list,
        }
        return json.dumps(entity_json)

    def get_media_entities(self):
        """Returns a list of all available media entities"""
        entity_list = [entity["entity_id"] for entity in self.device_states_data
                       if "media_player." in entity["entity_id"]
                       and entity["state"] != "unavailable"]

        entity_json = {
            "media_player_entities": entity_list,
        }
        return json.dumps(entity_json)

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

    def broadcast_message(self, media_player_id: str, message: str):
        """
        pass in media entity and string to announce a message
        :param media_player_id:
        :param message:

        :return: returns message to GPT to indicate the function was run
        """
        url = self.cloud_say_service_url
        data = {"entity_id": media_player_id, "message": message, }
        requests.post(url, headers=self.headers, json=data)
        action_performed = {
            "action_performed": "The message was broadcast successfully, no further action required.",
        }
        return json.dumps(action_performed)

    # method for light dimming
    def light_adjust(self, lights, brightness=None, color=()):
        url = self.light_turn_on_service_url

        light_list = lights.split(",")

        for light in light_list:
            data = {"entity_id": light, "brightness_pct": brightness}
            requests.post(url, headers=self.headers, json=data)

        action_performed = {
            "action_performed": f"The specified lights have been adjusted to {brightness}%",
        }
        return json.dumps(action_performed)

    def turn_on_lights(self, lights):

        """
        :param lights:
        :return: returns message to GPT to indicate the function was run
        """
        url = self.light_turn_on_service_url

        light_list = lights.split(",")

        for light in light_list:
            data = {"entity_id": light}
            requests.post(url, headers=self.headers, json=data)
        action_performed = {
            "action_performed": "The specified lights have been turned on",
        }
        return json.dumps(action_performed)

    def turn_off_lights(self, lights):

        """
        :param lights:
        :return: returns message to GPT to indicate the function was run
        """
        url = self.light_turn_off_service_url
        light_list = lights.split(",")

        for light in light_list:
            data = {"entity_id": light}
            requests.post(url, headers=self.headers, json=data)
        action_performed = {
            "action_performed": "The specified lights have been turned off",
        }
        return json.dumps(action_performed)
