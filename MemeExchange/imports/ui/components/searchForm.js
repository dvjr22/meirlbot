import { Template } from 'meteor/templating';
import { Session } from 'meteor/session';
import './searchForm.html';

/*
 * Handlers for events from the searchFrom Template
 */
Template.searchForm.events({
  // Triggered when the for is submitted
  // either by pressing the submit button
  // or by pressing enter after typing the
  // search term
  'submit form': function(event){
    event.preventDefault(); // This stops the page from reloading
    searchTerm = event.target.playerName.value; // Gets the value from the text field
    console.log("search term = " + searchTerm);
    Session.set("searchTerm", searchTerm); // Sets the session variable so that it can be accessed in the helper functions
  },
})


/*
 * Helper functions that are accesible from the html by {{<function name>}}
 */
Template.searchForm.helpers({
  // A getter for the searchTerm variable which is
  // passed to the trends template and then into
  // the iframe to change the graph
  searchTerm: function(){
    return Session.get("searchTerm"); // Returns the Session variable searchTerm which is set by the search text field
  },
})

/*
 * Created function when the template is created to initialize variables
 */
Template.searchForm.created = function(){
  Session.set("searchTerm","dat%20boi");
}
