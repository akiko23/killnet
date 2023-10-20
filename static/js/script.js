function enableSubmit() {
    var fileInput = document.getElementById("fileInput");
    var submitButton = document.getElementById("submitButton");
    if (fileInput.value) {
        submitButton.classList.add("enabled");
        submitButton.disabled = false;
    } else {
        submitButton.classList.remove("enabled");
        submitButton.disabled = true;
    }
}

document.getElementById("uploadForm").addEventListener("submit", function(e) {
    e.preventDefault();

    var result = document.getElementById("result");
    var fileInput = document.getElementById("fileInput");

    var file = fileInput.files[0];
    if (file) {
        result.innerHTML = "Файл загружен: " + file.name;
    } else {
        result.innerHTML = "Файл не был загружен.";
    }

    // Очистить поле выбора файла
    fileInput.value = "";

    // Скрыть кнопку отправить
    var submitButton = document.getElementById("submitButton");
    submitButton.classList.remove("enabled");
    submitButton.disabled = true;
    

    // Send file on backend api
    var data = new FormData()
    data.append('file', file)
    
    sendFileOnBackend("http://localhost:8000/sendfile", data)
});


async function sendFileOnBackend(url = "", data = {}) {
    await fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "no-cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
        "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: "follow", // manual, *follow, error
        referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: data, // body data type must match "Content-Type" header
    });
}