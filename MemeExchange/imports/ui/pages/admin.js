import './admin.html';
import { Meteor } from 'meteor/meteor';
import { Template } from 'meteor/templating';


Template.admin.onCreated(function(){
  Session.set("responseText", "Default");
  // Start all the action buttons with the start button disabled (the processes
  // are automatically started when the server does) and the stop buttons enabled
  Session.set("logDisabledStartVar", false);
  Session.set("logDisabledStopVar", true);

  Session.set("mongoDisabledStartVar", false);
  Session.set("mongoDisabledStopVar", true);

  Session.set("upvoteCheckerDisabledStartVar", false);
  Session.set("upvoteCheckerDisabledStopVar", true);

  Session.set("newMemeIdentifierDisabledStartVar", false);
  Session.set("newMemeIdentifierDisabledStopVar", true);

  Session.set("redditDownloaderDisabledStartVar", false);
  Session.set("redditDownloaderDisabledStopVar", true);

  Session.set("captionFinderDisabledStartVar", false);
  Session.set("captionFinderDisabledStopVar", true);

  Session.set("googleDownloaderDisabledStartVar", false);
  Session.set("googleDownloaderDisabledStopVar", true);

  Session.set("memeCreatorDisabledStartVar", false);
  Session.set("memeCreatorDisabledStopVar", true);

  Session.set("logData","");
});

Template.admin.helpers({
  responseText: function(){
    return Session.get("responseText");
  },
  logDisabledStart: function(){
    return Session.get("logDisabledStartVar");
  },
  logDisabledStop: function(){
    return Session.get("logDisabledStopVar");
  },
  mongoDisabledStart: function(){
    return Session.get("mongoDisabledStartVar");
  },
  mongoDisabledStop: function(){
    return Session.get("mongoDisabledStopVar");
  },
  upvoteCheckerStart: function(){
    return Session.get("upvoteCheckerDisabledStartVar");
  },
  upvoteCheckerStop: function(){
    return Session.get("upvoteCheckerDisabledStopVar");
  },
  newMemeIdentifierStart: function(){
    return Session.get("newMemeIdentifierDisabledStartVar");
  },
  newMemeIdentifierStop: function(){
    return Session.get("newMemeIdentifierDisabledStopVar");
  },
  redditDownloaderStart: function(){
    return Session.get("redditDownloaderDisabledStartVar");
  },
  redditDownloaderStop: function(){
    return Session.get("redditDownloaderDisabledStopVar");
  },
  captionFinderStart: function(){
    return Session.get("captionFinderDisabledStartVar");
  },
  captionFinderStop: function(){
    return Session.get("captionFinderDisabledStopVar");
  },
  googleDownloaderStart: function(){
    return Session.get("googleDownloaderDisabledStartVar");
  },
  googleDownloaderStop: function(){
    return Session.get("googleDownloaderDisabledStopVar");
  },
  memeCreatorStart: function(){
    return Session.get("memeCreatorDisabledStartVar");
  },
  memeCreatorStop: function(){
    return Session.get("memeCreatorDisabledStopVar");
  },
  logData: function(){
    var data = Session.get("logData");
    if(data) return data;
    return 'Loading log data....';
  }
});

