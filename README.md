# Anonymous Telegram Bot 😶‍🌫️

### Bot that allows finding chat partners 🤖

### Bot Features 🤖
- **Find a Chat Partner:** Users can search for chat partners with the click of a button
- **Admin Commands:** Special commands for admins to send messages (to all users) and get user counts
- **Real-time Chat:** Connects users for instant messaging and allows users to leave chats whenever they want by typing /stop

### Getting started 🌠
You must have Python 3.* installed and get Telegram bot API key (you can get it from botfather in telegram)

### Installation 🌠
1. Clone the Repo: `git clone https://github.com/Agshin2004/anonymous_bot.git`
2. Set up venv: `python -m venv env`
3. Activate venv: `source env/bin/activate` (for linux/mac); Windows: `source env/Scripts/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Fill up API_KEY and ADMIN_ID with your data (I use Python Decouple library for seperating code and settings): `API_KEY=your_telegram_bot_api_key
ADMIN_ID=your_telegram_user_id`
6. Run bot `python bot.py`

### Main Bot Logic 🤖
**Start Command**: Initializes the user and presents them with options
**Special Mailing**: Admins can send a message to all users
**Count Command**: Admins can see how many users are registered
**Stop Command**: Ends the current chat for the user
**Message Handling**: Manages user interactions and connections

### Usage 🤖
**/start**: Starts the bot and adds the user to the database
**/special_mailing**: Allows the admin to send a message to all users
**/count**: Shows the admin the total number of users
**/stop**: Ends the current chat session
