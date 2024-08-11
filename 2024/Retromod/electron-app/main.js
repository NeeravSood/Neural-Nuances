const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { execFile, spawn } = require('child_process');

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            sandbox: true // Enable sandboxing for security
        }
    });

    win.loadFile('index.html');
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// Handling game execution with emulator
ipcMain.on('run-game', (event, gamePath, enhancementOptions) => {
    const emulatorPath = path.join(__dirname, 'emulator', 'emulator.exe');
    const args = [gamePath, '--enhance', JSON.stringify(enhancementOptions)];

    const gameProcess = spawn(emulatorPath, args, { stdio: 'inherit' });

    gameProcess.on('close', (code) => {
        console.log(`Game process exited with code ${code}`);
    });
});

// Error handling
process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
    dialog.showErrorBox('Error', 'An unexpected error occurred. Please try again.');
});
