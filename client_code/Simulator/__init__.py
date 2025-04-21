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
    # Call different variations of the solver code depending on whether CSVs are being sent or not?
    if self.pump.selected_value == "CSV File": #if CSV feature here is not empty, obtain a,b,c
      pump_list = self.file_loader_pumps.file.get_bytes().decode()
      print(pump_list)
    if self.tank.selected_value == "CSV File": #if CSV feature here is not empty, collect vector of custom tank volus
      tank_list = self.file_loader_tanks.file.get_bytes().decode()
      tank_list = tank_list.split('\r\n')
      tank_list.pop(0)
      tank_list.pop(-1)
      tank_list = [int(x) for x in tank_list]
      print(tank_list)

    if (self.pump.selected_value != "CSV File") and (self.tank.selected_value != "CSV File"):
      Q_solution, t_fill = anvil.server.call('anvilSolver', 
                                           float(self.rho.text), 
                                           float(self.L.text), 
                                           (float(self.D.text)/12),
                                           float(self.h_elevation.text),
                                           float(self.f.text),
                                           float(self.K_minor.text),
                                           float(self.LossVar.text),
                                           self.pump.selected_value,
                                           self.tank.selected_value)
    else:
      Q_solution, t_fill = anvil.server.call('anvilSolver_CSV', 
                                           float(self.rho.text), 
                                           float(self.L.text), 
                                           (float(self.D.text)/12),
                                           float(self.h_elevation.text),
                                           float(self.f.text),
                                           float(self.K_minor.text),
                                           float(self.LossVar.text),
                                           self.pump.selected_value,
                                           tank_list)

    result_dict = {}
    result_items = []
    
    if (self.pump.selected_value != "CSV File") and (self.tank.selected_value != "CSV File"):
      self.result_grid.visible = False
      if Q_solution:
        self.flow_rate_result.visible = True
        self.flow_rate_result.text = "Calculated Flow Rate = " + f"{Q_solution:.2f}" + " gpm"
      if t_fill:
        self.fill_time_result.visible = True
        self.fill_time_result.text = "Calculated Fill Time = " + f"{t_fill:.2f}" + " min"
    else:
      self.result_grid.visible = True
      self.flow_rate_result.visible = False
      for pump_name in list([self.pump.selected_value]):
        for j in range(len(tank_list)):
          result_dict['Pump'] = pump_name
          result_dict['Tank Volume (gal)'] = tank_list[j]
          result_dict['Flow Rate (gpm)'] = f"{Q_solution:.2f}"
          result_dict['Fill Time (min)'] = f"{t_fill[j]:.2f}"
          print(result_dict)
          result_items.append(result_dict)
    
          


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
  def send_feedback(name,email,topic,feedback):
    anvil.email.send(to="janetphan.work@gmail.com",
                     subject=f"Feedback from {name},",
                     text=f"""
                     {name} has sent feedback from the brine tank simulator regarding {topic}. Their message is as follows:
                     {feedback}
                     """)

  def file_loader_pumps_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    print(f"The file's content type is: {file.content_type}")
    print(f"The file's contents are: '{file.get_bytes()}'")

  def file_loader_tanks_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    print(f"The file's content type is: {file.content_type}")
    print(f"The file's contents are: '{file.get_bytes()}'")
