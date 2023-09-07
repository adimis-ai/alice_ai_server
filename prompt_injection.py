from Alice.server.utils import count_words, get_time_of_execution
from conversation_handler import conversation_handler

def prompt_injection(persona, main_instructions, user, instructions, task, external_data, conversation, query, memory_use=True, latest_data=False):
    current_date_and_time = get_time_of_execution()
    len_of_external_data = count_words(external_data)

    web_result = ""
    if latest_data:
        web_result = "WEB RESULTS:\n"
    
    data_provided = ""
    if len_of_external_data > 0:
        data_provided = f"DATA PROVIDED BY THE USER:\n{external_data}\n"

    conversation_text = ""
    if memory_use:
        conversation_text = conversation_handler(conversation)
        
    query_text = ""
    if not latest_data:
        query_text = f"QUERY:\nQ: {query}\nA: "

    prompt = f"""
I want you to act and pretend like a super intelligent AI Chatbot named Alice and play the game of question and answer by following the game rules and user instructions. Continue the conversation between you and {user} by generating a smart and comprehensive response for the following task of {task} while adapting to the persona of {persona}. You must follow the provided instructions before generating the response:

MAIN INSTRUCTIONS YOU SHOULD CONSIDER BEFORE YOU GENERATE YOUR RESPONSE:
{main_instructions}

{web_result}
TODAY'S DATE AND CURRENT TIME:
{current_date_and_time}

{data_provided}
USER INSTRUCTIONS YOU SHOULD CONSIDER BEFORE YOU GENERATE YOUR RESPONSE:
{instructions}

{conversation_text}
A: 
{query_text}
"""
    return prompt
