# MEIRLBOT
[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

And if that didn't convince you then:

This is a python program for analyzing meme usage on reddit's me_irl subreddit and creating relevent memes for posting


## Installation
* Clone this repo
* Setup a Google Vision Credentials
* Set the GOOGLE_APPLICATION_CREDENTIALS variable to the path to the JSON file from the previous step
* Make sure there are read and write privileges to the images and createdMemes directory

## Run Project
* Use the following command to start the project
  - ./zMeIrlBot <reddit subreddit name>

## Explanation of Project Parts
MEIRLBOT is split into six different parts with each part using a different technology. The majority of the project is written in the Python scripting language with a bash script to start it all. 

| Part Name       | File Name     | Use                              | Main Technology       | Language       |
| ------------- | ------------- | -------------------------------- | --------------------- | -------------- |
| Reddit Downloader| redditDownloader.py| Downloads images from a given subreddit | [PRAW (Python Reddit API Wrapper](https://praw.readthedocs.io/en/stable/)) | Python  |
| Keyword Gatherer | keywordGatherer.py | Determines keywords based on the subject of each image | [Google Vision API](https://cloud.google.com/vision/) | Python |
| Keyword Condenser | keywordCondenser.py | Finds the two most common keywords from the Keyword Gatherer | [Base Python](https://www.python.org/) | Python |
| Google Downloader | googleDownloader.py | Scrapes Google Images using the most common keywords to get the base of the meme | [GoogleImageCrawler](https://pypi.python.org/pypi/icrawler/0.2.2) | Python |
| Meme Creator | memeCreator.py | Creates the meme from the keywords and the images | [PIL (Python Image Library](http://www.pythonware.com/products/pil/)) | Python |
| Reddit Uploader | redditPost.skl | Takes control of the mouse and uses image recognition to navigate to Reddit and upload the meme due to no upload ability in PRAW | [SikuliX](http://www.sikulix.com/) | Sikuli (Using Python) |

## Contributions
If anyone wants to work on MEIRLBOT feel free to fork this repository and work on it. Once you have a working version with new features then submit a pull request and the project owner will review it and merge it in.

If you have any questions feel free to email moon.tyler@gmail.com
