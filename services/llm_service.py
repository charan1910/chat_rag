from langchain.llms.base import LLM
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
import requests
import numpy as np
from config import api_key


class GrokLLM(LLM):
    api_key: str
    endpoint: str = "https://api.x.ai/v1/chat/completions"

    def _call(self, prompt: str, stop=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        json_data = {'messages': [{'role': 'system', 'content': 'You are a chatbot assistant.'}, {'role': 'user', 'content': prompt}], 'model': 'grok-beta', 'temperature': 0}
        response = requests.post(self.endpoint, headers=headers, json=json_data)
        return response.json()["choices"][0]["message"]["content"] if response.status_code == 200 else f"Error: {response.status_code} - {response.text}"

    @property
    def _llm_type(self):
        return "grok_llm"

def retrieve_relevant_chunks(index, question, model):
    question_embedding = model.encode([question])
    distances, indices = index.search(np.array(question_embedding), k=5)  # Top 5 matches
    return indices

def initialize_chain():
    grok_llm = GrokLLM(api_key=api_key)
    template = "The conversation so far:\n{chat_history}\n\nThe user asked: {question}\nProvide a helpful and concise answer."
    prompt = PromptTemplate(template=template, input_variables=["chat_history", "question"])
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="question")
    return LLMChain(llm=grok_llm, prompt=prompt, memory=memory)
