displayView = function(){
    // the code required to display a view
    // If the token exists in local storage, then display the profile view directly
    if (localStorage.getItem("token") == null) {
        document.getElementById("startpage").innerHTML = document.getElementById("welcomeview").innerHTML;
    }else{
        document.getElementById("startpage").innerHTML = document.getElementById("profileview").innerHTML;
        // Once the user leaves a tab for a while and comes back to it, the data in the tab shall be
        // preserved without asking the server stub again.
        loadPersonalProfile();
        retrieveMsg('home');
	
    }
}

window.onload =function(){
    displayView();
}

signInWebSocket = function(){
    currentEmail = localStorage.getItem("email");
    currentToken = localStorage.getItem("token");
    ws = new WebSocket("ws://" + document.domain + ":5000/websoc");
    var signInUser = {
        "email" : currentEmail,
        "token" : currentToken
    }
    // Connect and send the email and token to the websocket
    ws.onopen = function(){
        ws.send(JSON.stringify((signInUser)));
    }

    // Receive the message from the websocket
    ws.onmessage = function (message) {
		if (message.data == "SignOut"){
            localStorage.removeItem("token");
            localStorage.removeItem("email");
            displayView();
        }
        
                
    };
}

signInValidator = function(form){
 
    // Mandatory Check 
    if (mandatoryCheck(form.email.value) == false){
        document.getElementById("errormsgSignIn").innerHTML = "Please type your email.";
        return false;
    }

    if (emailFormatCheck(form.email.value) == false){
        document.getElementById("errormsgSignIn").innerHTML = "Please type valid email address.";
        return false;
    }

    if (mandatoryCheck(form.passwordSignIn.value) == false){
        document.getElementById("errormsgSignIn").innerHTML = "Please type your password.";
        return false;
    }

    // If the signup failed, return false until the user enters correct information
    
    var signInForm = {
        "email": form.email.value.trim(),
        "password": form.passwordSignIn.value.trim()
    }

    var con = new XMLHttpRequest();
    con.open("POST",'/signin',true);
    
    con.onreadystatechange = function(){
        if (con.readyState == 4){
            var responseMsg = JSON.parse(con.responseText);
            if (con.status==200){
                // If signin successfully, then it should direct to the profile view
                // Save the email and token to local storage
                localStorage.setItem("token",responseMsg.data);
				localStorage.setItem("email",form.email.value);
                displayView();
                // Connect ws and trigger auto-signout checking
				signInWebSocket(); 
            } else {
                document.getElementById('errormsgSignIn').innerHTML = responseMsg.message;
                return false;
            }
        }
    }

    con.setRequestHeader("Content-Type", "application/json");
    con.send(JSON.stringify(signInForm));
    return false;

}

signUpValidator = function(form){

    // Get the form data
    var userEmail = form.email.value;
    var userPW = form.passwordSignUp.value;
    var userFirstName = form.firstname.value;
    var userFamilyName = form.familyname.value;
    var userGender = form.gender.value;
    var userCity = form.city.value;
    var userCountry = form.country.value;
    var pw1 = form.passwordSignUp.value;
    var pw2 = form.repeatPSW.value;

    //Mandatory Check
    if (mandatoryCheck(userFirstName) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type your first name.";
        return false;
    }

    if (mandatoryCheck(userFamilyName) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type your family name.";
        return false;
    }

    if (mandatoryCheck(userGender) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please select your gender.";
        return false;
    }

    if (mandatoryCheck(userCity) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type your city.";
        return false;
    }

    if (mandatoryCheck(userCountry) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type your country.";
        return false;
    }

    if (mandatoryCheck(userEmail) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type your email.";
        return false;
    }

    if (emailFormatCheck(userEmail) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type valid email address.";
        return false;
    }

    if (mandatoryCheck(pw1) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type your password.";
        return false;
    }

    if (mandatoryCheck(pw2) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please confirm your password.";
        return false;
    }


    // Password Validation (Min length and same password in confirmation field)
    if (pwValidator(pw1,pw2,'errormsgSignUp') == false) {
        return false;
    }
    
    var signUpForm = {
        "email": userEmail.trim(),
        "password": pw1.trim(),
        "firstname": userFirstName.trim(),
        "familyname": userFamilyName.trim(),
        "gender": userGender.trim(),
        "city": userCity.trim(),
        "country": userCountry.trim()

    }

    var con = new XMLHttpRequest();
    con.open("POST",'/signup',true);
    
    con.onreadystatechange = function(){
        if (con.readyState == 4){
            var responseMsg = JSON.parse(con.responseText);
            if (con.status == 200){
                document.getElementById('errormsgSignUp').innerHTML= responseMsg.message;
                document.getElementById('loginmsg').innerHTML = "You may try your first login.";
                form.reset();
            } else {
                clearMsg('loginmsg');
                document.getElementById('errormsgSignUp').innerHTML= responseMsg.message;
            }
        }
    }

    con.setRequestHeader("Content-Type", "application/json");
    con.send(JSON.stringify(signUpForm));
    return false;
}

// Check if the input is empty or not
mandatoryCheck = function(value){
    if (value == "" || value == " ")
        return false;
    return true;
}

