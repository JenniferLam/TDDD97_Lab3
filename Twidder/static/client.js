/*
TDDD97 Project Assignment
Created by Jennifer Lam and Vlad Buga 
Last Updated on 13 Mar 2018
*/

// Store the websocket
var ws;

// D3 visualization
var graph_numPost;
var graph_numUsers;
var graph_view;

// Template rendering for displaying message wall
var source_msgwall;
var template_msgwall;
var source_welcome;
var template_welcome;
var source_profile;
var template_profile;

// Implement before close the browser
window.onbeforeunload = function(){
    currentEmail = localStorage.getItem("email");
    currentToken = localStorage.getItem("token");

    var closeBrowse = {
        "type": "unload",
        "email": currentEmail,
        "token": currentToken
    }
    // Inform server to update the total no. of online users
    ws.send(JSON.stringify(closeBrowse));
    ws.close();
}

window.onload =function(){
    compileTemplate();
    loadWebSoc();
}

compileTemplate = function() {
    // Display the latest message on th wall
    Handlebars.registerHelper('reverse', function (arr) {
        arr.reverse();
    });
    
    Handlebars.registerHelper('ifEquals', function(arg1, arg2, options) {
        return (arg1 == arg2) ? options.fn(this) : options.inverse(this);
    });
    
    // Compile the templates 
    source_msgwall   = document.getElementById("msgDisplay_template").innerHTML;
    template_msgwall = Handlebars.compile(source_msgwall);
    source_welcome = document.getElementById("welcomeview").innerHTML;
    template_welcome = Handlebars.compile(source_welcome);
    source_profile = document.getElementById("profileview").innerHTML;
    template_profile = Handlebars.compile(source_profile);
}

/* For live data presentation, 
    1. No. of posts per user: display total number of posts of current user
    2. No. of online users: display the number of online users
    If the user just closes the browser instead of sign out properly,
    the user will not be considered as online users
    3. No. of views per profile: 
    display the number of users to search the current user's profile

    createWebSoc() supports the live data presentation
    by sending and receiving messages through websocket
*/
createWebSoc = function(json) {

    // Connect and send the email and token to server
    // json is from sign in websocket
    ws.onopen = function(){
        ws.send(JSON.stringify((json)));
    }
    
    // Receive the message from the websocket
    ws.onmessage = function (message) {
        message = JSON.parse(message.data);

        // Inform the client side to sign out
		if (message.type == "autoSignOut" && message.value == "SignOut"){
            localStorage.removeItem("token");
            localStorage.removeItem("email");
            displayView();
            ws.close();
        } 

        // Update total count of online users
        if (message.type == "updateUserCnt"){
			updateGraph(graph_numUsers, message.value, message.total);
        }

        // Update no. of posts
        if (message.type == "postMsg"){
			updateGraph(graph_numPost, message.value, message.total);
        }

        // Update no. of views
        if (message.type == "updateUserView"){
			updateGraph(graph_view, message.value, message.total);
        }
                
    };
    
    ws.onclose = function() {};
}

/*  
    After close and reopen browser, 
    check if the token in local storage is valid or not.
    If invalid, remove the token and email in local storage 
    and then redirect to welcome view.
*/
loadWebSoc = function(){
    token = localStorage.getItem("token");
    email = localStorage.getItem("email");
    if ( token != null) {
        var con = new XMLHttpRequest();

        con.open("GET",'/getUserDataByToken/'+token,true);

        con.onreadystatechange = function(){
            if (con.readyState == 4){
                var response = JSON.parse(con.responseText);
                if (con.status == 200){
                        // This will implement when refresh the browser
                        ws = new WebSocket("ws://" + document.domain + ":5000/websoc");
                        var reload = {
                            "type":"reload",
                            "email": email,
                            "token": token
                        }
                        createWebSoc(reload);
                    } else {
                        // This will implement when user closes the browser
                        // and signs in again in another browser
                        localStorage.removeItem('token');
                        localStorage.removeItem('email');
                }
            }
        };
        con.send(null);
    }
    displayView();

}

// Determine which view (welcome or profile) should be displayed
displayView = function(){
    
    token = localStorage.getItem("token");
    // When the token does not exist, display welcome view, otherwise, profile view
    if ( token == null) {
        document.getElementById("container").innerHTML = template_welcome(template_data);
        //document.getElementById("container").innerHTML = document.getElementById("welcomeview").innerHTML;
    }else{        
        //document.getElementById("container").innerHTML = document.getElementById("profileview").innerHTML;
        document.getElementById("container").innerHTML = template_profile(template_data);
        ;
		// Load the D3 graph
        setupGraph();
        loadPersonalProfile();
        retrieveMsg('home');
    }
}

// Create the websocket once the user signs in 
signInWebSocket = function(){
    currentEmail = localStorage.getItem("email");
    currentToken = localStorage.getItem("token");
    ws = new WebSocket("ws://" + document.domain + ":5000/websoc");
    
    var signInUser = {
        "type": "signin",
        "email" : currentEmail,
        "token" : currentToken
    }
    createWebSoc(signInUser);
    
}

