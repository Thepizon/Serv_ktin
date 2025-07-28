document.addEventListener("DOMContentLoaded", () => {
    const start_btn = document.getElementById("on");
    start_btn.addEventListener("click", () => {
        fetch("/wol", { method: "POST" })
            .then(response => response.text())
            .then(msg => alert(msg))
            .catch(err => alert("Erreur: " + err));
    });
});


function updateStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            const state = document.getElementById('status');
            state.textContent = data.status;
        });
}
function updateVPN() {
    fetch('/vpn')
        .then(response => response.json())
        .then(data => {
            const state = document.getElementById('vpn');
            state.textContent = data.status;
        })
 }

 function updateCPU() {
    fetch('/cpu')
        .then(response => response.json())
        .then(data => {

            const temp = document.getElementById('cpu');
            temp.textContent = data.status
        })
        .catch(err => {
            // Erreur silencieuse, rien ne s'affiche ni ne change
            console.warn("Erreur CPU (probablement PC éteint) :", err);
            const temp = document.getElementById('cpu');
            temp.textContent = "...";
        });
 }
  function updateRAM() {
    fetch('/ram')
        .then(response => response.json())
        .then(data => {

            const temp = document.getElementById('ram');
            temp.textContent = data.status
        })
        .catch(err => {
            // Erreur silencieuse, rien ne s'affiche ni ne change
            console.warn("Erreur CPU (probablement PC éteint) :", err);
        });
 }
setInterval(updateStatus, 5000);
setInterval(updateVPN, 5000);
setInterval(updateCPU, 1000);
setInterval(updateRAM, 1000);
window.onload = updateStatus;
window.onload = updateVPN;