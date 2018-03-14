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
    ]
};

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
    source_signin = document.getElementById("welcomeview").innerHTML;
    template_signin = Handlebars.compile(source_signin);
}