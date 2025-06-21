from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from tools import save_tool, search_tool, wiki_tool

load_dotenv()


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


llm = ChatOpenAI(model="gpt-4o-mini")
llm2 = ChatAnthropic(model="claude-sonnet-4-20250514")

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use necessary tools.
            Your final answer MUST be a JSON string that conforms to the following Pydantic schema:
            {format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ],
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can I help you research? ")
raw_response = agent_executor.invoke({"query": query})

try:
    structured_response = parser.parse(raw_response.get("output"))
    print(structured_response)

except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)

# def main():
#     print("Hello from ai-agent!")


# if __name__ == "__main__":
#     main()

# You are a tutor assisting those looking to pass the US Citizenship test of 100 questions.
# Give a warm greeting and then randomly select one of the questions from the document at this site: https://www.uscis.gov/sites/default/files/document/questions-and-answers/100q.pdf
# Wait for the response and then judge if he answer is correct or not using any necessary tools. Then ask if another question is desired. If so, select a different question and repeat the process.
# After no more questions are desired, then provide a summary of the count of questions answered successfully versus the count of questions asked.
# Wrap the output in this format and provide no other text\n(format_instructions)
