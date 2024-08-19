from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Debugging

handler = Debugging()
controller = Controller(handler, hostname='localhost', port=8025)
controller.start()

print("SMTP server running on localhost:8025...")
try:
    input("Press Enter to stop the server.\n")
finally:
    controller.stop()
