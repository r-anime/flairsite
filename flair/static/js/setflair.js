
//alert("I am an alert box!");

//var checkBox = document.querySelector('input[type="checkbox"]');
//var textInput = document.querySelector('form-control').attr('required','required');
//document.querySelector('.form-control').attr('required');

//    alert(document.getElementById('trackerAccountName'));

function setAccountTrackerRequired(){
    document.getElementById('trackerAccountName').required = true;
}

function setAccountTrackerNotRequired(){
    document.getElementById('trackerAccountName').required = false;
}





//<input class="form-control" type="text" id="trackerAccountName" name="trackerAccountName"
//value="{{tracker_user_account_name}}" placeholder="e.g: https://myanimelist.net/animelist/[ThisUsername]" minlength="3" maxlength="20">
