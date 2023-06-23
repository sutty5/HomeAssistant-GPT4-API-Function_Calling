# Home Assistant GPT API - With Function Calling

<h1>A chat interface for HomeAssistant that actually can control devices!</h1>

<hr/>

This project makes use of the Home Assistant REST API and GPT-4 Function Calling.
This Powerful combination enables you to converse directly with GPT to directly control
your local HA Instance. As this project currently stands, it is a basic CLI interface for asking 
GPT-4 to perform actions on HA Devices. If GPT decided it needs to call a function
that is currently a function inside gpt_requests.py, it can call this function to send
commands directly to the HA REST API.

<hr/>

<h1>Requirements:</h1>

<ul>
    <li>Install the requirements</li>
    <li>Please set Environment Variable ["OPENAI_API_KEY]</li>
    <li>Inside main.py replace the Instance URL with your HomeAssistant URL e.g. http://homeassistantpi.local:8123</li>
    <li>Create a Long-Lived Access Token in your HA Instance, store this key in
    an environment variable ["HOME_ASSISTANT_TOKEN"]</li>
</ul>

<hr/>

<h1>Run main.py</h1>
<p>Run main.py, you can now chat with GPT-4 and ask it to control devices. Not all devices are supported yet as
I need to build out the functions</p>

<hr/>

<h1>Contributing:</h1>
<p>Anyone is welcome to contribute to the project, this is very early stages and
will likely change a lot as it progresses, code is very suboptimal and will become more
OOP as I work it out. Ultimately I envision this existing in various ways...
Such as voice control rather than text input, easily done with OpenAIs Whisper model. And somehow, ultimately
this needs to be a keyword listening speech-to-text server. Just imagine! "Hey HomeAssistant, Can you please lock up 
and let me know if the windows are all closed?"

<br>
I fully expect the code-base to completely change, this is basically a working draft.
</p>




