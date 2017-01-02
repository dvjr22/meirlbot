# MEIRLBOT

The MEIRLBOT is a set of Java Spring Boot applications for the purpose of creating and displaying memes. The main reason for creating this project was to learn new technologies and build resumes. There are three different applications and a MongoDB database. The MemeAPI is a REST API for interacting with the MongoDB Database Collection. The MemeProcessor project is the application which processes memes from Reddit's me_irl subreddit for relevent current memes and attempts to create a similar meme. There are several parts to the project which involve a Reddit API, a Flickr API for downloading source images, and a Tesseract OCR program for OCR of the image captions. The third and final part of the MEIRLBOT is the MemeExchange which is a React JS webapp for displaying the created memes from the MemeProcessor. 

## Installation

This is a Spring Boot application which is easily developed and deployed from the [Spring Tool Suite](https://spring.io/tools) program. Also the [Tesseract OCR program](https://github.com/tesseract-ocr/tesseract) needs to be installed, and a [MongoDB](https://www.mongodb.com/) database. The MongoDB Database can be started by using `mongod` and the other components can be run by `mvn spring-boot:run` or by using the STS IDE. 

## Usage

To compile the Spring Boot applications into a executable jar file use the command `mvn package` from the application directory. To then run the application use `java -jar target/JARFILENAME`. For the MemeProcessor or the MemeExchange to work the MemeAPI needs to be running. For the MemeAPI to work the MongoDB database must be running. 

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request and put Tyler Moon as the reviewer :D

## History

### October 2016
- Start of MEIRLBOT with a Python script for downloading images from Reddit
- Got the initial MemeExchange built with Meteor.js

### November 2016
- Added a MongoDB Database and RabbitMQ Messaging server

### November and December 2016
- Finished the Python prototype 
- Re-wrote MEIRLBOT in Java using the Spring Boot platform

## Credits

Tyler Moon

## License

Copyright 2017 Tyler Moon

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