// Check if the email is in correct format
// Format should be XXXX@XXXX
emailFormatCheck = function(value){
    if (value.indexOf("@") > 0 && value.indexOf("@") < value.length-1)
        return true;
    return false;
}


pwValidator = function(password1, password2,errorMsgID){

    if (pwLengthCheck(password1) == false)
    {
        // Display error message
        document.getElementById(errorMsgID).innerHTML = "The password should have at least 8 characters.";
        return false;
    }
    else{
        if (pwIsSame(password1,password2) == false){
            document.getElementById(errorMsgID).innerHTML = "The password must be the same.";
            return false;
        }
    }
    return true;
}

// Check if the password satisfies the minimum length of characters
pwLengthCheck = function(password){
    var minLength = 8;
    if (password.length < minLength) {
        return false;
    }
    return true;
}

// Check if the passwords in "Password" and "Repeat PSW" are the same
pwIsSame = function(password1, password2){
    if (password1 == password2) {
        return true;
    }
    else{
        return false;
    }
}

//Change Password function in Account Tab
changePassword = function(form){

    var oldPW = form.oldPW.value;
    var newPW = form.newPW.value;
    var confirmPW = form.confirmPW.value;

    if (mandatoryCheck(oldPW) == false){
        document.getElementById("errormsgPW").innerHTML = "Please type your old password.";
        return false;
    }

    if (mandatoryCheck(newPW) == false){
        document.getElementById("errormsgPW").innerHTML = "Please type your new password.";
        return false;
    }

    if (mandatoryCheck(confirmPW) == false){
        document.getElementById("errormsgPW").innerHTML = "Please confirm your password.";
        return false;
    }

    // Validate the password before send to server
    // Minimum length and same string in new password and confirm password fields
    if (pwValidator(newPW,confirmPW,'errormsgPW') == false){
        return false;
    }

    // Not allow to change password with same password
    if (oldPW == newPW){
        document.getElementById("errormsgPW").innerHTML = "New password cannot be as same as old password.";
        return false;
    }


    // if pass all validations, send to server and request for password change
    var currentToken = localStorage.getItem("token");

    var pwForm = {
        "token": currentToken,
        "oldPassword": oldPW,
        "newPassword": newPW
    }

    var con = new XMLHttpRequest();
    con.open("POST",'/changePassword',true)

    con.onreadystatechange = function(){
        if (con.readyState == 4){
            var responseMsg = JSON.parse(con.responseText);
            if (con.status==200){
                form.reset();
            }
            document.getElementById("errormsgPW").innerHTML = responseMsg.message;
        }
    }

    con.setRequestHeader("Content-Type", "application/json");
    con.send(JSON.stringify(pwForm));


    return false;

}

// Sign out function in Account Tab
signOut = function(){
    var currentToken =  localStorage.getItem("token");

    var con = new XMLHttpRequest();
    con.open("POST",'/signout',true);

    con.onreadystatechange = function(){
        if (con.readyState == 4){
            var responseMsg = JSON.parse(con.responseText);
            if (con.status==200){
                localStorage.removeItem("token");
				localStorage.removeItem("email");
                displayView();
            }
        }
    }

    con.setRequestHeader("Content-Type", "application/json");
    con.send(JSON.stringify({"token":currentToken}));

}


// Display the selected tab by changing the class name
// call this function once click the tab button
selectTab = function(event, tabName){
    var tabcontent, tabbutton;

    // Reset the page content to none 
    tabcontent = document.getElementsByClassName("tabcontent");
    for (var i=0; i<tabcontent.length;i++){
        tabcontent[i].style.display = "none";
    }
    
    // Display the correct content according to which tab is selected
    document.getElementById(tabName).style.display="block";

    // Reset all class names to "tab"
	tabbutton = document.getElementsByClassName("tab");
	for (var i=0; i<tabbutton.length;i++){
	    tabbutton[i].className = "tab"
	}

    // Set the class name for selected tab to "tab active"
    // Also use for marking which tab is selected
	event.className = "tab active"
}

// Extract and display the personal information of current user in home tab
loadPersonalProfile = function(){

    var currentToken = localStorage.getItem("token");
    var con = new XMLHttpRequest();
    con.open("GET",'/getUserDataByToken/'+currentToken,true)

    con.onreadystatechange = function(){
        if (con.readyState == 4){
            var response = JSON.parse(con.responseText);
            if (con.status == 200){
                var data = response.data;
                document.getElementsByName("home_personalInfo_email")[0].innerHTML = data[0]['email'];
                document.getElementsByName("home_personalInfo_firstname")[0].innerHTML = data[0]['firstname'];
                document.getElementsByName("home_personalInfo_familyname")[0].innerHTML = data[0]['familyname'];
                document.getElementsByName("home_personalInfo_gender")[0].innerHTML = data[0]['gender'];
                document.getElementsByName("home_personalInfo_city")[0].innerHTML = data[0]['city'];
                document.getElementsByName("home_personalInfo_country")[0].innerHTML = data[0]['country'];
            }
        }
    };

    con.send(null);
}

