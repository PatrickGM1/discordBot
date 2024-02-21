require('dotenv').config();
const { REST, Routes, Client, GatewayIntentBits } = require('discord.js');
const client = new Client({
  intents: [
      GatewayIntentBits.Guilds,
      //GatewayIntentBits.Guilds,
      GatewayIntentBits.GuildMembers,
      //GatewayIntentBits.GuildMessages,
      //GatewayIntentBits.MessageContent,
      // ...
  ]
})
const guildId = client.guilds.cache.get("YOUR_GUILD_ID");
const commands = [
  {
    name: 'hey',
    description: 'Replies with hey!',
  },
  {
    name: 'ping',
    description: 'Pong!',
  },
  {
    name: 'tabinet',
    description: 'Play a game!',
  },
];

const rest = new REST({ version: '10' }).setToken(process.env.TOKEN);

(async () => {
  try {
    console.log('Registering slash commands...');

    await rest.put(
      Routes.applicationCommands(
        process.env.clientId
      ),
      { body: commands }
    );
    console.log(process.env.clientId)
    console.log('Slash commands were registered successfully!');
  } catch (error) {
    console.log(`There was an error: ${error}`);
  }
})();