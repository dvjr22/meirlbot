import { Template } from 'meteor/templating';

import './home.html';
import '../components/trends.js';



Template.home.helpers({
  generateURL: function (){
    return "Pepe the frog";
  },
  generateURL2: function (){
    return "Dat boi";
  },
  generateURL3: function (){
    return "Harambe";
  },
});
