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

    if Q_solution:
      self.flow_rate_result.visible = True
      self.flow_rate_result.text = "Calculated Flow Rate = " + str(round(Q_solution, 2)) + " gpm"

    if t_fill:
      self.fill_time_result.visible = True
      self.fill_time_result.text = "Calculated Fill Time = " + str(round(t_fill, 2)) + " min"


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
    self.f.text = 0.02
    pass

  def LossVar_show(self, **event_args):
    """This method is called when the TextBox is shown on the screen"""
    self.LossVar.text = 0
    pass

  def rho_show(self, **event_args):
    """This method is called when the TextBox is shown on the screen"""
    self.rho.text = 64.1 #(Density of 23.3% salinity water)
    pass

# Contact Page
  def send_feedback(name,email,feedback):
    anvil.email.send(to="janetphan.work@gmail.com",
                     subject=f"Feedback from {name},",
                     text=f"""
                     {name} has sent feedback from the brine tank simulator."""
