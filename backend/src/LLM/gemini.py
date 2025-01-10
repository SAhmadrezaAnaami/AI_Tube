import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

import sys
sys.path.append("./utils")

from response import get_response

class Genai():
    def __init__(self ,
                 token ,
                 temperature = 1 ,
                 top_p = 0.95 ,
                 top_k = 40 ,
                 max_output_tokens = 8192 ,
                 model = "gemini-1.5-flash-002" ,
                 sys_instruct = "you are a helpful chatbot",
                 schema =  "False"):
        
        genai.configure(api_key=token)
        if schema == "False":
            self.generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
            "response_mime_type": "text/plain",
            }
        else:
            self.generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
            "response_schema" : schema,
            "response_mime_type": "application/json",
            }
        
        self.sys_instruct = sys_instruct
        self.model = model

    def generate_text(self, text):
        try:
            model = genai.GenerativeModel(
                model_name=self.model,
                generation_config= self.generation_config,
                system_instruction=self.sys_instruct,
            )
            response = model.generate_content(
                text
            )
            return get_response(
                message="Request sent successfully.",
                status="ok",
                code=200,
                data=response.text
            )
        except Exception as e:  # Catch all other exceptions
            return get_response(
                status="error",
                message="An unexpected error occurred.",
                meta=str(e),
                code=500
            )