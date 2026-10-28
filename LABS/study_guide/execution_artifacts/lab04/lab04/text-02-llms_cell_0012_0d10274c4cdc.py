import datetime

chat_template = """
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023
Today Date: """+datetime.datetime.now().strftime("%d %b %Y")+"""

{system_message}

<|eot_id|>
<|start_header_id|>user<|end_header_id|>

{user_message}

<|eot_id|>
"""