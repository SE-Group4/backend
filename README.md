# StudBud Chat Application

This is a chat application built with Django that allows users to join group chats and send private messages to other users.

## Tech Stack
- Django Restframework
- Channels
- Websocket
- Django restframework redis

## Features
- Users can create an account and log in.
- Users can join or create a group chat and send messages to all participants in the group.
- Users can send private messages to other users.
- Users can view a list of all the active group chats and the participants in each chat.
- Users can view their own message history in group chats and private messages.
- Users can upload files and images in group chats.

## Installation
1. Clone this repository: `git clone https://github.com/your-username/backend.git`.
2. Change into the project directory: `cd backend`.
3. Create a virtual environment: `python3 -m venv env`.
4. Activate the virtual environment: `source env/bin/activate` (on Unix-based systems) or `env\Scripts\activate` (on Windows).
5. Install the project dependencies: `pip install -r requirements.txt`.
6. Create a database: `python manage.py migrate`.
7. Create a superuser: `python manage.py createsuperuser`.
8. Start the development server: `python manage.py runserver`.

## Usage
1. Navigate to http://localhost:8000 in your web browser.
2. Log in or create an account if you haven't already.
3. From the home page, you can view a list of all the active group chats and the participants in each chat.
4. To join a group chat, click on its name in the list.
5. To create a new group chat, click the "Create New Group Chat" button and enter a name and description for the chat.
6. To send a private message to another user, click on their name in the list of users or search for them using the search bar.
7. To upload a file or image in a group chat, click the "Attach File" button and select the file or image from your computer.

## Contributing
If you'd like to contribute to this project, please fork the repository and create a new branch for your feature or bug fix. Then, submit a pull request with your changes for review.
