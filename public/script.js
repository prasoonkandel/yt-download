const BASE_URL = "http://127.0.0.1:5000";
let mp3API = `${BASE_URL}/api/mp3`;
let data = null;

async function fetchMp3(url) {
  api_url = mp3API;
  try {
    const response = await fetch(api_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: url }),
    });
    data = await response.json();
    console.log(data);
  } catch (error) {
    console.error("Error fetching MP3 URL:", error);
    data = { error: `Error fetching MP3 URL: ${error.message}` };
  }
  if (data.error) {
    showError(data.error || "Unknown error occurred");
    return;
  }

  if (!data.download || !data.preview) {
    showError("Unknown Error Occurred");
    return;
  }

  const downloadUrl = BASE_URL + data.download;
  const previewUrl = BASE_URL + data.preview;

  window.folder_id = data.folder_id;

  showDownload(downloadUrl, data.filename);
  showPreview(previewUrl, "audio/mpeg");
}

function showDownload(link, filename) {
  const downloadLink = document.getElementById("download_link");
  const formContainer = document.getElementById("form_container");

  formContainer.style.display = "none";

  downloadLink.innerHTML = `<a href="${link}" download="${filename}"><i class="fa-solid fa-download"></i>&nbsp; Download MP3</a>`;
}
function showPreview(link, type) {
  const preview = document.getElementById("preview_audio");
  const formContainer = document.getElementById("form_container");

  formContainer.style.display = "none";
  preview.innerHTML = `<audio src="${link}" type="${type}" controls></audio>`;
}
function showError(message) {
  const downloadLink = document.getElementById("download_link");
  const formContainer = document.getElementById("form_container");
  formContainer.style.display = "none";
  downloadLink.innerHTML = `<div id="error_message">
    <span><i class="fa-solid fa-circle-exclamation"></i>&nbsp; ${message}</span>
    <button type="button" id="retry_button" onclick="location.reload()">
      <i class="fa-solid fa-arrow-rotate-right"></i>&nbsp; Try Again
    </button>
  </div>`;
}

let form = document.querySelector("form");

form.addEventListener("submit", (e) => {
  const formContainer = document.getElementById("form_container");
  const downloadLink = document.getElementById("download_link");
  e.preventDefault();
  const url = document.getElementById("url_mp3").value.trim();

  if (!url) {
    showError("Please enter a valid YouTube URL");
    return;
  }
  formContainer.style.display = "none";
  downloadLink.innerHTML = `<p>Processing...</p>`;
  fetchMp3(url);
});

window.addEventListener("beforeunload", () => {
  if (!window.folder_id) return;

  const url = `${BASE_URL}/api/cleanup/${window.folder_id}`;

  navigator.sendBeacon(url);
});
