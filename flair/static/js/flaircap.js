const checks = document.querySelectorAll(".input-check");
const max = 2;
for (let i = 0; i < checks.length; i++){
  checks[i].onclick = selectiveCheck;
}
function selectiveCheck (event) {
  const checkedChecks = document.querySelectorAll(".input-check:checked");
    //if length is equal to max, this means we should grey out all other options
    if (checkedChecks.length === max){
        for (let i = 0; i < checks.length; i++){
            if(!checks[i].checked){
                checks[i].classList.add("greyout")
            }
        }
    }
    //if it's below max then we're back to normal, don't grey out anything
    if (checkedChecks.length < max){
        for (let i = 0; i < checks.length; i++){
            if(!checks[i].checked){
                checks[i].classList.remove("greyout")
            }
        }
    }

  // if we attempt to click a third flair, don't do anything
  if (checkedChecks.length >= max + 1){
      return false;
  }
    
}