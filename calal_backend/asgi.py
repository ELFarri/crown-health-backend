# =========================================================================
# CALAL BACKEND - ASGI (Asynchronous Server Gateway Interface) Configuration
# =========================================================================
"""
ASGI config for the Calal project.

It exposes the ASGI callable as a module-level variable named `application`.
This entry point is used by asynchronous web servers (like Uvicorn, Daphne, or Hypercorn)
to serve the application.

---------------------------------------------------------------------------
🎓 DEFENSE NOTES & CONCEPT EXPLANATIONS (Jury Q&A Prep)
---------------------------------------------------------------------------

1. WHAT IS ASGI?
   ASGI (Asynchronous Server Gateway Interface) is the modern standard for 
   Python web application development. It is the successor to WSGI (Web Server 
   Gateway Interface). While WSGI only supports synchronous request-response 
   flows, ASGI provides support for both synchronous and asynchronous protocols,
   including WebSockets, HTTP/2, and long-poll connections.

2. THE "RESTAURANT" ANALOGY (Easy way to explain this to the jury):
   
   - WSGI (Synchronous - Classical Web Server):
     Like a waiter in a traditional restaurant. A customer (the mobile app) 
     orders a meal. The waiter goes to the kitchen (database), waits for the 
     chef to cook it, brings it back, and leaves. The connection is closed. 
     If the customer wants a glass of water later, they must start all over 
     again by signaling the waiter, placing a new order, and waiting.
     
   - ASGI (Asynchronous - Modern WebSocket Server):
     Like a waiter who establishes a permanent "walkie-talkie" connection 
     between the table and the kitchen. The waiter doesn't stand waiting at 
     the table; they can manage 1000 tables simultaneously. If the kitchen 
     has an update (e.g., the AI coach pushes a new notification like 
     "Warning: You exceeded your calorie target!"), the kitchen can immediately 
     push it to the customer via the walkie-talkie in real-time, without 
     the customer having to request anything or refresh their screen.

3. WHY DO WE HAVE THIS FILE?
   Although the current Calal REST API prototype uses synchronous HTTP requests 
   (handled by WSGI), the inclusion of this ASGI configuration ensures that 
   the architecture is FUTURE-PROOF. It allows developers to easily scale the 
   app to support real-time features (like live chat WebSockets, instant push 
   notifications, or streaming AI tokens word-by-word) without changing the 
   framework base.
"""

import os
from django.core.asgi import get_asgi_application

# Step 1: Set the default Django settings module. 
# This tells the server to load settings from 'calal_backend.settings' (settings.py).
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calal_backend.settings')

# Step 2: Initialize the ASGI application callable.
# The server will call this 'application' variable to route asynchronous HTTP/WebSocket traffic.
application = get_asgi_application()

# =========================================================================
# END OF ASGI CONFIGURATION
# =========================================================================
