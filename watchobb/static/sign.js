// // to close the signin and open the signup
// function signup(){
//     let modal = document.getElementById('id01');
//     modal.style.display="none";
//     let modal2 = document.getElementById('id02');
//     modal2.style.display="block";
//   }

// let matchPass = function() {
//   let ps1 = document.getElementById('ps1').value;
//   let ps2 = document.getElementById('ps2').value;
//   if(!ps1){
//     document.getElementById('passHint').innerHTML = '';
//     document.getElementById("crtacc").disabled = true;
//   }else if (ps1 ==ps2) {
//     document.getElementById('passHint').style.color = 'green';
//     document.getElementById('passHint').innerHTML = 'Password matching';
//     document.getElementById("crtacc").disabled = false;
//   } else {
//     document.getElementById('passHint').style.color = 'red';
//     document.getElementById('passHint').innerHTML = 'Password not matching';
//     document.getElementById("crtacc").disabled = true;
//   }
//   if(ps1.length<8){
//     document.getElementById('passHint1').style.color = 'red';
//     document.getElementById('passHint1').innerHTML = 'Minimum 8 characters';
//     document.getElementById("ps2").disabled = true;
//   }else{
//     document.getElementById('passHint1').style.color = 'green';
//     document.getElementById("ps2").disabled = false;
//   }

// }

// function valName(name, id){
//   let regex = /^[a-zA-Z]+$/;
    
//   if(!regex.test(name)){
//     document.getElementById(id).innerHTML = 'Invalid Name'
//     document.getElementById("crtacc").disabled = true;
//   }else{
//     document.getElementById(id).innerHTML = '';
//     document.getElementById("crtacc").disabled = false;
//   }
// }

// function valPhone(number, id){
//   let regex = /^[\d]{10}$/
    
//   if(!regex.test(number)){
//     document.getElementById(id).innerHTML = 'Invalid Number'
//     document.getElementById("crtacc").disabled = true;
//   }else{
//     document.getElementById(id).innerHTML = '';
//     document.getElementById("crtacc").disabled = false;
//   }
// }

// const emailField = document.querySelector('#emailField');
// const feedback = document.querySelector('#emailH');
// const subm = document.querySelector('#crtacc');
// function valmail(emailVal) {
//   if(emailVal.length >0){
//     fetch("/authentication/validate-email", {
//       body: JSON.stringify({email:emailVal}),
//       method: "POST",
//     })
//     .then((res) => res.json())
//     .then((data) => {
//       console.log("data", data);
//       if(data.email_error){
//         subm.disabled = true;
//         feedback.innerHTML = 'E-mail already registered';
//       }
//     })
//   }
// }