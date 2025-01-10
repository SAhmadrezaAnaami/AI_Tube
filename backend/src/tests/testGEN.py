from LLM.gemini import Genai
from prompts.getVideo import getVideoPrompts

t = "AIzaSyCNdycC43JpWErW0FzcwlWg8taRrOZ7Z88"
model = Genai(t , sys_instruct=getVideoPrompts)
print(model.generate_text("اموزش زبان انگلیسی از پایه"))