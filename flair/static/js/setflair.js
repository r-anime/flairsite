function setAccountTrackerRequired(){
    document.getElementById('trackerAccountName').required = true;
    document.getElementById('trackerAccountName').disabled = false;
}

function setAccountTrackerNotRequired(){
    document.getElementById('trackerAccountName').required = false;
    document.getElementById('trackerAccountName').disabled = true;
}
