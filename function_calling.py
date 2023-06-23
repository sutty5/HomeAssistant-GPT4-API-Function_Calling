import openai
import json
import os
from available_functions import available_functions
from home_assistant_api import HomeAssistant

home_assistant = HomeAssistant(instance_url="YOUR_HA_URL")
openai.api_key = os.getenv("OPENAI_API_KEY")
FUNCTIONS = available_functions

messages = []


class FunctionCalling:

    def __init__(self):
        pass

    # send model the user query and what functions it has access to.

    def run_conversation(self, user_message: str):
        print(messages)

        # If GPT Wants to call a function, it gets called in this first request

        messages.append({"role": "system", "content": "Let's think step-by-step. You have been designed to control"
                                                      " a smarthome. You have access to python functions to enable"
                                                      " you to carry out your tasks. Think about the users request,"
                                                      " and use common sense when choosing which function to run"
                                                      "and what devices should be controlled based on the users"
                                                      "request. e.g. if a user specifies devices in a specific"
                                                      "room or more than one device, then you should include"
                                                      "possible matches in your function calls"})

        messages.append({"role": "user", "content": user_message})
        # print(messages) DEBUG

        # First call to API with initial user request
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
            functions=FUNCTIONS,
            function_call="auto",
        )

        model_response = response["choices"][0]["message"]  # First response
        print(f"First Response: {model_response}")

        # append the model_response to messages so the assistant can keep context
        messages.append(model_response)

        # Now check if the model wants to call a function and call it if so
        if model_response.get("function_call"):  # If function called needed...
            function_name = model_response["function_call"]["name"]
            arguments = json.loads(model_response["function_call"]["arguments"])
            print(f'to be json loaded: {model_response["function_call"]["arguments"]}')

            # call the function
            # Note: the JSON response from the model may not be valid JSON
            function_response = getattr(home_assistant, function_name)(**arguments)

            # Step 4, send model the info on the function call and what the function returned
            # append the function response to messages so assistant has the context
            messages.append({
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    })

            second_response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=messages,
                functions=FUNCTIONS,
                function_call="auto"
            )
            model_response = second_response["choices"][0]["message"]
            print(f"Second Response: {model_response}")

            # append the model_response to messages so the assistant can keep context
            messages.append(model_response)

        else:
            return model_response, "Function call was not requested"

        # Step 2.1, check if the model wants to call another function
        if model_response.get("function_call"):
            function_name = model_response["function_call"]["name"]
            arguments = json.loads(model_response["function_call"]["arguments"])

            # Step 3, call the function
            # Note: the JSON response from the model may not be valid JSON
            function_response = getattr(home_assistant, function_name)(**arguments)

            # Step 4, send model the info on the function call and function response
            messages.append({
                "role": "function",
                "name": function_name,
                "content": function_response,
            })
            third_response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=messages,
                functions=FUNCTIONS,
                function_call="auto"
            )

            model_response = third_response["choices"][0]["message"]
            # append the model_response to messages so the assistant can keep context
            messages.append(model_response)

            print(f"Third Response: {model_response}")
            return third_response

        else:
            return model_response, "Function call was not requested"
