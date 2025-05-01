from ._anvil_designer import SimulatorTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

class Simulator(SimulatorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.simulator_card.visible = False
    self.how_to_use_card.visible = True
    self.references_card.visible = False
    self.contact_card.visible=False
    # Any code you write here will run before the form opens.
  
  def calculate_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Check if variables are negative, if they are then alert and prompt a re-enter
    if int(self.rho.text) < 0:
      alert("Rho is negative. Please re-enter")
      pass

    if int(self.L.text) < 0:
      alert("Pipe length is negative. Please re-enter")
      pass

    if int(self.D.text) < 0:
      alert("Pipe diameter is negative. Please re-enter")
      pass
      
    if int(self.h_elevation.text) < 0:
      alert("Height difference is negative. Please re-enter")
      pass      
      
    if int(self.f.text) < 0:
      alert("Darcy friction factor is negative. Please re-enter")
      pass

    if int(self.K_minor.text) < 0:
      alert("The total minor losses are negative. Please re-enter")
      pass
    # Call different variations of the solver code depending on whether CSVs are being sent or not
    if self.pump.selected_value == "CSV File": #if CSV feature here is not empty, obtain a,b,c
      pump_list = self.file_loader_pumps.file.get_bytes().decode()
      pump_list = pump_list.split('\r\n')
      pump_list.pop(-1)
      split_pump_list = []
      for item in pump_list:
        item = item.split(',')
        split_pump_list.append(item)
      split_pump_list = [item for sublist in split_pump_list for item in sublist]
      split_pump_list = [float(x) for x in split_pump_list]
      pump_list = split_pump_list
    else:
      pump_list = [0]

    if self.tank.selected_value == "CSV File": #if CSV feature here is not empty, collect vector of custom tank volumes
      tank_list = self.file_loader_tanks.file.get_bytes().decode()
      tank_list = tank_list.split('\r\n')
      tank_list.pop(-1)
      tank_list = [int(x) for x in tank_list]
    else:
      tank_list = [0]

     # Assign values if user-defined pump and/or tank values are provided
    if self.pump.selected_value == "Other": #if other pump, obtain a,b,c
      pump_list = [float(self.pump_a.text), float(self.pump_b.text), float(self.pump_c.text)]
      other_pump = tuple(pump_list)
    else:
      other_pump = (0,0,0)

    if self.tank.selected_value == "Other": #if other tank, obtain volume
      other_tank = float(self.tank_v.text)
    else:
      other_tank = 0

    if (self.pump.selected_value != "CSV File") and (self.tank.selected_value != "CSV File"): #non-CSV case
      Q_solution, t_fill = anvil.server.call('anvilSolver', 
                                            float(self.rho.text), 
                                            float(self.L.text), 
                                            (float(self.D.text)/12),
                                            float(self.h_elevation.text),
                                            float(self.f.text),
                                            float(self.K_minor.text),
                                            float(self.LossVar.text),
                                            self.pump.selected_value,
                                            self.tank.selected_value,
                                            other_pump,
                                            other_tank)
    elif (self.tank.selected_value == "CSV File") and (self.pump.selected_value != "CSV File"): #tank CSV case
      Q_solution, t_fill = anvil.server.call('anvilSolver_tank_CSV', 
                                            float(self.rho.text), 
                                            float(self.L.text), 
                                            (float(self.D.text)/12),
                                            float(self.h_elevation.text),
                                            float(self.f.text),
                                            float(self.K_minor.text),
                                            float(self.LossVar.text),
                                            self.pump.selected_value,
                                            tank_list,
                                            other_pump)
    elif (self.tank.selected_value != "CSV File") and (self.pump.selected_value == "CSV File"): #pump CSV case
      Q_solution, t_fill = anvil.server.call('anvilSolver_pump_CSV', 
                                            float(self.rho.text), 
                                            float(self.L.text), 
                                            (float(self.D.text)/12),
                                            float(self.h_elevation.text),
                                            float(self.f.text),
                                            float(self.K_minor.text),
                                            float(self.LossVar.text),
                                            self.tank.selected_value,
                                            pump_list,
                                            other_tank)
    else:
      Q_solution, t_fill = anvil.server.call('anvilSolver_dual_CSV', 
                                            float(self.rho.text), 
                                            float(self.L.text), 
                                            (float(self.D.text)/12),
                                            float(self.h_elevation.text),
                                            float(self.f.text),
                                            float(self.K_minor.text),
                                            float(self.LossVar.text),
                                            tank_list,
                                            pump_list)
      
    #print(Q_solution)
    #print(t_fill)
    
    result_dict = {}
    result_items = []
    
    if (self.pump.selected_value != "CSV File") and (self.tank.selected_value != "CSV File"):
      self.result_grid.visible = False
      self.repeating_panel_1.visible = False
      if Q_solution:
        self.flow_rate_result.visible = True
        self.flow_rate_result.text = "Calculated Flow Rate = " + f"{Q_solution:.2f}" + " gpm"
      if t_fill:
        self.fill_time_result.visible = True
        self.fill_time_result.text = "Calculated Fill Time = " + f"{t_fill:.2f}" + " min"
    else:
      self.result_grid.visible = True
      self.repeating_panel_1.visible = True
      self.flow_rate_result.visible = False
      self.fill_time_result.visible = False
      if (self.pump.selected_value != "CSV File") and (self.tank.selected_value == "CSV File"):
        for pump_name in list([self.pump.selected_value]):
          for j in range(len(tank_list)):
            result_dict['pump'] = pump_name
            result_dict['tank'] = tank_list[j]
            result_dict['flow'] = f"{Q_solution:.2f}"
            result_dict['fill'] = f"{t_fill[j]:.2f}"
            result_items.append(result_dict.copy())
      elif (self.pump.selected_value == "CSV File") and (self.tank.selected_value != "CSV File"):
        for tank_name in list([self.tank.selected_value]):
          for j in range(len(pump_list) // 3):
            result_dict['pump'] = f"Pump #{j+1}"
            if tank_name == "Other":
              result_dict['tank'] = self.tank_v.text
            else:
              result_dict['tank'] = tank_name
            result_dict['flow'] = f"{Q_solution[j]:.2f}"
            result_dict['fill'] = f"{t_fill[j]:.2f}"
            result_items.append(result_dict.copy())
      elif (self.pump.selected_value == "CSV File") and (self.tank.selected_value == "CSV File"):
        for i in range(len(pump_list) // 3):
          for j in range(len(tank_list)):
            result_dict['pump'] = f"Pump #{i+1}"
            result_dict['tank'] = tank_list[j]
            result_dict['flow'] = f"{Q_solution[3*i+j]:.2f}"
            result_dict['fill'] = f"{t_fill[3*i+j]:.2f}"
            result_items.append(result_dict.copy())

      self.repeating_panel_1.items = result_items
          


  def how_to_use_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.how_to_use_card.visible = True
    self.simulator_card.visible = False
    self.references_card.visible = False
    self.contact_card.visible=False
    pass

  def simulator_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.simulator_card.visible = True
    self.how_to_use_card.visible = False
    self.references_card.visible = False
    self.contact_card.visible=False
    pass

  def references_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.references_card.visible = True
    self.simulator_card.visible = False
    self.how_to_use_card.visible = False
    self.contact_card.visible=False
    pass

  def contact_click(self,**event_args):
    # switches to contact page when clicked
    self.contact_card.visible=True
    self.references_card.visible=False
    self.simulator_card.visible=False
    self.how_to_use_card.visible=False

  def form_refreshing_data_bindings(self, **event_args):
    """This method is called when refresh_data_bindings is called"""
    pass

  def K_minor_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass

  def pump_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.pump.selected_value == "Other":
      self.disclaimer_2.visible = True
      self.custom_a.visible = True
      self.custom_b.visible = True
      self.custom_c.visible = True
      self.pump_a.visible = True
      self.pump_b.visible = True
      self.pump_c.visible = True
    else:
      self.disclaimer_2.visible = False
      self.custom_a.visible = False
      self.custom_b.visible = False
      self.custom_c.visible = False
      self.pump_a.visible = False
      self.pump_b.visible = False
      self.pump_c.visible = False
      
    if self.pump.selected_value == "CSV File":
      self.custom_pumps.visible = True
      self.file_loader_pumps.visible = True
    else:
      self.custom_pumps.visible = False
      self.file_loader_pumps.visible = False
    pass

  def tank_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.tank.selected_value == "Other":
      self.custom_volume.visible = True
      self.tank_v.visible = True
    else:
      self.custom_volume.visible = False
      self.tank_v.visible = False

    if self.tank.selected_value == "CSV File":
      self.custom_tanks.visible = True
      self.file_loader_tanks.visible = True
    else:
      self.custom_tanks.visible = False
      self.file_loader_tanks.visible = False
    pass

  def f_show(self, **event_args):
    """This method is called when the TextBox is shown on the screen"""
    self.f.text = f"{0.02:.2f}"
    pass

  def LossVar_show(self, **event_args):
    """This method is called when the TextBox is shown on the screen"""
    self.LossVar.text = 0
    pass

  def rho_show(self, **event_args):
    """This method is called when the TextBox is shown on the screen"""
    self.rho.text = f"{64.1:.2f}" #(Density of 23.3% salinity water)
    pass

# Contact Page
  #function to send email with entered fields
  def send_click(self, **event_args):
    """This method is called when the send button is clicked"""
    name = self.name.text
    email = self.email.text
    feedback = self.feedback.text
    anvil.server.call('send_feedback', name, email, feedback)
    Notification("Thank you for your message!").show()
    self.name.text = ""
    self.email.text = ""
    self.feedback.text = ""
    pass


