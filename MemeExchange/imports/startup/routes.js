import { FlowRouter } from 'meteor/kadira:flow-router';
import { BlazeLayout } from 'meteor/kadira:blaze-layout';

// Import layout
import '../ui/layout/applicationLayout.js';

// Import pages
import '../ui/pages/home.js';
import '../ui/pages/about.js';
import '../ui/pages/search.js';

/*
 * Home Page
 */
FlowRouter.route('/',{
  action: function(){
    // Renders when the http://app.com/ route is hit
    console.log("In the Home Page!");
    // Render the home page
    // /imports/ui/pages/home.html
    BlazeLayout.render('applicationLayout', { main: 'home', title: 'Home Page' });
  },
  name: 'home'
})

/*
 * Search Page
 */
FlowRouter.route('/search', {
  action: function(){
    // Renders when the http://app.com/search route is hit
    console.log("In the Search Page!");
    // Render the search page
    // /imports/ui/pages/search.html
    BlazeLayout.render('applicationLayout', { main: 'search', title: 'Search Page' });
  }
})

/*
 * Terms of Service Page
 */
FlowRouter.route('/about', {
  action: function(){
    // This stuff happens when we visit http://app.com/terms
    console.log("In the About Page!");
    // Render the terms of service page
    // /imports/ui/pages/termsOfService.html
    BlazeLayout.render('applicationLayout', { main: 'about', title: 'About Page' });
  },
  name: 'about' // Optional route name
})
