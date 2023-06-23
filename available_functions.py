
available_functions = [
                {
                    "name": "get_light_entities",
                    "description": "returns a list of light entities which can be passed to a function for changing"
                                   " the state of each light in the list."
                                   "This function must be called first if a user has requested to change the state of"
                                   "lights and you have not first been given a list of available light entities",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lights": {
                                "type": "string",
                                "description": "A list of light entities returned from the get_light_entities function",
                            },
                        },
                        "required": [],
                    },
                },
                {
                    "name": "turn_on_lights",
                    "description": "Send a request to a HomeAssistant Rest API to turn on lights. "
                                   "you must use the get_light_entities function first to retrieve the list"
                                   " of available lights.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lights": {
                                "type": "string",
                                "description": "A list of one or more light entities",
                            },
                        },
                        "required": ["lights"],
                    },
                },
                {
                    "name": "turn_off_lights",
                    "description": "Sends a request to a HomeAssistant Rest API to turn off lights. "
                                   "you must use the get_light_entities function first to retrieve the list"
                                   " of available lights.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lights": {
                                "type": "string",
                                "description": "A list of one or more light entities",
                            },
                        },
                        "required": ["lights"],
                    },
                },
                {
                    "name": "get_media_entities",
                    "description": "returns a list of media player entities which can later be passed to a function"
                                   " which makes use of media player entities."
                                   " This function must be called first if a user has requested to perform an action"
                                   "with a media player and you have not first been given a list"
                                   " of available media player entities",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "media_players": {
                                "type": "string",
                                "description": "A list of media player entities in the users smart home",
                            },
                        },
                        "required": [],
                    },
                },
                {
                    "name": "broadcast_message",
                    "description": "This function is used if the user would like to broadcast a message"
                                   "or have a media player say something with tts, send the users requested"
                                   "message as the message parameter",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "media_player_id": {
                                "type": "string",
                                "description": "A list of media player entities to send to broadcast_message function",
                            },
                            "message": {
                                "type": "string",
                                "description": "The message to broadcast on the media player/s",
                            },
                        },
                        "required": ["media_player_id", "message"],
                    },
                },
                {
                    "name": "light_adjust",
                    "description": "Send a request to a HomeAssistant Rest API to change the brightness of lights. "
                                   "you must use the get_light_entities function first to retrieve the list"
                                   " of available lights.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lights": {
                                "type": "string",
                                "description": "A list of one or more light entities",
                            },
                            "brightness": {
                                "type": "integer",
                                "description": "percentage brightness to set a light to",
                            },
                        },
                        "required": ["lights", "brightness"],
                    },
                },
            ]


