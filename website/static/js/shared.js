// ---------------------------------------------------------------- //
// 以下為共用的function
// (大多數的檔案都有使用到的function)
// ---------------------------------------------------------------- //

// 取得今天日期
function getToday() {
    var today = new Date().toISOString().split('T')[0];
    return today;
}

// 設定日期欄位最大值為今天
function setTodayAsMaxDate(fieldId) {
    var today = getToday();
    var tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    var tomorrowISOString = tomorrow.toISOString().split('T')[0];
    document.getElementById(`${fieldId}`).setAttribute('max', tomorrowISOString);
}

// 檢查開始日期是否大於結束日期
function checkDate(start_date, end_date, delete_date_field, alert_text) {
    var startDate = new Date(document.getElementById(`${start_date}`).value);
    var endDate = new Date(document.getElementById(`${end_date}`).value);
    if (startDate != "" && endDate != "") {
        if (startDate > endDate) {
            alert(`${alert_text}`);
            document.getElementById(`${delete_date_field}`).value = "";
        }
    }
}

// 計算兩個日期的相差天數
function getDaysDifference(start_date, end_date) {
    var _start_date = new Date(document.getElementById(`${start_date}`).value);
    var _end_date = new Date(document.getElementById(`${end_date}`).value);

    if (_start_date != "" && _end_date != "") {
        var timeDifference = _end_date - _start_date;
        var daysDifference = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
        return daysDifference;
    }
}

// 顯示密碼
function showPassword(buttonName) {
    document.getElementById(`${buttonName}Password`).type = "text";
    var eyeButton = document.getElementById(`${buttonName}_eyeButton`);
    eyeButton.setAttribute("onclick", `hiddenPassword('${buttonName}')`);
    eyeButton.innerHTML = '<i class="fa-regular fa-eye-slash"></i>';
}

// 隱藏密碼
function hiddenPassword(buttonName) {
    document.getElementById(`${buttonName}Password`).type = "password";
    var eyeButton = document.getElementById(`${buttonName}_eyeButton`);
    eyeButton.setAttribute("onclick", `showPassword('${buttonName}')`);
    eyeButton.innerHTML = '<i class="fa-regular fa-eye"></i>';
}

// 設定modal關閉時清空form
function clearModal(modalName, fromName) {
    var modal = document.getElementById(modalName);
    var form = document.getElementById(fromName);
    modal.addEventListener('hidden.bs.modal', function (event) {
        // form回到初始狀態
        form.reset();
    })
}

// 新增row到table
function addRowForTable(_tableId, _mid, _name, _num, mode) {
    var table = document.getElementById(`${_tableId}`);
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
    cell1.innerHTML = table.rows.length;
    cell2.innerHTML = _mid;
    cell3.innerHTML = _name;
    cell4.innerHTML = _num;
    if (mode == "staff") {
        cell5.innerHTML = `<button type='button' class='btn' id='deleteStaff_${table.rows.length}_btn' onclick='deleteStaff("${_mid}", "${_name}", "${_num}")'><i class='fa-solid fa-trash-can'></i></button>`;
    } else if (mode == "participant") {
        cell5.innerHTML = `<button type='button' class='btn' id='deleteParticipant_${table.rows.length}_btn' onclick='deleteParticipant("${_mid}", "${_name}", "${_num}")'><i class='fa-solid fa-trash-can'></i></button>`;
    }
}

// 刪除table中的所有row
function deleteAllRowForTable(_tableId) {
    var table = document.getElementById(`${_tableId}`);
    // 刪除所有的row
    for (var i = table.rows.length - 1; i > 0; i--) {
        table.deleteRow(i); // 從最後一行開始刪
    }
    if (table.rows.length > 0) {
        table.deleteRow(0);
    }
}

// 取得member_id並存進Field
function getMemberToField(_fieldId, _list) {
    var temp = [];
    for (var i = 0; i < _list.length; i++) {
        temp.push(_list[i].mid);
    }
    document.getElementById(`${_fieldId}`).value = JSON.stringify(temp);
}