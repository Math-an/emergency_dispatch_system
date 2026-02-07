# emergency_dispatch_system


🚑 AI-Based Emergency dispatch Location Extraction System

An AI-powered system that extracts location and emergency details from unstructured text messages and converts them into map coordinates for faster emergency response.

📌 Problem Statement

Emergency messages are often unstructured and lack precise location details, causing delays in response time and manual interpretation errors.

💡 Proposed Solution

This system uses Natural Language Processing (NLP) to:

Extract street/locality from free-text messages

Detect emergency-related keywords

Convert extracted locations into latitude and longitude

Generate Google Maps directions for responders

Support human verification before dispatch

👥 Primary Users

Emergency response teams (police, ambulance, disaster management)

Control room operators

🚀 Key Features

AI-based location extraction (NER model)

Works with unstructured text messages

Automatic geocoding (latitude & longitude)

Google Maps direction link generation

Urgency keyword detection

Human-in-the-loop verification

🧠 Primary Innovation

Algorithm – NLP-based extraction of emergency and location data from free-text input.

📊 Data Type Used

Free-text emergency messages

Example:
"Accident in Velacherry near bus stand"

⚙️ Decision Logic

Receive emergency message

Extract location and emergency keywords

Assign urgency based on detected patterns

Convert location to coordinates

Generate map directions

Operator verifies before dispatch



🛠️ Technologies Used

Python

spaCy (NER model)

Geopy (Nominatim)

Google Maps URL API

