let tg = Telegram.WebApp;

tg.ready();
tg.expand();

function setThemeClass() {
    document.documentElement.className = tg.colorScheme;
}

tg.onEvent('themeChanged', setThemeClass);
setThemeClass();

function webviewClose() {
    tg.close();
}

tg.MainButton
    .setText('CLOSE')
    .show()
    .onClick(function () {
        webviewClose();
    });