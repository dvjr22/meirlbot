import { Meteor } from 'meteor/meteor';

Meteor.startup(() => {
    // code to run on server at startup
    Ticker = new Mongo.Collection('ticker');

    var ticker = JSON.parse(Assets.getText('tickerData.json'));
    
    Ticker.insert(ticker);

    var test = Ticker.find({ test: "test" }).fetch();

    console.log(test);
    
    console.log(ticker);
});
