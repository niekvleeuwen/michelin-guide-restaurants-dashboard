import os

from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from loguru import logger

from dashboard.data.database import Database
from dashboard.singleton import SingletonMeta

OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


class LLM(metaclass=SingletonMeta):
    ANALYSIS_PROMPT = """
    When the user asks about specific restaurant categories, use the following guidelines to determine the appropriate
    column:

    Award Column:
        Use this column if the user mentions "Selected Restaurants," "Bib Gourmand," "1 Star," "2 Stars," or "3 Stars".
        This column categorizes restaurants by Michelin recognition, where:
            "Selected Restaurants" lists all Michelin-approved restaurants.
            "Bib Gourmand" highlights high-quality but value-oriented restaurants.
            "1 Star," "2 Stars," and "3 Stars" denote increasing levels of Michelin prestige.

    Price Normalized Column:
        Use this column if the user mentions "Budget-Friendly," "Moderate," "Premium," or "Luxury".
        This column organizes restaurants by pricing tiers, where:
            "Budget-Friendly" includes affordable dining options.
            "Moderate" indicates mid-range prices.
            "Premium" represents a higher price tier.
            "Luxury" refers to top-tier, high-priced establishments.

    Ensure that you only select data from the relevant column based on these keywords. Here is the user's query:

    {}
    """

    def __init__(self) -> None:
        logger.debug("LLM object is being created..")
        db = Database().get_db()
        llm = ChatOpenAI(model=OPENAI_MODEL)
        self.agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

    def invoke_llm(self, prompt: str) -> str:
        """Invoke the LLM with a given prompt."""
        input_str = self.ANALYSIS_PROMPT.format(prompt)
        response = self.agent_executor.invoke({"input": input_str})
        return response["output"]
