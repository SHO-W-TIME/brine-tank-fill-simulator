import anvil.files
from anvil.files import data_files
import anvil.email
import anvil.users
import anvil.server

#Email service
@anvil.server.callable
def send_feedback(name, email, feedback):
    anvil.email.send(to="", 
                     subject=f"Feedback from {name},",
                     text=f"""
                     {name} has sent feedback from the brine tank simulator. To reply, send a message to their email {email}. Their message is as follows:
                     {feedback}
                     """)
