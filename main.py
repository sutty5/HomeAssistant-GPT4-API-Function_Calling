from function_calling import FunctionCalling

function_calling = FunctionCalling()

while True:
    user_command = input("User: ")
    function_calling.run_conversation(user_command)
