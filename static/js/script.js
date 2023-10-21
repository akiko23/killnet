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
    if (file) {
        result.innerHTML = `<div style="font-family: 'DM Sans', sans-serif;c">Файл загружен: ${file.name}</div>
        <div style="display: flex; justify-content: center; flex-direction: column; align-items: center; gap: 8px; margin-bottom: 20px;">
        <div class="container2">
            <div style="width: 850px;">
                <input type="checkbox" id="zoomCheck">
                <label for="zoomCheck">
                <img src="static/resources/old_data_graph.png"></img> 
                </label>
            </div>
            <div style="width: 850px;">
                <input type="checkbox" id="zoomCheck">
                <label for="zoomCheck">
                <img src="static/resources/old_data_graph.png"></img> 
                </label>
            </div>
        </div>
            
            
            <div class="button_download_img" style="margin-bottom: 30px;">
                <a href="static/resources/corrected_data.csv" class="button2" download>
                    <svg width="40px" height="40px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 3V16M12 16L16 11.625M12 16L8 11.625" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M15 21H9C6.17157 21 4.75736 21 3.87868 20.1213C3 19.2426 3 17.8284 3 15M21 15C21 17.8284 21 19.2426 20.1213 20.1213C19.8215 20.4211 19.4594 20.6186 19 20.7487" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </a>
            </span>
        </div>
            <span style="font-size: 24px; font-family: 'DM Sans', sans-serif;">
        </div>
        `;
    } else {
        result.innerHTML = "Файл не был загружен.";
    }
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


const dropContainer = document.getElementById("dropcontainer")
const fileInput = document.getElementById("fileInput")

  dropContainer.addEventListener("dragover", (e) => {
    // prevent default to allow drop
    e.preventDefault()
  }, false)

  dropContainer.addEventListener("dragenter", () => {
    dropContainer.classList.add("drag-active")
  })

  dropContainer.addEventListener("dragleave", () => {
    dropContainer.classList.remove("drag-active")
  })

  dropContainer.addEventListener("drop", (e) => {
    // e.preventDefault();
    console.log(e.dataTransfer.files)
    dropContainer.classList.remove("drag-active");
    fileInput.files = e.dataTransfer.files;

    if (fileInput.value) {
        submitButton.classList.add("enabled");
        submitButton.disabled = false;
    } else {
        submitButton.classList.remove("enabled");
        submitButton.disabled = true;
    }
  })
