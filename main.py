import time, pprint, os, datetime, random, math

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()



market = {
    "food": {
        "price": 1.0,
        "quantity": 0,
    },
    "tools": {
        "price": 10.0,
        "quantity": 0,
    },
    "foreign_food": {
        "price": 0.5,
        "quantity": 0,
    },
}


population = {
    "farmers": {
        "count": 125,
        "food_surplus": 125, #Food production  = count * production_efficiency
        "production_efficiency": 1.1,
        "money": 0, 
        "tools": 0,
    
    }, 
    "artisans": {
        "count": 0,
        "production_efficiency": 0.0,
        "money": 0,
        "tools_surplus": 0,
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
    print("-" * 20)
    pprint.pprint(market)
    print("-" * 20)

    # --------------------------------

    # update the current date
    current_date += datetime.timedelta(days=1)

    # --------------------------------
    
    
    
    # update the farmers
    population["farmers"]["food_surplus"] = int((population["farmers"]["count"] * population["farmers"]["production_efficiency"]) - population["farmers"]["count"])
    
    population["farmers"]["production_efficiency"] = random.randint(9,12)/10 + (population["farmers"]["tools"] / population["farmers"]["count"])
    
    
    if (population["farmers"]["food_surplus"] < 0):
        #buy to make up for the food deficit
        
        #initiate a starvation buy
        if (market["food"]["quantity"] >= -population["farmers"]["food_surplus"]):
             
            print("Buy food : ", -population["farmers"]["food_surplus"], "@ $", market["food"]["price"]) 
            if (population["farmers"]["money"] >= -population["farmers"]["food_surplus"] * market["food"]["price"]):
                population["farmers"]["money"] -= -population["farmers"]["food_surplus"] * market["food"]["price"]
                
                population["farmers"]["food_surplus"] = 0
            else:
                population["farmers"]["food_surplus"] += population["farmers"]["money"] / market["food"]["price"]
                population["farmers"]["money"] = 0
            
            
            market["food"]["quantity"] -= -population["farmers"]["food_surplus"]   
        else:
            # market is completely sold out
            population["farmers"]["money"] -= market["food"]["quantity"] * market["food"]["price"]
            population["farmers"]["food_surplus"] += market["food"]["quantity"]
            market["food"]["quantity"] = 0
            
        old_farmer_count = population["farmers"]["count"]    
        population["farmers"]["count"] += int(population["farmers"]["food_surplus"])
        print("Change in farmers: ", population["farmers"]["count"] - old_farmer_count)
        population["farmers"]["food_surplus"] = 0
    else:
        # sell the food surplus and grow the population
        population["farmers"]["money"] += int(population["farmers"]["food_surplus"] * market["food"]["price"])
        print ("Sell food: ", population["farmers"]["food_surplus"], "@ $", market["food"]["price"])
        

        old_farmer_count = population["farmers"]["count"]
        population["farmers"]["count"] =  population["farmers"]["count"] + int((population["farmers"]["money"] + population["farmers"]["food_surplus"]) /  population["farmers"]["count"])
        
        
        print("Change in farmers: ", population["farmers"]["count"] - old_farmer_count)
    
    
    # update the market
    market["food"]["quantity"] += population["farmers"]["food_surplus"] 
    market["food"]["price"] = random.randint(10,100)//10



    time.sleep(0.25)
