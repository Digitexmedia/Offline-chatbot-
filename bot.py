const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const fs = require('fs');
const app = express();
const port = 5000;

const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: {
    headless: true,
    args: ['--no-sandbox']
  }
});

client.on('qr', (qr) => {
  qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
  console.log('✅ WhatsApp is ready.');
});

client.on('message', async msg => {
  const messageData = {
    from: msg.from,
    body: msg.body,
    isGroup: msg.from.endsWith('@g.us')
  };
  fs.writeFileSync('latest_message.json', JSON.stringify(messageData));
});

app.get('/send', async (req, res) => {
  const number = req.query.number;
  const message = req.query.message;

  if (number && message) {
    const chatId = number.includes('@c.us') ? number : `${number}@c.us`;
    client.sendMessage(chatId, message);
    res.send('✅ Message sent.');
  } else {
    res.send('❌ Missing number or message');
  }
});

app.get('/send-image', async (req, res) => {
  const number = req.query.number;
  const caption = req.query.caption || '';
  const chatId = number.includes('@c.us') ? number : `${number}@c.us`;

  const media = MessageMedia.fromFilePath('./profile.jpg');
  await client.sendMessage(chatId, media, { caption, sendMediaAsViewOnce: true });

  res.send('✅ View-once image sent.');
});

app.listen(port, () => {
  console.log(`📡 Control API running at http://localhost:${port}`);
});

client.initialize();
