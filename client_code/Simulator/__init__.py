from ._anvil_designer import SimulatorTemplate
from anvil import *
import anvil.server


class Simulator(SimulatorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def pump_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def tank_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def rho_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def text_area_1_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def L_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass
