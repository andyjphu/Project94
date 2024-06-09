import time, pprint, os, datetime, random, math

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()



population = {
    "farmers": {
        "arable_land": 1000, # "max count of farmers"
        "count": 125,
        "food": 125,
        "production_efficiency": 1.1,
        "knowledge": 0.0, 
        "tools": 0,
    
    }, 
    "artisans": {
        "count": 0,
        "production_efficiency": 0.0,
        "knowledge": 0.0,
        "tools": 0,
    },
}

current_date = datetime.datetime.now()


while True:
    # clear terminal
    os.system("clear")

    # print all relevant data
    print(current_date.strftime("%Y-%m-%d"), "\n", "-" * 20)
    #print(f"{Style.BRIGHT}", end="")
    pprint.pprint(population)

    # --------------------------------

    # update the current date
    current_date += datetime.timedelta(days=1)

    # --------------------------------

    # update artisan population
    if (population["farmers"]["count"] < population["farmers"]["tools"]):
        population["artisans"]["count"] -= 1
        population["farmers"]["count"] += 1 
        print("Demoted an artisan to farmer, Unsold tools")

    # update artisan knowledge
    population["artisans"]["knowledge"] += min(100, math.log(max(1, population["artisans"]["count"])) * 0.00001)

    # update artisan production efficiency
    population["artisans"]["production_efficiency"] = 2 + population["artisans"]["knowledge"]

    # --------------------------------

    # Update the tools
    population["farmers"]["tools"] = int(population["artisans"]["count"] * population["artisans"]["production_efficiency"])

    # Update production efficiency
    population["farmers"]["production_efficiency"] = max(0, ((1500 - population["farmers"]["count"])/1000 ) + population["farmers"]["knowledge"]  + (population["farmers"]["tools"] / population["farmers"]["count"]) )

    # Update the food
    food_consumption = population["farmers"]["count"] + population["artisans"]["count"]

    food_production = (
        population["farmers"]["count"] * population["farmers"]["production_efficiency"] 
    )

    food_surplus = int(food_production - food_consumption +  (population["farmers"]["food"] * 0.75))

    # Update population
    if (food_surplus < 0):
        population_loss = min(int(0.25 * population["farmers"]["count"]), -food_surplus)
        print(f"Not enough food, lost {population_loss} farmers")
        population["farmers"]["food"] = 0
        population["farmers"]["count"] -= population_loss

        # Demote an artisan to farmer
        population["farmers"]["count"] += 1
        population["artisans"]["count"] -= 1
        print("Demoted an artisan to farmer")
    else:
        population["farmers"]["food"] = max(0, food_surplus)

        # Update the population, can't increase too fast
        old_population = population["farmers"]["count"]

        population["farmers"]["count"] = int(population["farmers"]["count"] * min(max(1.0, (population["farmers"]["food"] / (population["farmers"]["count"] + population["artisans"]["count"]))  - 0.25), 1.05))

        print(f"{population['farmers']['count'] - old_population} new farmers!")

    population["farmers"]["knowledge"] += min(100, math.log(population["farmers"]["count"]) * 0.00001)

    # --------------------------------

    # population promotion for artisans

    if ( population["farmers"]["count"] > population["farmers"]["tools"] and    (population["farmers"]["food"] /( population["farmers"]["count"] + population["artisans"]["count"])) > 1.05):
        population["artisans"]["count"] += 1
        population["farmers"]["count"] -= 1
        print("1 new artisan!")

    time.sleep(0.25)
