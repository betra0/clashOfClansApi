const {Client, Events, ActionRowBuilder, ButtonBuilder, ButtonStyle, EmbedBuilder, Embed} = require('discord.js');
const axios = require('axios');
const findAndEditMessageText = require('./services/findAndEditMessageText');
const generateRegister = require('./other/generateRegister');

require('dotenv').config({ path: '../../.env' });


const client = new Client({
    intents:process.env.INTENTSDS
});
const token = process.env.BOTDSTOKEN
const handlerReqireCommand = (carpeta, arg, message)=>{
  try{
    const command = require(`./${carpeta}/${arg}`)
    command.run(message)
  }catch(e){
    console.log(e)
  }

}


const donationsRankingTask = async () => {
    const channelIdRankingDonate = '1326100799800999939'; // Reemplaza con el ID del canal
    const messageIdRankingDonate = '1326102556979499074'; // Reemplaza con el ID del mensaje
    const channelIdLogsDonate='1326428017257353216'
    const messageIdLogsDonate='1326428211311284245'

    try {
                
        const URL = `http://${process.env.APIHOST}:${process.env.APIPORT}/members`
        console.log(URL)
        let response;
        try {
            response = await axios.get(URL);
            if (response.status !== 200 || !response.data) {
                throw new Error('Respuesta inválida de la API');
            }
        } catch (err) {
            console.error('Error al obtener los miembros del clan de la api:', err);
            return;
        }
        // member is object or dictionary
        const members = response.data.members;
        // doantionLogs is a list or array
        const donationLogs = response.data.donationLogs;
        

        // Ordenar los miembros por 'accumulatedDonations' en orden descendente
        const sortedMembers = Object.values(members).sort((a, b) => b.accumulatedDonations - a.accumulatedDonations);
        // Construir el mensaje con hora y dia 
        let newMessage = `   ≫ ───────≪•◦Última actualización: ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()} UTC ◦•≫ ─────── ≪\n`;
        newMessage += '**                               ≫ Ranking de donaciones del clan ≪:**\n';
        let i = 1;
        for (const member of sortedMembers) {
            if (member.accumulatedDonations === 0) break;
            newMessage += `•◦ ${i} •◦ ★ ${member.username}  Donaciones: ${member.accumulatedDonations}\n`;
            i++;
        }
        newMessage += '   ≫ ─────── ≪•◦ ❈ ◦•≫ ─────── ≪'
        
        if (newMessage.length > 2000) {
            newMessage = newMessage.slice(-1999); // Mantener los últimos 2000 caracteres
          }
        await findAndEditMessageText(client, channelIdRankingDonate, messageIdRankingDonate, newMessage);

        const embeds = generateEmbedsLogs({membersDict: members, logsDonationList: donationLogs})
        await findAndEditMessageText(client, channelIdLogsDonate, messageIdLogsDonate, {content: '' ,embeds: embeds});
        

    } catch (err) {
        console.error('Error al editar el mensaje:', err); 
    }
};


const audioTask2 = async () => {
    console.log('Esta tarea se ejecuta cada x tiempo.');

    const idVoiceChannel = '842217117393747988'; // ID del canal de voz

    try {
        const voiceChannel = client.channels.cache.get(idVoiceChannel);
        if (!voiceChannel) throw new Error('El canal de voz no existe o no es válido.');

        const newName = `Actualizado: ${new Date().toLocaleTimeString()}`;
        const updatedChannel = await voiceChannel.setName(newName, { reason: 'Actualización automática' });

        if (updatedChannel) {
            console.log(`Nombre cambiado a: ${updatedChannel.name}`);
        }

        // Obtener información de límite de tasa
        const headers = updatedChannel?.rateLimitPerUser || updatedChannel?.lastMessage?.rateLimitHeaders;

        if (headers) {
            console.log(`Límite: ${headers['x-ratelimit-limit']}`);
            console.log(`Restantes: ${headers['x-ratelimit-remaining']}`);
            console.log(`Se reinicia en: ${new Date(headers['x-ratelimit-reset'] * 1000)}`);
            console.log(`Tiempo hasta el reinicio: ${headers['x-ratelimit-reset-after']} segundos`);
        }

    } catch (err) {
        console.error('Ocurrió un error al cambiar el nombre del canal:', err);

        // Errores específicos
        if (err.code === 50013) {
            console.log('El bot no tiene permisos para cambiar el nombre del canal.');
        } else if (err.code === 10003) {
            console.log('El canal no existe o ha sido eliminado.');
        } else if (err.response && err.response.status === 429) {
            // Manejo específico para rate limit excedido
            const retryAfter = err.response.data.retry_after;
            console.log(`Excediste el límite de tasa. Espera ${retryAfter} segundos antes de intentar nuevamente.`);
        } else {
            console.log('Error desconocido:', err);
        }
    }
};

