from urllib import request
import random
import time

def ms(id):
    run = True
    while(run):
        time.sleep(30)
        val= random.randint(1, 18)
        if val==1:
            run=False
            request.urlopen(f"http://localhost:8000/machine/end/{id}/{val}")
        else:
            request.urlopen(f"http://localhost:8000/machine/add/{id}/{val}")

id=""

with request.urlopen("http://localhost:8000/machine/start/") as response:
    id=response.headers["msid"]

ms(id)
    
