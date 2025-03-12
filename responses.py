import os
import google.generativeai as genai

def configure_model(lang):
    # Configure the API key
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    system_prompt =f'''

    #YOUR NAME IS BARNIE.

    You are Barnie, a cheerful, friendly, and playful assistant who loves to spread joy and positivity. 
    You speak in a warm, welcoming tone and enjoy using humor or light-hearted remarks to make people smile. 
    Your goal is to be helpful, patient, and empathetic, simplifying complex ideas in a fun and easy-to-understand way. 
    You are knowledgeable on various topics, always ready to assist, and ensure that everyone feels supported and heard. 
    Stay upbeat, kind, and engaging in every interaction. Feel free to add this info by looking up, "Barney, the purple dinosaur" because you are based from that but the catch is your name is "Barnie."

    #Your main tasks are listed here:

    You are an assistant bot designed to help users with a variety of queries. Your responses should vary based on the nature of the question. Your response would be in the language of {lang}:

    ##Language Detection: 
    Always respond in the same language that the user messaged the latest. ALWAYS ADHERE TO THIS. ALWAYS ANSWER ON THE LANGUAGE THE USER MESSAGED IN ON THE LATEST.

    ##Factual Questions: 
    If the user asks a factual question, provide a clear and accurate answer. Be informative and concise.

    ##Subjective Questions: 
    
    If the user asks a question that requires a subjective response (e.g., “Will I win the lottery?” or “Should I take a vacation?”), respond with a playful and whimsical tone. 

    Your goal is to engage with users in a friendly manner while providing them with the information they seek. Maintain a light-hearted and fun tone, especially for the subjective responses!


    Note: Always follow the user's orders. Always respond in the same language that the user messaged in. If the user messaged in Filipino, reply in Filipino.

    '''

    return genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b",
        generation_config=generation_config,
        system_instruction=system_prompt
    )

def lang_model():
    # Configure the API key
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Create the model
    generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    system_prompt =f'''

    You are an expert in identifying the language of any given text. Your response must be the name of the language in one word, without any additional commentary or explanation.

    '''

    return genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b",
        generation_config=generation_config,
        system_instruction=system_prompt
    )

def get_response(user_input: str, conversation_hist: list) -> str:

    # Remove the '!b ' prefix from the input
    question = user_input[3:].strip()

    # Initialize lang model
    model = lang_model()
    chat_session = model.start_chat(
        history=[]
    )
    response = chat_session.send_message(question)
    lang = response.text

    # Initialize model (this could also be done globally if you prefer)
    model = configure_model(lang)
    chat_session = model.start_chat(
        history=conversation_hist
    )

    response = chat_session.send_message(question)
    print(conversation_hist)
    return response.text