// Post message in home and browse tab
// The parameter "tab" is used to determine the location to store the message 
// Current user: use the token to store in the current user profile
// Other user: according to the email displayed in the personal information, store the message in that user profile
postMsg = function(tab, form){
	var currentToken = localStorage.getItem("token");
    var email;

    if (tab == "home"){
        email = document.getElementsByName("home_personalInfo_email")[0].innerHTML;
    } else {
        email = document.getElementsByName("email_otherUser")[0].innerHTML;
    }    
    
    var msg = form.postArea.value.trim();
	var con = new XMLHttpRequest();

    con.open ("POST",'/postMsg', true);
    con.onreadystatechange = function(){
        if (con.readyState == 4){
            var response = JSON.parse(con.responseText);
            if (con.status == 200){
               form.reset();
               retrieveMsg(tab); 
            } 
            document.getElementById("errormsgPostWall_"+tab).innerHTML = response.message;
        }
    };

    var msgForm = {
        "token": currentToken,
        "toEmail": email,
        "content": msg
    }

    con.setRequestHeader("Content-Type", "application/json");
    con.send(JSON.stringify(msgForm));

	return false;
}

// Retrieve the message from user profile and display on the message wall
// Call this function when clicking the refresh button and after new message is posted
retrieveMsg = function(tab){

    var con = new XMLHttpRequest();
    var currentToken = localStorage.getItem("token");

    if (tab == "home"){
        con.open("GET",'/getUserMessagesByToken/'+currentToken,true);

        con.onreadystatechange = function(){
            if (con.readyState == 4){
                var responseMsg = JSON.parse(con.responseText);
                if (con.status==200){

                    var allMsg = responseMsg.data;
                    document.getElementById("msgWall").innerHTML = "";
                    for (var i=allMsg.length-1; i>=0;i--){
                        document.getElementById("msgWall").innerHTML += "<div class= \"row\">"+"From: " + allMsg[i].fromemail + "</div>" ;
                        document.getElementById("msgWall").innerHTML += "<div class= \"msgBorder row\">" + allMsg[i].content + "</div>" + "<div class= \"row\"></div>"; 
                    }
                } 
            }
        };
        con.send(null);
    } else {
        
        document.getElementById("msgWall_browse").innerHTML = "";
        var email = document.getElementsByName("email_otherUser")[0].innerHTML;
        con.open("GET",'/getUserMessagesByEmail/'+currentToken+"/"+email,true);

        con.onreadystatechange = function(){
            if (con.readyState == 4){
                var responseMsg = JSON.parse(con.responseText);
                if (con.status==200){

                    var allMsg = responseMsg.data;
                    document.getElementById("msgWall_browse").innerHTML = "";
                    for (var i=allMsg.length-1; i>=0;i--){
                        document.getElementById("msgWall_browse").innerHTML += "<div class= \"row\">"+"From: " + allMsg[i].fromemail + "</div>" ;
                        document.getElementById("msgWall_browse").innerHTML += "<div class= \"msgBorder row\">" + allMsg[i].content + "</div>" + "<div class= \"row\"></div>";
                    }
                } 
            }
        };
        con.send(null);
    }
}

// Search user function in browse tab
searchUser = function(form){

    var con = new XMLHttpRequest();
    var email = form.searchEmail.value;
    var currentToken = localStorage.getItem("token");

    con.open("GET",'/getUserDataByEmail/'+currentToken+"/"+email,true);

    con.onreadystatechange = function(){
        if (con.readyState == 4){
            var responseMsg = JSON.parse(con.responseText);
            if (con.status==200){
                clearMsg("errorMsgSearch");
                //Display user information
                //Overwrite the existing personal information
                var data = responseMsg.data[0];
                document.getElementById("personalInfo_browse").innerHTML = "";
                document.getElementById("personalInfo_browse").innerHTML += "<h3>Personal Information</h3>";
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><label>Email: </label><div id=\"email_otherUser\" name=\"email_otherUser\">" + data['email'] + "</div></div>";
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><label>First Name: </label>" + data['firstname'] + "</div>";
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><label>Family Name: </label>" + data['familyname'] + "</div>";
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><label>Gender: </label>" + data['gender'] + "</div>";
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><label>City: </label>" + data['city'] + "</div>";
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><label>Country: </label>" + data['country'] + "</div>";

                //Display the message wall
                document.getElementById("msgWallDisplay").innerHTML = document.getElementById("msgwallcontent").innerHTML;

                // Display the message on the wall
                retrieveMsg('browse');

                // Clear the search field
                form.reset();
                // Clear the feedback for the post area if necessary
                clearMsg('errormsgPostWall_browse');

            } else {
                document.getElementById("errorMsgSearch").innerHTML = responseMsg.message;
            }
        }
    };
    con.send(null);
    return false;
}

// Clear the feedback from the server after posted a message
// Call this function:
// Home tab: when user focuses on the textarea again after posted a message
// Browse tab: 
// 1. When user focuses on the textarea again after posted a message
// 2. Search another user
clearMsg = function(eleID){
    document.getElementById(eleID).innerHTML = "";
}





