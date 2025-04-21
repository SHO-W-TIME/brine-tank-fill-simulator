import anvil.files
from anvil.files import data_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def import_tanks_csv():
    # Read the contents of a file
    with open(data_files['tanks.csv']) as f:
        tanks = f.read()
    return tanks

@anvil.server.callable
def import_pumps_csv():
    # Read the contents of a file
    with open(data_files['pumps.csv']) as f:
        pumps = f.read()
    return pumps
