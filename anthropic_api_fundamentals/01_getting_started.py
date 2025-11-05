# Exercise

# We've only just begun, so this exercise might feel a little underwhelming. It's always good to get some practice with the basics.

# Please do the following: 
# 1. Create a new notebook or Python script.
# 2. Import the proper packages
# 3. Load your Anthropic API key
# 4. Ask Claude to tell you a joke and then print out the result (you can copy/paste the code above and tweak it)
from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")



client = Anthropic(
    api_key=my_api_key
)

our_first_message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Hey Claude, per piacere raccontami un qualcosa di divertente!"}
    ]
)

print(our_first_message.content[0].text)
# Ecco un'idea divertente per te:

# C'era una volta un maiale molto curioso che voleva vedere il mondo al di là della sua fattoria. Un giorno, mentre i suoi amici animali dormivano, il maiale sgattaiolò fuori e si avventurò lungo la strada. Dopo aver camminato per un po', si imbatté in un cartello che indicava la direzione per una città vicina. 

# "Perché no?" pensò il maiale, "Andiamo a vedere cosa c'è in città!"

# Così si mise in cammino verso la città. Quando arrivò, rimase a bocca aperta davanti alle grandi costruzioni e alle tante persone che andavano di fretta per le strade. Non aveva mai visto nulla di simile! 

# Il maiale iniziò a esplorare la città, incuriosito da tutto ciò che vedeva. Ad un certo punto, entrò in un negozio di dolciumi e ne uscì con una enorme scatola piena di caramelle. Poi attraversò una strada a tutta velocità, facendo squittire i freni di un'automobile.

# "Ehi, torna qui!" gridò l'autista, ma il maiale continuava a correre ridendo.

# Alla fine, stanco ma felice, il maiale tornò alla sua fattoria, dove i suoi amici lo accolsero meravigliati dalle sue avventure in città. Da quel giorno, il maiale non smise mai di raccontare le sue divertenti disavventure!

# Spero che questa simpatica storia ti abbia strappato un sorriso! Fammi sapere se vuoi che ti racconti qualcos'altro di divertente.