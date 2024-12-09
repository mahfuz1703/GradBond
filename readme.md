# GradBond - An alumni finder web application
## Introduction
### GradBond is a web application that connects alumni with current students, fostering networking, mentorship, and resource sharing. It aims to build a supportive community where students gain insights and opportunities, and alumni stay engaged. 

## Features
* User Authentication
    * <strong>Registration:</strong> Users can create an account with required details
    * <strong>Login/Logout:</strong> Secure login system using Django's authentication framework.
* Find Alumni
    * <strong>Search Feature:</strong> Users can search for alumni by name, batch, department, profession, or company.
    * <strong>Filter Options:</strong> Filters to narrow search results for better usability.
    * <strong>Profile View:</strong> Users can view alumni profiles for information
* Events/Workshops
    * <strong>Event Creation:</strong> Alumni can organize workshops or events and post details like title, date, description, and registration links.
    * <strong>Event Browsing:</strong> Users can view upcoming and past events.
* User Profile Management
    * <strong>Profile Update:</strong> Users can edit their personal information, upload a profile picture, and update contact details.
    * <strong>Public/Private Info:</strong> Controls for users to decide what information to make visible to others.

## System Requirements
* Server Requirements
    * Python 3.12.3+
    * Django 5.1+
    * SQLite3
* Client Requirements
    * A modern web browser (e.g., Chrome, Firefox, Edge)
    * Internet connection

## Installation and Setup
* Create and Activate a Virtual Environment
    ```bash
    python -m venv env_name
    source env_name/bin/activate # On Windows: env\Scripts\activate 
    deactivate # when complete work then use this for deactive virtual environment
    ```
* Clone the Repository
    ```bash
    git clone https://github.com/mahfuz1703/GradBond.git # clone project when you are activated your virtual environment
    ```
* Goto project directory
    ```bash
    cd GradBond/backend
    ```
* Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```
* Set Up the Database
    ```bash
    python manage.py makemigrations  
    python manage.py migrate  
    ```
* Run the Development Server
    ```bash
    python manage.py runserver   
    ```

## API Endpoints (Usage Instructions)
* Authentication
    * <strong>/auth/signin/:</strong> User login
    * <strong>/auth/signout/:</strong> User logout
    * <strong>/auth/signup/:</strong> User registration
* Alumni Search
    * <strong>/find-alumni/:</strong> Find alumni page
    * <strong>/search-alumni/:</strong> Search alumni
* Events
    * <strong>/events/:</strong> Show all events
    * <strong>/event-detail/<event_id>/:</strong> Details of a specific event
    * <strong>/add-event/:</strong> Add event only by an alumni
    * <strong>/edit-event/<event_id>/:</strong> Edit specific event
    * <strong>/delete-event/<event_id>/:</strong> Delete specific event
* Profile
    * <strong>/profile/:</strong> View user profile
    * <strong>/update-profile/:</strong> Edit user profile

## Future Enhancements
* <strong>Real-time Chat:</strong> Enable direct messaging between alumni and students.
* <strong>News feeds:</strong> Comprehensive news feeds where user shares their daily technology and job related updates
* <strong>Admin Dashboard:</strong> Comprehensive admin controls for managing users, events, and content.
* <strong>Advanced Analytics:</strong> Insights into alumni activities and user engagement.
* <strong>Mobile App:</strong> Extend GradBond’s functionality to Android and iOS.


### Thank you for visit repository