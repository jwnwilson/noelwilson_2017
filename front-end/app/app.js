/* Libs */
require("angular/angular");
require("angular-route/angular-route");
require("angular-resource/angular-resource");
/* Config Vars */
var routesConfig = require("./routes");
/* Components */
require("./components/home/home");

/* Globals */
_ = require("lodash");
_urlPrefixes = {
  API: "api/v1/",
  TEMPLATES: "static/app/"
};

/* Components */

/* App Dependencies */
angular.module("app", [
  "Home",
  "ngResource",
  "ngRoute",
]);

/* App Config */
angular.module("app").config(routesConfig);
