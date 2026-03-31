from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated,Literal
from langchain_core.messages import BaseMessage,HumanMessage
from pydantic import BaseModel,Field
import operator
from langchain_core.prompts import ChatPromptTemplate
import os
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=os.getenv("GEMINI_API_KEY"))
def chat_node(state:ChatState):
    messages=state["messages"]
    response=model.invoke(messages)
    return {"messages":[response]}
graph=StateGraph(ChatState)
checkpoint=MemorySaver()
graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)
chatbot=graph.compile(checkpointer=checkpoint)

