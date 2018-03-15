var template_data = {
	signin: [
		 {
		   "label": "Email",
		   "type": "text",
		   "name": "email",
		   "id": "signin_email"
		 },
		 {
		   "label": "Password",
		   "type": "password",
		   "name": "passwordSignIn",
		   "id": "signin_pw"
		 }
	],
    signup: [
		 {
		   "label": "First Name",
		   "tag": "input",
		   "type": "text",
		   "name": "firstname",
		   
		},
		 {
		   "label": "Family Name",
		   "tag": "input",
		   "type": "text",
		   "name": "familyname",
		   
		},
		 {
		   "label": "Gender",
		   "tag": "select",
		   "name": "gender",
		   "value": [
		      "",
		      "Male",
		      "Female"
		   ]
		},
		 {
		   "label": "City",
		   "tag": "input",
		   "type": "text",
		   "name": "city",

		},
		 {
		   "label": "Country",
		   "tag": "input",
		   "type": "text",
		   "name": "country",
		},
		 {
		   "label": "Email",
		   "tag": "input",
		   "type": "text",
		   "name": "email",
		   "id": "signup_email",
		},
		 {
		   "label": "Password",
		   "tag": "input",
		   "type": "password",
		   "name": "passwordSignUp",
		},
		 {
		   "label": "Repeat PSW",
		   "tag": "input",
		   "type": "password",
		   "name": "repeatPSW",
		}
    ],
    navBar: [
		 {
		   "class": "tab active",
		   "onclick": "home",
		   "id": "tab_home",
		   "value": "Home"
		 },
		 {
		   "class": "tab",
		   "onclick": "browse",
		   "id": "tab_browse",
		   "value": "Browse"
		 },
		 {
		   "class": "tab",
		   "onclick": "account",
		   "id": "tab_account",
		   "value": "Account"
		 }
	],
	graph : [
		 {
		   "id": "graph_numPost",
		   "value": "No. of Posts"
		 },
		 {
		   "id": "graph_numUsers",
		   "value": "No. of Users Online"
		 },
		 {
		   "id": "graph_view",
		   "value": "No. of Views"
		 }
	],
	personalInfo_home : [
		 {
		   "label": "Email",
		   "name": "home_personalInfo_email"
		 },
		 {
		   "label": "First Name",
		   "name": "home_personalInfo_firstname"
		 },
		 {
		   "label": "Family Name",
		   "name": "home_personalInfo_familyname"
		 },
		 {
		   "label": "Gender",
		   "name": "home_personalInfo_gender"
		 },
		 {
		   "label": "City",
		   "name": "home_personalInfo_city"
		 },
		 {
		   "label": "Country",
		   "name": "home_personalInfo_country"
		 }
	],
	personalInfo_browse: [
		 {
		   "label": "Email",
		   "name": "email_otherUser",
		   "id": "email_otherUser"
		 },
		 {
		   "label": "First Name"
		 },
		 {
		   "label": "Family Name"
		 },
		 {
		   "label": "Gender"
		 },
		 {
		   "label": "City"
		 },
		 {
		   "label": "Country"
		 }
	],
	changePW = [
		 {
		   "label": "Old Password",
		   "name": "oldPW"
		 },
		 {
		   "label": "New Password",
		   "name": "newPW"
		 },
		 {
		   "label": "Confirm Password",
		   "name": "confirmPW"
		 }
	]
};

var personalInfo_home_name = ["home_personalInfo_email", "home_personalInfo_firstname", "home_personalInfo_familyname", "home_personalInfo_gender", "home_personalInfo_city", "home_personalInfo_country"];

