const { ipcRenderer } = require('electron');

document.getElementById('run-game-btn').addEventListener('click', () => {
    const gameFile = document.getElementById('game-file').files[0];
    if (gameFile) {
        const enhancementOptions = {
            graphics: document.getElementById('enhance-graphics').checked,
            sound: document.getElementById('enhance-sound').checked,
            npc: document.getElementById('enhance-npc').checked
        };

        ipcRenderer.send('run-game', gameFile.path, enhancementOptions);
    } else {
        alert('Please select a game file to run.');
    }
});
