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
           "tab": "home",
           "name": "email",
           "label": "Email"
         },
         {
           "tab": "home",
           "name": "firstname",
           "label": "First Name"
         },
         {
           "tab": "home",
           "name": "familyname",
           "label": "Family Name"
         },
         {
           "tab": "home",
           "name": "gender",
           "label": "Gender"
         },
         {
           "tab": "home",
           "name": "city",
           "label": "City"
         },
         {
           "tab": "home",
           "name": "country",
           "label": "Country"
         }
    ],
	personalInfo_browse: [
         {
           "tab": "browse",
           "name": "email",
           "id": "email_otherUser",
           "label": "Email"
         },
         {
           "tab": "browse",
           "name": "firstname",
           "label": "First Name"
         },
         {
           "tab": "browse",
           "name": "familyname",
           "label": "Family Name"
         },
         {
           "tab": "browse",
           "name": "gender",
           "label": "Gender"
         },
         {
           "tab": "browse",
           "name": "city",
           "label": "City"
         },
         {
           "tab": "browse",
           "name": "country",
           "label": "Country"
         }
    ],
	changePW : [
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

