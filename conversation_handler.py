from Alice.server.utils import count_words, remove_first_words, davinci_completion

def conversation_handler(conversation):
    tokens_in_conversation = count_words(conversation)
    
    if tokens_in_conversation < 700:
        return conversation
    
    if tokens_in_conversation < 1000:
        extra_tokens = tokens_in_conversation - 1000
        return remove_first_words(conversation, extra_tokens)
    
    if tokens_in_conversation < 1500:
        summary_prompt = "Summarize the following Question and Answer conversation and generate a summarized form of Q and A in Q: and A: format:\n\n" + conversation
        conversation_summary = generate_conversation_summary(summary_prompt)
        return conversation_summary
    
    extra_tokens = tokens_in_conversation - 1500
    new_conversation = remove_first_words(conversation, extra_tokens)
    summary_prompt = "Summarize the following Question and Answer conversation and generate a summarized form of Q and A in Q: and A: format:\n\n" + conversation
    conversation_summary = generate_conversation_summary(summary_prompt)
    return conversation_summary

def generate_conversation_summary(summary_prompt):
    return davinci_completion(
        summary_prompt,
        temperature=0.0,
        max_tokens=700,
        top_p=1.0,
        n=1,
        frequency_penalty=1.5,
        presence_penalty=2.0,
        logprobs=10,
        model="text-davinci-003",
    )
