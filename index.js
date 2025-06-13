const { exec } = require("child_process");
const path = require("path");

console.log("🟢 Starting the WhatsApp Chatbot System...");

// Start server.js
const serverProcess = exec("node server.js", (error, stdout, stderr) => {
  if (error) {
    console.error(`❌ server.js error: ${error.message}`);
    return;
  }
  if (stderr) console.error(`⚠️ server.js stderr: ${stderr}`);
  console.log(`📡 server.js output: ${stdout}`);
});

// Start bot.py
const botProcess = exec("python3 bot.py", (error, stdout, stderr) => {
  if (error) {
    console.error(`❌ bot.py error: ${error.message}`);
    return;
  }
  if (stderr) console.error(`⚠️ bot.py stderr: ${stderr}`);
  console.log(`🤖 bot.py output: ${stdout}`);
});

// Listen for exit
serverProcess.on("exit", code => console.log(`server.js exited with code ${code}`));
botProcess.on("exit", code => console.log(`bot.py exited with code ${code}`));