/*
    User allows to drag the message and drop it to the textarea
    Usually for replying others' messages
*/
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("fromemail", ev.toElement.getElementsByClassName("fromemail_msg")[0].innerText);
    ev.dataTransfer.setData("content", ev.toElement.getElementsByClassName("content_msg")[0].innerText);
}

function drop(ev) {
    ev.preventDefault();
    var fromemail = ev.dataTransfer.getData("fromemail");
    fromemail = fromemail.replace(":","");
    var content = ev.dataTransfer.getData("content");
    ev.target.value += ">>>" + fromemail + ": " + content + "\n";
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

// Handle password validation
pwValidator = function(password1, password2,errorMsgID){

    if (pwLengthCheck(password1) == false)
    {
        // Display error message
        document.getElementById(errorMsgID).innerHTML = "The password should have at least 8 characters.";
        // Error message effect
        $("#"+errorMsgID).parent().effect("bounce", {times:3}, 300);
        return false;
    }
    else{
        if (pwIsSame(password1,password2) == false){
            document.getElementById(errorMsgID).innerHTML = "The password must be the same.";
            // Error message effect
            $("#"+errorMsgID).parent().effect("bounce", {times:3}, 300);
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

// Handle signin validation and request
signInValidator = function(form){
 
    // Mandatory Field Check 
    if (mandatoryCheck(form.email.value) == false){
        document.getElementById("errormsgSignIn").innerHTML = "Please type your email.";
		$("#errormsgSignIn").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    // Check the email format
    if (emailFormatCheck(form.email.value) == false){
        document.getElementById("errormsgSignIn").innerHTML = "Please type valid email address.";
		$("#errormsgSignIn").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    if (mandatoryCheck(form.passwordSignIn.value) == false){
        document.getElementById("errormsgSignIn").innerHTML = "Please type your password.";
		$("#errormsgSignIn").parent().effect("bounce", {times:3}, 300);
        return false;
    }

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
                signInWebSocket(); 
                displayView();
            } else {
                document.getElementById('errormsgSignIn').innerHTML = responseMsg.message;
				// Error message effect
                $("#errormsgSignIn").parent().effect("bounce", {times:3}, 300);
                return false;
            }
        }
    }

    con.setRequestHeader("Content-Type", "application/json");
    con.send(JSON.stringify(signInForm));
    return false;

}

// Handle signup validation and request
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
		$("#errormsgSignUp").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    if (mandatoryCheck(userFamilyName) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type your family name.";
		$("#errormsgSignUp").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    if (mandatoryCheck(userGender) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please select your gender.";
		$("#errormsgSignUp").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    if (mandatoryCheck(userCity) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type your city.";
		$("#errormsgSignUp").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    if (mandatoryCheck(userCountry) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type your country.";
		$("#errormsgSignUp").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    if (mandatoryCheck(userEmail) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type your email.";
		$("#errormsgSignUp").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    // Check the email format
    if (emailFormatCheck(userEmail) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type valid email address.";
		$("#errormsgSignUp").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    if (mandatoryCheck(pw1) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please type your password.";
		$("#errormsgSignUp").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    if (mandatoryCheck(pw2) == false){
        clearMsg('loginmsg');
        document.getElementById("errormsgSignUp").innerHTML = "Please confirm your password.";
		$("#errormsgSignUp").parent().effect("bounce", {times:3}, 300);
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
				// Error message effect
                $("#errormsgSignUp").parent().effect("bounce", {times:3}, 300);
            }
        }
    }

    con.setRequestHeader("Content-Type", "application/json");
    con.send(JSON.stringify(signUpForm));
    return false;
}

// Change Password function in Account Tab
changePassword = function(form){

    var oldPW = form.oldPW.value;
    var newPW = form.newPW.value;
    var confirmPW = form.confirmPW.value;

    if (mandatoryCheck(oldPW) == false){
        document.getElementById("errormsgPW").innerHTML = "Please type your old password.";
		$("#errormsgPW").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    if (mandatoryCheck(newPW) == false){
        document.getElementById("errormsgPW").innerHTML = "Please type your new password.";
		$("#errormsgPW").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    if (mandatoryCheck(confirmPW) == false){
        document.getElementById("errormsgPW").innerHTML = "Please confirm your password.";
		$("#errormsgPW").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    // Validate the password before sending to server
    // Minimum length and same string in new password and confirm password fields
    if (pwValidator(newPW,confirmPW,'errormsgPW') == false){
        return false;
    }

    // Not allow to change password with same password
    if (oldPW == newPW){
        document.getElementById("errormsgPW").innerHTML = "New password cannot be as same as old password.";
		$("#errormsgPW").parent().effect("bounce", {times:3}, 300);
        return false;
    }

    // If pass all validations, send to server and request for password change
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
                // Clear the user input
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
    var currentToken = localStorage.getItem("token");
    var currentEmail = localStorage.getItem("email");
    var con = new XMLHttpRequest();
    con.open("POST",'/signout',true);

    con.onreadystatechange = function(){
        if (con.readyState == 4){
            var responseMsg = JSON.parse(con.responseText);
            if (con.status==200){
                var signOut = {
                    "type": "signout",
                    "email": currentEmail,
                    "token": currentToken
                }
                ws.send(JSON.stringify(signOut));

                // Update the no. of views if the user searched someone before sign out
                // Get the email address displayed in browse tab and exclude it in the count
                var email_browser = document.getElementsByName("email_otherUser")[0];
                if (email_browser) { email_browser = document.getElementsByName("email_otherUser")[0].innerHTML;}
                else {email_browser == "";}
                if (email_browser != ""){
                    var updateview = {
                        "type": "updateuserview",
                        "value": "signout",
                        "email": email_browser,
                        "token": currentToken
                    }
                    ws.send(JSON.stringify(updateview));
                }

                localStorage.removeItem("token");
                localStorage.removeItem("email");
                displayView();
                ws.close();
            }
        }
    }

    con.setRequestHeader("Content-Type", "application/json");
    con.send(JSON.stringify({"token":currentToken}));

}


// Display the selected tab by changing the class name
// Call this function once click the tab button
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

    // To hide the navigation bar menu after click on a tab
	if ($("#quickNavBar:visible").is(":visible")){
		$(".navbar-toggler").click();
	}
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
                // Update live data
				updateGraph(graph_numPost, response.NumOfPost, response.TotalOfPost);
                for (int i =0; i<personalInfo_home_name.length;i++;){
                    document.getElementsByName(personalInfo_home_name[i])[0].innerHTML = template_profile()

                }


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

/* 
    Handle post message implementation
    The parameter "tab" is to determine which implementation should be used
    The email address is extracted from UI
*/
postMsg = function(tab, form){
	var currentToken = localStorage.getItem("token");
    var email;

    // Get the email address from UI
    if (tab == "home"){
        email = document.getElementsByName("home_personalInfo_email")[0].innerHTML;
    } else {
        email = document.getElementsByName("email_otherUser")[0].innerHTML;
    }    
    
    var msg = form.postArea.value.trim();
    // Not allow to post empty message
    if (msg == ""){
        document.getElementById("errormsgPostWall_"+tab).innerHTML = "Your message is empty.";
        return false;
    }

	var con = new XMLHttpRequest();

    con.open ("POST",'/postMsg', true);
    con.onreadystatechange = function(){
        if (con.readyState == 4){
            var response = JSON.parse(con.responseText);
            if (con.status == 200){
               form.reset();
               retrieveMsg(tab); 
               // Update the number of posts
               var postMsg = {
                    "type": "postMsg",
                    "email": email,
                    "token": currentToken
               }
               ws.send(JSON.stringify(postMsg));
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
                    // Apply template to display the message
                    var allMsg = responseMsg.data;
					document.getElementById("msgWall").innerHTML = template_msgwall(allMsg);
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
                    // Apply template to display the message
                    var allMsg = responseMsg.data;
                    document.getElementById("msgWall_browse").innerHTML = template_msgwall(allMsg);
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

    // Update the number of views
    /*
        Reduce the number of views when the user searches another user profile
    */
    var previousEmail = document.getElementsByName("email_otherUser")[0];
    if (previousEmail){
        previousEmail = previousEmail.innerHTML;
    } else {
        previousEmail = "null";
    }

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
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><div class=\"col-md-12\"><h3 class=\"title\">Personal Information</h3></div></div>";
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><div class=\"col-md-3\"><label>Email: </label></div><div class=\"col-md\"><div id=\"email_otherUser\" name=\"email_otherUser\">" + data['email'] + "</div></div></div>";
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><div class=\"col-md-3\"><label>First Name: </label></div><div class=\"col-md\">" + data['firstname'] + "</div></div>";
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><div class=\"col-md-3\"><label>Family Name: </label></div><div class=\"col-md\">" + data['familyname'] + "</div></div>";
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><div class=\"col-md-3\"><label>Gender: </label></div><div class=\"col-md\">" + data['gender'] + "</div></div>";
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><div class=\"col-md-3\"><label>City: </label></div><div class=\"col-md\">" + data['city'] + "</div></div>";
                document.getElementById("personalInfo_browse").innerHTML += "<div class=\"row\"><div class=\"col-md-3\"><label>Country: </label></div><div class=\"col-md\">" + data['country'] + "</div></div>";

                //Display the message wall
                document.getElementById("msgWallDisplay").innerHTML = document.getElementById("msgwallcontent").innerHTML;

                // Display the message on the wall
                retrieveMsg('browse');

                // Clear the search field
                form.reset();

                // Clear the feedback for the post area if necessary
                clearMsg('errormsgPostWall_browse');

                // Send message to update no. of views
                var searchUser = {
                    "type": "updateuserview",
                    "value": "search",
                    "email": email,
                    "previousEmail": previousEmail,
                    "token": currentToken
                }
                ws.send(JSON.stringify(searchUser));

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





