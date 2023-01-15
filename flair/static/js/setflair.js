function setAccountTrackerRequired(){
    document.getElementById('trackerAccountName').required = true;
    document.getElementById('trackerAccountName').disabled = false;
}

function setAccountTrackerNotRequired(){
    document.getElementById('trackerAccountName').required = false;
    document.getElementById('trackerAccountName').disabled = true;
}


let delayTimer;
function searchGeneralFlairs(event) {
    clearTimeout(delayTimer);
    delayTimer = setTimeout(function () {
        const searchText = document.getElementById("search-box").value.toLowerCase();
        if (searchText.length > 1) {
            const flairList = document.querySelectorAll('.list-card-general');
            for (let flairCard of flairList) {
                const flairName = flairCard.dataset.flairName.toLowerCase();
                if (flairName.indexOf(searchText) !== -1) {
                    flairCard.style.display = 'flex';
                } else if (flairName !== "none") { // Always display "None" option
                    flairCard.style.display = 'none';
                }
            }
        } else {
            // Undo hiding everything from a search.
            const flairList = document.querySelectorAll('.list-card-general');
            for (let flairCard of flairList) {
                flairCard.style.display = 'flex';
            }
        }
    }, 300);
}

window.onload = function() {
    document.getElementById("search-box").value = '';
}