const generateEmbedsLogs = ({membersDict={}, logsDonationList={}})=>{
    const MAX_LOGS = 9;
    if (!membersDict || !logsDonationList) throw new Error('No se han proporcionado los datos necesarios.');
    const donationLogs = [...logsDonationList];
    // Verifica si el array supera el límite
    if (donationLogs.length > MAX_LOGS) {
      // Elimina los elementos más antiguos (los primeros)
      donationLogs.splice(-1 * (donationLogs.length - MAX_LOGS));
    }
    let embeds = []
    const TitleEmbed = new EmbedBuilder()
        .setColor('#0099ff')
        .setTitle(`≫ ───────≪•◦Registro donaciones del clan•◦≫ ───────≪`)
        .setDescription('Este es el registro de las ultimas donaciones del clan')
        .setTimestamp()
    embeds.push(TitleEmbed)

    let n=1
    for (const log of donationLogs.reverse()){
        let embed=generateRegister({ members:membersDict, NRegistro: n, logMembers: log.members });
        if (embed)
            embeds.push(embed)
            n++

    }
    return embeds
}


const exampleTask = async () => {
    const channelIdLogsDonate='1325969560372903999'
    const messageIdLogsDonate='1326973197417189397'
    const URL = `http://${process.env.APIHOST}:${process.env.APIPORT}/members`
        console.log(URL)
        let response;
        try {
            response = await axios.get(URL);
            if (response.status !== 200 || !response.data) {
                throw new Error('Respuesta inválida de la API');
            }
        } catch (err) {
            console.error('Error al obtener los miembros del clan de la api:', err);
            return;
        }

    const members = response.data.members;
    // doantionLogs is a list or array
    const donationLogs = response.data.donationLogs;
    const embeds = generateEmbedsLogs({membersDict: members, logsDonationList: donationLogs})
    await findAndEditMessageText(client, channelIdLogsDonate, messageIdLogsDonate, {content: '' ,embeds: embeds});
/*     const targetChannelId = '1327107443666452563'; 
    const channel = client.channels.cache.get(targetChannelId);

        if (channel) {
            // Envía un mensaje al canal
            channel.send({
              content: '',
              embeds: embeds,  
            
            });
        } else {
            console.log('Canal no encontrado.');
        } */



}

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}`);

    // Espera 10 segundos antes de ejecutar por primera vez
    setTimeout(() => {
        donationsRankingTask(); // Ejecuta la función después del retraso

        // Programa la ejecución repetitiva cada 2 minutos (120,000 ms)
        setInterval(donationsRankingTask, 1000 * 60 * 1,5);
    }, 4000); 
      // Revisa si ya existe una iteración activa
    

        
        

        /* setTimeout(() => {
            exampleTask(); // Ejecuta la función después del retraso
            
        }, 1000)
         */


});

client.on(Events.MessageCreate, async message => {
    console.log('Message received:', message.guildId, message.content, message.channelId);
    if (!message.guild) {
          return message.reply('Este comando solo puede ser usado en un servidor de Discord.');
    }
    if (message.content.startsWith('sudo')) {


          if (message.author.bot) return
          if (message.member && !message.member.permissions.has('ADMINISTRATOR')) {
              return message.reply('¡Solo los administradores pueden ejecutar este comando!');
          }
        
           // Handler comannd
          const arg = message.content.slice(5).split(' ')[0]
          if(arg === 'create'){
            const arg = message.content.slice(5).split(' ')[1]
            console.log(arg)
            handlerReqireCommand('createCommands', arg, message)
          }
          else{
            console.log(arg)
            handlerReqireCommand('adminCommands', arg, message)
          }
          


    }
    if (message.content.startsWith('%')){
      if (message.author.bot) return
      const arg = message.content.slice(1).split(' ')[0]
      console.log(arg)
      handlerReqireCommand('commands', arg, message)
    }
    
    

});

client.login(token); 