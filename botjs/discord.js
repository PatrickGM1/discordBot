// Initialize dotenv
require('dotenv').config();


// Discord.js versions ^13.0 require us to explicitly define client intents
const { REST, Routes, Client, GatewayIntentBits, SlashCommandBuilder } = require('discord.js')
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
const rest = new REST({ version: '10' }).setToken(process.env.TOKEN);
  
  client.on('ready', (c) => {
    console.log(`✅ ${c.user.tag} is online.`);
  });
  
  client.on('interactionCreate', (interaction) => {
    if (!interaction.isChatInputCommand()) return;
  
    if (interaction.commandName === 'hey') {
      return interaction.reply('hey!');
    }
  
    if (interaction.commandName === 'ping') {
      return interaction.reply('Pong!');
    }
    if (interaction.commandName == 'tabinet'){
      const filter = m => m.author.id ===  message.author.id;
        message.channel.awaitMessages(filter, {
        max: 1, // leave this the same
        time: 10000, // time in MS. there are 1000 MS in a second
          }).then(async(collected) => {
            if(collected.first().content == 'cancel'){
            message.reply('Command cancelled.')
        } 
        console.log('collecred :' + collected.first().content)
        }).catch(() => {
            // what to do if a user takes too long goes here 
        message.reply('You took too long! Goodbye!') 
        });
    }
  });
// Log In our bot
client.login(process.env.TOKEN);