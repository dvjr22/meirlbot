# MEIRLBOT
[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

And if that didn't convince you then:

This is a python program for analyzing meme usage on reddit's me_irl subreddit and creating relevent memes for posting

## MemeCreator Bot
The purpose of the MemeCreator Bot is to generate new spicy memes. Using a MongoDB database with memes that have been found by the MemeTrend Bot to be new hot memes, the MemeCreator Bot attempts to create a new meme using a similar image and caption and then post that meme to the me_irl subreddit. This project is a work in progress and has new features planned faster than the original plan can be completed. The MemeCreator Bot is primarily written in Python and currently is started by a Bash Script.

### Installation
* Clone this repo
* Setup a Google Vision Credentials
* Set the GOOGLE_APPLICATION_CREDENTIALS variable to the path to the JSON file from the previous step
* Make sure there are read and write privileges to the images and createdMemes directory
* Run "pip install -r requirements.txt" to install all the python libraries needed
* Setup a [MongoDB](https://www.mongodb.com/) database
* Run "mongod" to start an instance of the database
* Run "./zMeIrlBot" from the MemeCreator directory to start the MemeCreator bot

### Run Bot
* Use the following command to start the project
  - ./zMeIrlBot <reddit subreddit name>

### Explanation of Bot Parts
MEIRLBOT is split into five different parts with each part using a different technology. The majority of the project is written in the Python scripting language with a bash script to start it all. 

| Part Name       | File Name     | Use                              | Main Technology       | Language       |
| ------------- | ------------- | -------------------------------- | --------------------- | -------------- |
| Reddit Downloader| redditDownloader.py| Downloads images from posts specified in the MongoDB database | [PRAW (Python Reddit API Wrapper](https://praw.readthedocs.io/en/stable/)) | Python  |
| Keyword Gatherer | keywordGatherer.py | Determines caption of each image where the updateFlag in the database is set to true | [Google Vision API](https://cloud.google.com/vision/) | Python |
| Google Downloader | googleDownloader.py | Scrapes Google Images using the caption to get a similar image to the meme | [GoogleImageCrawler](https://pypi.python.org/pypi/icrawler/0.2.2) | Python |
| Meme Creator | memeCreator.py | Creates the meme from the keywords and the images | [PIL (Python Image Library](http://www.pythonware.com/products/pil/)) | Python |
| Reddit Uploader | redditPost.skl | Takes control of the mouse and uses image recognition to navigate to Reddit and upload the meme due to no upload ability in PRAW | [SikuliX](http://www.sikulix.com/) | Sikuli (Using Python) |


### MongoDB Schema
This project stores data in a MongoDB nonrelational database. There is one database called "meirlbot_mongodb" and one collection called "redditposts". The data in the redditposts collection is stored as JSON data with each reddit post following the schema:
```JSON
{
  "url": "<The url of the image>",
  "upvotes": "<The number of upvotes as of the last time it was checked>",
  "redditId": "<Id of the specific post which makes it easy to look up the post using [PRAW](https://praw.readthedocs.io/en/stable)>",
  "updateFlag": "<Set to true if the image is going to be used as a base for a meme. Only true if there is more upvotes currently then there is in the upvotes field in the database>",
  "captionText": "<The caption as determined via the Google Vision API OCR>",
  "localFile": "<Path to the downloaded meme>",
  "createdMemeFile": "<Path to the created meme>",
  "createdMemeFlag": "<True if a meme has been created with this post or false if it has not>"
}
```

## MemeTrend Bot
The purpose of the MemeTrend Bot is to continually check me_irl's new page and try to determine if a new meme will become popular. When a meme is found then the redditId and the current upvote total is saved to the MongoDB database and the MemeCreator Bot is started.

### Installation
There is not installation needed currently for the MemeTrend Bot. Simply pull down the code and run the start command which is specified in the next section

### Run Bot
* Use the following command to start the MemeTrend Bot (Note. This project will continue to run at a 5 min interval until the ctl-c KeyboardInterrupt command is issued)
  - python upvoteChecker.py
  
### Explanation of Bot Parts
This bot multi-threads two different parts. One part is the loadFromReddit method which pulls upvote information from me_irl's new page. The second part is the checkDatabase method which checks all the posts in the upvoteposts collection for a change in upvotes.

## Feature Roadmap
This project started from a simple goal of figuring out how to download spicy memes from meirl. It has now grown to a much larger project with new ideas and sub projects added all the time. The plan for meirlbot as of 10/25/2016 is as follows:

1. Finish MemeCreator Bot

2. Create MemeTrend Bot
 
3. Integrate meirlbot project in with the [MemeExchange](https://github.com/tmoon8730/MemeExchange) project

## Contributions
If anyone wants to work on MEIRLBOT feel free to fork this repository and work on it. Once you have a working version with new features then submit a pull request and the project owner will review it and merge it in.

If you have any questions feel free to email moon.tyler@gmail.com
