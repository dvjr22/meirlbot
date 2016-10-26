import { Template } from 'meteor/templating';

import './home.html';
import '../components/trends.js';



Template.home.helpers({
  generateURL: function (){
    return "America";
  },
  generateURL2: function (){
    return "Europe";
  },
  generateURL3: function (){
    return "Asia";
  },
});
