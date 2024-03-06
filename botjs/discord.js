// Load environment variables from .env file
require('dotenv').config();

// Import necessary classes and objects from discord.js library
const { REST, Routes, Client, GatewayIntentBits, SlashCommandBuilder } = require('discord.js');

// Initialize a new Discord client with specified intents
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds, // Necessary for interacting with guilds (servers)
        //GatewayIntentBits.Guilds, // Duplicate line, might be a mistake or placeholder for other intents
        GatewayIntentBits.GuildMembers, // Necessary for interacting with guild members
        //GatewayIntentBits.GuildMessages, // Commented out, used for receiving messages in guilds
        //GatewayIntentBits.MessageContent, // Commented out, required for receiving message content
        // ... Add more intents as needed
    ]
});

// Listen for messages sent in any channel the bot has access to
client.on('message', (message) => {
  // Ignore messages from bots to prevent potential infinite loops or spam
  if (message.author.bot) return false;

  // Check if the message starts with the "!say" command
  if (message.content.toLowerCase().startsWith('!say')) {
    console.log("Command detected: !say");
    // Ensure there is at least one mentioned member in the message
    if (!message.mentions.members.size) return false;
    // Reply in the channel with a playful message targeting the mentioned member
    message.channel.send(`${message.mentions.members.first()} is a son of a cookie`);
  }
});

// Placeholder for your guild ID
const guildId = client.guilds.cache.get("YOUR_GUILD_ID");
// Initialize REST client for interacting with Discord API
const rest = new REST({ version: '10' }).setToken(process.env.TOKEN);

// Log when the bot is successfully logged in and set up
client.on('ready', (c) => {
  console.log(`Bot is online: ${c.user.tag}`);
});

// Handle slash command interactions
client.on('interactionCreate', (interaction) => {
  // Ignore non-command interactions
  if (!interaction.isChatInputCommand()) return;

  // Respond to the "hey" command
  if (interaction.commandName === 'hey') {
    return interaction.reply('hey!');
  }

  // Respond to the "ping" command
  if (interaction.commandName === 'ping') {
    return interaction.reply('Pong!');
  }

  // Placeholder for a potential "tabinet" command
  if (interaction.commandName == 'tabinet'){
    // Command logic here
  }
});

// Log the bot in using the token from .env file
client.login(process.env.TOKEN);
