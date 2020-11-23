# StockWatcher
Used in Amz B4U servers to snipe their stock. &lt;3         


## How to use StockWatcher
Fork StockWatcher or download/copy the `stockv2.py` file to your computer.         
Download [Python 3.8](https://www.python.org/downloads/release/python-386/) - remember to follow the steps, since you __need__ to add to PATH.               
Right click in the folder where you have `stockv2.py` and make a file named `token.json` with the following format                 
`{"token": "INSERT TOKEN HERE"}` where you replace the text with your Discord token.              
In your folder, open command prompt by clicking the bar, write `cmd` and click enter.                
When in the opened command prompt window, write `py stockv2.py` or alternatively `python stockv2.py`             

Edit `stockv2.py` to fit your servers - insert server id's in the `server_ids` list.
I've just inserted two that I used it on, which worked perfectly fine.
I'd recommend adding a small delay so you don't look that suspicious, and possibly adding an array of random texts.
      

## How to get your Discord Token
Go to [Discord](https://www.discord.com/) and click CTRL+I and login or click the first https://discord.com/api/v8/science request you can find.               
Look under headers and you should be able to find an Authorization header - just get the value of it.               
That's it!               

------
You're welcome to customize this all you want, as this is free and open source! <3              