Template.admin.events({
  "click #logButton": function(event, template){
    console.log("logWriter btn pressed")
    var buttonText = template.$("responseButton").text();
    Meteor.call('startLogWriter', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
  },


  // Log Button
  "click #startLogButton": function(event, template){
    console.log("logWriter start btn pressed")
    Meteor.call('pythonShell', 'start', 'LogWriter', 'logFileWriter', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("logDisabledStartVar",true)
    Session.set("logDisabledStopVar",false)
    console.log(Session.get("logDisabledStartVar"))
  },
  "click #stopLogButton": function(event, template){
    console.log("logWriter stop btn pressed")
    Meteor.call('pythonShell', 'stop', 'LogWriter', 'logFileWriter', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("logDisabledStartVar", false)
    Session.set("logDisabledStopVar",true)
    console.log(Session.get("logDisabledStopVar"))
  },

  // MongoDB Button
  "click #startMongoButton": function(event, template){
    console.log("mongoDBDatabase start btn pressed")
    Meteor.call('pythonShell', 'start', 'MongoDB', 'MongoDBDatabase', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("mongoDisabledStartVar",true)
    Session.set("mongoDisabledStopVar",false)
    console.log(Session.get("mongoDisabledStartVar"))
  },
  "click #stopMongoButton": function(event, template){
    console.log("mongoDBDatabase stop btn pressed")
    Meteor.call('pythonShell', 'stop', 'MongoDB', 'MongoDBDatabase', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("mongoDisabledStartVar", false)
    Session.set("mongoDisabledStopVar",true)
    console.log(Session.get("mongoDisabledStopVar"))
  },
  // Upvote Checker Button
  "click #startUpvoteChecker": function(event, template){
    console.log("upvoteChecker start btn pressed")
    Meteor.call('pythonShell', 'start', 'MemeTrend', 'upvoteChecker', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("upvoteCheckerDisabledStartVar",true)
    Session.set("upvoteCheckerDisabledStopVar",false)
    console.log(Session.get("upvoteCheckerDisabledStartVar"))
  },
  "click #stopUpvoteChecker": function(event, template){
    console.log("upvoteChecker stop btn pressed")
    Meteor.call('pythonShell', 'stop', 'MemeTrend', 'upvoteChecker', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("upvoteCheckerDisabledStartVar", false)
    Session.set("upvoteCheckerDisabledStopVar",true)
    console.log(Session.get("upvoteCheckerDisabledStopVar"))
  },
  // newMemeIdentifier Button
  "click #startNewMemeIdentifier": function(event, template){
    console.log("newMemeIdentifier start btn pressed")
    Meteor.call('pythonShell', 'start', 'MemeTrend', 'newMemeIdentifier', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("newMemeIdentifierDisabledStartVar",true)
    Session.set("newMemeIdentifierDisabledStopVar",false)
    console.log(Session.get("newMemeIdentifierDisabledStartVar"))
  },
  "click #stopNewMemeIdentifier": function(event, template){
    console.log("newMemeIdentifier stop btn pressed")
    Meteor.call('pythonShell', 'stop', 'MemeTrend', 'newMemeIdentifier', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("newMemeIdentifierDisabledStartVar", false)
    Session.set("newMemeIdentifierDisabledStopVar",true)
    console.log(Session.get("newMemeIdentifierDisabledStopVar"))
  },
  // redditDownloader Button
  "click #startRedditDownloader": function(event, template){
    console.log("redditDownloader start btn pressed")
    Meteor.call('pythonShell', 'start', 'MemeCreator', 'redditDownloader', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("redditDownloaderDisabledStartVar",true)
    Session.set("redditDownloaderDisabledStopVar",false)
    console.log(Session.get("redditDownloaderDisabledStartVar"))
  },
  "click #stopRedditDownloader": function(event, template){
    console.log("redditDownloader stop btn pressed")
    Meteor.call('pythonShell', 'stop', 'MemeCreator', 'redditDownloader', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("redditDownloaderDisabledStartVar", false)
    Session.set("redditDownloaderDisabledStopVar",true)
    console.log(Session.get("redditDownloaderDisabledStopVar"))
  },
  // captionFinder Button
  "click #startCaptionFinder": function(event, template){
    console.log("captionFinder start btn pressed")
    Meteor.call('pythonShell', 'start', 'MemeCreator', 'captionFinder', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("captionFinderDisabledStartVar",true)
    Session.set("captionFinderDisabledStopVar",false)
    console.log(Session.get("captionFinderDisabledStartVar"))
  },
  "click #stopCaptionFinder": function(event, template){
    console.log("captionFinder stop btn pressed")
    Meteor.call('pythonShell', 'stop', 'MemeCreator', 'captionFinder', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("captionFinderDisabledStartVar", false)
    Session.set("captionFinderDisabledStopVar",true)
    console.log(Session.get("captionFinderDisabledStopVar"))
  },
  // googleDownloader Button
  "click #startGoogleDownloader": function(event, template){
    console.log("googleDownloader start btn pressed")
    Meteor.call('pythonShell', 'start', 'MemeCreator', 'googleDownloader', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("googleDownloaderDisabledStartVar",true)
    Session.set("googleDownloaderDisabledStopVar",false)
    console.log(Session.get("googleDownloaderDisabledStartVar"))
  },
  "click #stopGoogleDownloader": function(event, template){
    console.log("googleDownloader stop btn pressed")
    Meteor.call('pythonShell', 'stop', 'MemeCreator', 'googleDownloader', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("googleDownloaderDisabledStartVar", false)
    Session.set("googleDownloaderDisabledStopVar",true)
    console.log(Session.get("googleDownloaderDisabledStopVar"))
  },
  // memeCreator Button
  "click #startMemeCreator": function(event, template){
    console.log("memeCreator start btn pressed")
    Meteor.call('pythonShell', 'start', 'MemeCreator', 'memeCreator', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("memeCreatorDisabledStartVar",true)
    Session.set("memeCreatorDisabledStopVar",false)
    console.log(Session.get("memeCreatorDisabledStartVar"))
  },
  "click #stopMemeCreator": function(event, template){
    console.log("memeCreator stop btn pressed")
    Meteor.call('pythonShell', 'stop', 'MemeCreator', 'memeCreator', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("memeCreatorDisabledStartVar", false)
    Session.set("memeCreatorDisabledStopVar",true)
    console.log(Session.get("memeCreatorDisabledStopVar"))
  },
  // Refresh button
  "click #refreshButton": function(event, template){
    console.log("refreshing logs")
    Meteor.call('logShell', function(err,response){
      if(err){
        alert(err);
      }else{
        console.log('response ' + JSON.stringify(response));
        Session.set("logData",JSON.stringify(response['content']));
      }

    });
  }
})
