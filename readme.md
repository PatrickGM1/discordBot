# 🤖 Discord Bot
A simple yet powerful Discord bot with basic commands to enhance your server experience.

## 🚀 Features
- 🎉 Basic commands (hi, milmoi, guess)
- 🛠 Moderation commands (kick, warn, ban, mute, unmute)
- 🎭 Role management (automatic role assignment, mute/unmute)
- 📜 Logging system
- 🎮 Fun commands (coinflip, roll, rps)
- 📊 Information commands (userinfo, serverinfo)

## 📦 Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/PatrickGM1/bot.git
   cd discordBot/code
   ```

2. Install dependencies:
   ```sh
   pip install -r code/requirements.txt
   ```

3. Set up your `.env` file:
   ```env
   DISCORD_BOT_TOKEN=your-bot-token
   ```

4. Run the bot:
   ```sh
   python bot.py
   ```

## 🛠 Commands

### User Commands
| Command      | Description |
|--------------|-------------|
| `/hi`        | Greets the user. |
| `/milmoi`    | Sends a friendly greeting. |
| `/guess`     | Play a number game. |
| `/coinflip`  | Flips a coin. |
| `/roll`      | Rolls a dice. |
| `/rps`       | Play Rock Paper Scissors. |
| `/balance`   | Shows your current balance. |
| `/daily`     | Collect your daily reward. |
| `/pay`       | Pay another user. Usage: /pay @user [amount] |
| `/gamble`    | Gamble your balance. Usage: /gamble [amount] |
| `/slots`     | Play a slot machine game. Usage: /slots [amount] |
| `/userinfo`  | Displays user information. Usage: /userinfo @user |
| `/serverinfo`| Displays server information. |
| `/work`      | Work and earn money. |

### Admin Commands
| Command              | Description |
|----------------------|-------------|
| `/kick`              | Kicks a user from the server. Usage: /kick @user [reason] |
| `/warn`              | Warns a user. Usage: /warn @user [reason] |
| `/ban`               | Bans a user from the server. Usage: /ban @user [reason] |
| `/mute`              | Mutes a user. Usage: /mute @user |
| `/unmute`            | Unmutes a user. Usage: /unmute @user |
| `/setFunds`          | Set a user's balance. |
| `/setWelcomeMessage` | Set a custom welcome message. |
| `/setWelcomeRole`    | Set a role to assign to new members. |
| `/setWelcomeChannel` | Set the channel for welcome messages. |
| `/removeWelcomeRole` | Remove the assigned welcome role. |
| `/toggleWelcome`     | Enable or disable welcome messages. |
| `/resetWelcomeSettings` | Reset all welcome settings for this server. |
| `/setLeaveMessage`   | Set a custom leave message. |
| `/setLeaveChannel`   | Set the channel for leave messages. |
| `/toggleLeaveMessage`| Enable or disable leave messages. |

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

🚀 **Enjoy using the bot? Give this repo a star!** ⭐

🔗 **GitHub Repository:** [PatrickGM1/bot](https://github.com/PatrickGM1/bot)