import '/imports/startup';
import { Meteor } from 'meteor/meteor';

Meteor.startup(() => {
    console.log("Client Spinning Up");
    Ticker = new Mongo.Collection('ticker');

    var anotherTest = Ticker.find({ test: "test" }).fetch();

    console.log(anotherTest);
});
