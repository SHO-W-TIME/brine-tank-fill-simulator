from ._anvil_designer import SimulatorTemplate
from anvil import *
import anvil.server

class Simulator(SimulatorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  
  def calculate_click(self, **event_args):
    """This method is called when the button is clicked"""
    Q_solution, t_fill = anvil.server.call('anvilSolver',
                                           float(self.rho.text),
                                           float(self.L.text),
                                           float(self.D.text)/12,
                                           float(self.h_elevation.text),
                                           float(self.f.text),
                                           float(self.K_minor.text),
                                           float(self.LossVar.text),
                                           self.pump.selected_value,
                                           self.tank.selected_value)

    if Q_solution:
      self.flow_rate_result.visible = True
      self.flow_rate_result.text = "Calculated Flow Rate = " + str(Q_solution) + " gpm"

    if t_fill:
      self.fill_time_result.visible = True
      self.fill_time_result.text = "Calculated Fill Time = " + str(t_fill) + " min"

  def how_to_use_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def simulator_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def references_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def form_refreshing_data_bindings(self, **event_args):
    """This method is called when refresh_data_bindings is called"""
    pass

  def K_minor_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass
