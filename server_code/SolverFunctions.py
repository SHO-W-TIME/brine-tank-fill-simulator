import anvil.files
from anvil.files import data_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd

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
def pumpCoefficients(pump_file):
  #Read contents of the CSV file
  with open(data_files['pumps.csv']) as file:
    pumps = file.read()
  return pumps

@anvil.server.callable
def tankVolumes(tank_file):
  #Read and organize contents of the tank CSV file
  with open(data_files['tanks.csv']) as file:
    tanks = file.read()
  return tanks

@anvil.server.callable
def anvilSolver(rho, L, D, h_elevation, f, K_minor, LossVar, selected_pump, selected_tank):

  # Constants
  g = 32.2  # ft/s^2 (gravitational acceleration)
  A = np.pi * (D / 2) ** 2  # Pipe cross-sectional area

  # User-selected pump coefficients (example pump curve: H_pump = aQ^2 + bQ + c)
  pump_coeffs = {
    "Sample Pump 1": (-0.005, -0.1, 50),  # coefficients describing the performance curve of the pump
    "Sample Pump 2": (-0.004, -0.09, 48),
  }
  a, b, c = pump_coeffs[selected_pump]

  # Tank selection
  tank_volumes = {
    "Sample Tank 1": 1000,  # gallons
    "Sample Tank 2": 1584,
    "Sample Tank 3": 2000,
  }

  V_gallons = tank_volumes[selected_tank]

  # Define the equation to solve for flow rate Q
  def flow_equation(Q):
    H_pump = a * Q**2 + b * Q + c  # Pump curve equation
    if LossVar == 0:
      v = Q / (A * 448.831)  # Convert GPM to ft/s
      H_friction = f * (L / D) * (v**2 / (2 * g))
      H_minor = K_minor * (v**2 / (2 * g))
      H_static = h_elevation / 2.31  # Convert ft to PSI
      H_total = H_friction + H_minor + H_static
    else:
      H_total = LossVar
    return (H_pump - H_total)  # Find Q where this equals zero

  # Solve for Q using fsolve. Flow equation located above
  Q_initial_guess = 200  # Initial guess for flow rate in GPM
  Q_solution = fsolve(flow_equation, Q_initial_guess)[0]  # Extract single value

  # Compute Fill Time
  t_fill = V_gallons / Q_solution  # Time in minutes

  # Return Results Back to Anvil GUI
  return (Q_solution, t_fill)
