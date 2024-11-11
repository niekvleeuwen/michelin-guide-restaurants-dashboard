from data.database import Database
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from loguru import logger
from singleton import SingletonMeta

OPENAI_MODEL = "gpt-3.5-turbo"


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

    def invoke_analysis_llm(self, prompt: str) -> str:
        """Invoke the LLM with a given prompt."""
        input_str = self.ANALYSIS_PROMPT.format(prompt)
        response = self.agent_executor.invoke({"input": input_str})
        return response["output"]

    def invoke_recommendations_llm(
        self,
        location_preference: str,
        cuisine_preference: str,
        price_range: list,
        award_range: list,
        description_of_restaurant: str,
    ) -> str:
        """Invoke the LLM to make a recommendation using the SQL agent."""
        input_str = f"""
        You are a helpful assistant recommending restaurants based on user preferences.
        Use the connected database to recommend a restaurant based on the following user preferences.
        Construct and execute SQL queries as needed to find a suitable match, prioritizing the user's preferences.
        Please use the "Price (normalized)" column.

        User Preferences:
        - City or Country Preference: {location_preference if location_preference else "Any location"}
        - Cuisine Preference: {cuisine_preference if cuisine_preference else "Any cuisine"}
        - Price Normalized Range: {', '.join(price_range) if price_range else "Any price range"}
        - Award Range: {', '.join(award_range) if award_range else "Any award level"}
        - Description of Desired Restaurant: {
            description_of_restaurant if description_of_restaurant else "No specific description"
        }

        Make sure that the that the results includes the restaurant's name, location, cuisine, price range, awards,
        and a brief explanation of why it fits the user's preferences.
        Ensure your response feels conversational and helpful, as if you are directly speaking to the user about your
        recommendation.
        """
        print(input_str)
        response = self.agent_executor.invoke({"input": input_str})
        return response["output"]
