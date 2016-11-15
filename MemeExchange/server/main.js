import { Meteor } from 'meteor/meteor';

Meteor.startup(function () {
  // Load future from fibers
  var Future = Npm.require("fibers/future");
  // Load exec
  var exec = Npm.require("child_process").exec;
  var request = Npm.require('request');

  // Server methods
  Meteor.methods({
    pythonShell: function(startOrStop, directory, filename) {
      request('http://localhost:5008/' + startOrStop + '/' + directory + '/' + filename, function(error, response, body){
        if (!error && response.statusCode == 200){
          console.log(body)
        }
      })
      return startOrStop + ' ' + filename + '.py'
    },
    logShell: function(){
      var future = new Future();
      HTTP.get('http://localhost:5008/log/return/', {}, function(error, response){
        if( error ){
          future.return(error);
        }else{
          future.return(response);
        }
      });
      return future.wait();
    }
  });
});
