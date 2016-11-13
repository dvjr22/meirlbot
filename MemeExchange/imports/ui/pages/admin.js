import './admin.html';
import { Meteor } from 'meteor/meteor';
import { Template } from 'meteor/templating';

Template.admin.onCreated(function(){
  Session.set("responseText", "Default");
  // Start all the action buttons with the start button disabled (the processes
  // are automatically started when the server does) and the stop buttons enabled
  Session.set("logDisabledStartVar", true);
  Session.set("logDisabledStopVar", false);
  Session.set("mongoDisabledStartVar", true);
  Session.set("mongoDisabledStopVar", false);
  Session.set("upvoteCheckerDisabledStartVar", false);
  Session.set("upvoteCheckerDisabledStopVar", true);
  Session.set("logData","Log Data Here!");
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
  logData: function(){
    return Session.get("logData");
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
    Meteor.call('logWriter', 'start', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("logDisabledStartVar",true)
    Session.set("logDisabledStopVar",false)
    console.log(Session.get("logDisabledStartVar"))
  },
  "click #stopLogButton": function(event, template){
    console.log("logWriter stop btn pressed")
    Meteor.call('logWriter', 'stop', function(err,response) {
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
    Meteor.call('mongoDBDatabase', 'start', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("mongoDisabledStartVar",true)
    Session.set("mongoDisabledStopVar",false)
    console.log(Session.get("mongoDisabledStartVar"))
  },
  "click #stopMongoButton": function(event, template){
    console.log("mongoDBDatabase stop btn pressed")
    Meteor.call('mongoDBDatabase', 'stop', function(err,response) {
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
    Meteor.call('upvoteChecker', 'start', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("upvoteCheckerDisabledStartVar",true)
    Session.set("upvoteCheckerDisabledStopVar",false)
    console.log(Session.get("upvoteCheckerDisabledStartVar"))
  },
  "click #stopUpvoteChecker": function(event, template){
    console.log("upvoteChecker stop btn pressed")
    Meteor.call('upvoteChecker', 'stop', function(err,response) {
      console.log('response ' + response);
      Session.set("responseText",response)
    });
    Session.set("upvoteCheckerDisabledStartVar", false)
    Session.set("upvoteCheckerDisabledStopVar",true)
    console.log(Session.get("upvoteCheckerDisabledStopVar"))
  },
  "click #refreshButton": function(event, template){
    console.log("refreshing logs")
    Meteor.call('returnLogs', function(err,response){
      console.log('response ' + response);
      Session.set("logData",response);
    });
  }
})
