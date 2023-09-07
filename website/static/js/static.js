function getToday() {
    var today = new Date().toISOString().split('T')[0];
    return today;
}

function setTodayAsMaxDate(fieldId) {
    // 設定日期欄位最大值為今天
    var today = getToday();
    var tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    var tomorrowISOString = tomorrow.toISOString().split('T')[0];
    document.getElementById(`${fieldId}`).setAttribute('max', tomorrowISOString);
}

function showPassword(buttonName) {
    document.getElementById(`${buttonName}Password`).type = "text";
    var eyeButton = document.getElementById(`${buttonName}_eyeButton`);
    eyeButton.setAttribute("onclick", `hiddenPassword('${buttonName}')`);
    eyeButton.innerHTML = '<i class="fa-regular fa-eye-slash"></i>';
}

function hiddenPassword(buttonName) {
    document.getElementById(`${buttonName}Password`).type = "password";
    var eyeButton = document.getElementById(`${buttonName}_eyeButton`);
    eyeButton.setAttribute("onclick", `showPassword('${buttonName}')`);
    eyeButton.innerHTML = '<i class="fa-regular fa-eye"></i>';
}