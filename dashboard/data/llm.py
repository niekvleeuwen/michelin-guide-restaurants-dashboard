import os

from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from loguru import logger

from dashboard.data.database import Database
from dashboard.singleton import SingletonMeta

OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


class LLM(metaclass=SingletonMeta):
    def __init__(self) -> None:
        logger.debug("LLM object is being created..")
        logger.debug("Creating database")
        db = Database().get_db()
        logger.debug("Creating LLM")
        llm = ChatOpenAI(model=OPENAI_MODEL)
        logger.debug("Creating executor")
        self.agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

    def invoke_llm(self, prompt: str) -> str:
        """Invoke the LLM with a given prompt."""
        response = self.agent_executor.invoke({"input": prompt})
        print(response)
        return response["output"]
