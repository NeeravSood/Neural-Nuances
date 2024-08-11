const { contextBridge, ipcRenderer } = require('electron');

// Expose a limited API to the renderer process
contextBridge.exposeInMainWorld('api', {
  runGame: (gamePath, enhancementOptions) => ipcRenderer.send('run-game', gamePath, enhancementOptions)
});
