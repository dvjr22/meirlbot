import { Meteor } from 'meteor/meteor';

Meteor.startup(function () {
  // Load future from fibers
  var Future = Npm.require("fibers/future");
  // Load exec
  var exec = Npm.require("child_process").exec;

  var PythonShell = require('python-shell');
  // TODO: Remove the hard coded paths
  var logOptions = {
    scriptPath: '/Users/tmoon/_Code/meirlbot/LogWriter',
  }
  var upvoteOptions = {
    scriptPath: '/Users/tmoon/_Code/meirlbot/MemeTrend',
  }
  var mongoOptions = {
    scriptPath: '/Users/tmoon/_Code/meirlbot/MongoDB',
  }

  // Initialize the scripts to the running state on startup of the server
  var logShell = new PythonShell('logFileWriter.py', logOptions);
  //var newMemeShell = new PythonShell('newMemeIdentifier.py', newMemeOptions);
  var mongoDBShell = new PythonShell('MongoDBDatabase.py', mongoOptions);

  // Asynchronous Method.
/*  Meteor.startup(function() {
    console.log('starting up reading file');
    var fs = Npm.require('fs');
    // Log file saved to public/system.log
    fs.readFile(process.cwd() + '/../web.browser/app/system.log','utf8',function(err,data){
      if(err){
        console.log('ERROR: ' + err);
        return;
      }
      console.log(data);
    });
  });
*/
  // Server methods
  Meteor.methods({
    logWriter: function(startOrStop) {
      if(startOrStop == 'stop'){
        logShell.send('stop');
        return 'stopped logFileWriter.py'
      }else if(startOrStop == 'start'){
        logShell = new PythonShell('logFileWriter.py',logOptions);
        return 'started logFileWriter.py'
      }
    },
    upvoteChecker: function(startOrStop){
      if(startOrStop == 'stop'){
        newMemeShell.send('stop');
        return 'stopped upvoteChecker.py'
      }else if(startOrStop == 'start'){
        upvoteCheckerShell = new PythonShell('upvoteChecker.py',upvoteOptions)
      }
    },
    mongoDBDatabase: function(startOrStop){
      if(startOrStop == 'stop'){
        mongoDBShell.send('stop');
        return 'stopped MongoDBDatabase.py'
      }else if(startOrStop == 'start'){
        mongoDBShell = new PythonShell('MongoDBDatabase.py', mongoOptions);
        return 'started MongoDBDatabase.py'
      }
    },
    returnLogs: function(){
      console.log('starting up reading file');
      var fs = Npm.require('fs');
      // Log file saved to public/system.log
      fs.readFile(process.cwd() + '/../web.browser/app/system.log','utf8',function(err,data){
        if(err){
          console.log('ERROR: ' + err);
          return;
        }
        console.log(data);
        return data
      });
    }
  });
});
