osu.py
-------------
A simple async API wrapper for Osu API

**Python 3.8 or higher**

To install the library, run the following command

*Note: you must have git installed in order to install this library.*

.. code:: sh

  #Linux/macOS
  python3 -m pip install -U git+https://github.com/SawshaDev/osu.py
  
  #Windows
  py -m pip install -U git+https://github.com/SawshaDev/osu.py
  
Quick Example
-------------
  
.. code:: py
  
  import osu
  import asyncio
  
  async def main():
    client = osu.Client(client_secret="YourClientSecret", client_id=clientid)
    return await client.fetch_user("Sawsha")

  user = asyncio.run(main())
  print(user)
  print(user.username)
  
