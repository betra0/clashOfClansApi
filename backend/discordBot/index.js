const {Client, Events, MessageActivityType} = require('discord.js');
const axios = require('axios');


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
    const channelId = '1326100799800999939'; // Reemplaza con el ID del canal
    const messageId = '1326102556979499074'; // Reemplaza con el ID del mensaje

    try {
        // Obtener el canal
        const channel = await client.channels.fetch(channelId);

        // Verificar si el canal existe y es de texto
        if (channel && channel.isTextBased()) {
            // Obtener el mensaje
            const message = await channel.messages.fetch(messageId);
            if (!message) {
                console.log('El mensaje no existe o ya fue eliminado.');
                return;
            }
            const URL = `http://${process.env.APIHOST}:${process.env.APIPORT}/members`
            console.log(URL)
            const response = await axios.get(URL);
            if (response.status !== 200 || !response.data) {
                throw new Error('Respuesta inválida de la API');
            }
            

            const members = response.data.members;

            // Ordenar los miembros por 'accumulatedDonations' en orden descendente
            const sortedMembers = Object.values(members).sort((a, b) => b.accumulatedDonations - a.accumulatedDonations);
            
            // Construir el mensaje con hora y dia 
            let newMessage = `   ≫ ───────≪•◦Última actualización: ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()} ◦•≫ ─────── ≪\n`;
            newMessage += '**                               ≫ Ranking de donaciones del clan ≪:**\n';
            let i = 1;
            for (const member of sortedMembers) {
                if (member.accumulatedDonations === 0) break;
                newMessage += `•◦ ${i} •◦ ★ ${member.username}  Donaciones: ${member.accumulatedDonations}\n`;
                i++;
            }
            newMessage += '   ≫ ─────── ≪•◦ ❈ ◦•≫ ─────── ≪'
            
            // Editar el mensaje con la hora actual
            await message.edit(newMessage);
            
            console.log('Mensaje editado correctamente.');
        } else {
            console.log('El canal no es válido o no es de texto.');
        }
    } catch (err) {
        console.error('Error al editar el mensaje:', err);

        if (err.code === 50001) {
            console.log('El bot no tiene permisos para ver los mensajes en este canal.');
        } else if (err.code === 10008) {
            console.log('El mensaje no existe o ya fue eliminado.');
        } else {
            console.log('Error desconocido:', err);
        }
    }
};

const intervalTask = () => {
    
    const idClan = '842217117151264778'
    const idChannel = '842217117151264780'
    const idMessage='1325979566690533428'

    const channel = client.channels.cache.get(idChannel); 
    if (channel) {
        channel.send('¡Este es un mensaje programado cada 2 minutos!');
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




client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}`);

    // Espera 10 segundos antes de ejecutar por primera vez
    setTimeout(() => {
        donationsRankingTask(); // Ejecuta la función después del retraso

        // Programa la ejecución repetitiva cada 2 minutos (120,000 ms)
        setInterval(donationsRankingTask, 1000 * 60 * 2);
    }, 10000); // 10,000 ms = 10 segundos

    /* setInterval(audioTask2, 1000*60*1); */

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