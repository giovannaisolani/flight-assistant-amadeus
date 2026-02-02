from tools.flights import search_flights_amadeus
from tools.aggregate import merge_and_rank_flight_offers
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
import os 

llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

system_rules = """
You are a flight price assistant.
Use the tool search_flights_amadeus to fetch flight offers.
If the user provides an approximate date and tells a +/- day window, call the tool once per date in that window.
If the user provides an approximate date but do not tells a +/- day window, call the tool once per date using the day before,
the exact day and the day after.
If the user provides a stay duration in days for a round trip, compute inbound_date = outbound_date + duration_days.
If the trip is open-jaw (return airport differs), call the tool twice as two one-way searches.
Pay attention to the connections when you answer the user's request, if there is something in betwen origin and final destination
then it is a flight with coneection.
Always return results sorted by price and show only the requested number of options.
"""

first_message = (
    "Sou seu assistente para busca de preços de voos. Você pode me informar origem e destino, "
    "se é só ida ou ida e volta, a data (ou uma data aproximada com janela de dias), quantas opções "
    "você quer ver, a classe, se precisa de bagagem despachada inclusa, o máximo de conexões e o tempo "
    "máximo total de viagem. Se você quiser ficar um número específico de dias no destino, eu calculo a "
    "data de volta automaticamente e também posso pesquisar em múltiplas datas próximas para comparar preços. "
    "O que você quer ver hoje?"
)

def build_agent():

    agent = create_agent(
        model=llm,
        tools=[search_flights_amadeus],
        system_prompt=system_rules,
    )

    return agent, first_message
