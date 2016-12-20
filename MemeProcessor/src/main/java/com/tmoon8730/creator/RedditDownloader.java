package com.tmoon8730.creator;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;

import javax.imageio.ImageIO;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.tmoon8730.api.RedditAPI;
import com.tmoon8730.api.RedditPost;


public class RedditDownloader {
	
	private static final Logger log = LoggerFactory.getLogger(RedditDownloader.class);
	
	private RedditAPI redditAPI;
	
	
	public RedditDownloader(){
		redditAPI = new RedditAPI();
	}
	
	/**
	 * End point for starting the download process. This method loops through all the
	 * posts stored in the database with a memeFlag of true and downloads the memes.
	 * 
	 * tl;dr Download those memes brah
	 */
	public void download(){
		// TODO: Change this to only use memes with a memeFlag of true
		RedditPost[] posts = redditAPI.getAllPosts();
		log.info("found " + posts.length + " posts");
		for(RedditPost value: posts){
			if(value.isMemeFlag()){
				String imageUrl = value.getImageUrl();
				log.info("Trying to download: " + imageUrl);
				try{
					parseInput(imageUrl);
				}catch(IOException e){
					e.printStackTrace();
				}
				value.setMemeFlag(false);
				value.setUpvoteTrend(0);
				redditAPI.updatePost(value);
			}
		}
	}
	
	private void parseInput(String sourceUrl) throws IOException{
		// Download the image directly if the url contains png or jpg
		if(sourceUrl.contains("png") || sourceUrl.contains("jpg")){
			log.info("download directly " + sourceUrl);
			// TODO: Place the code below in its own method 
			downloadImage(sourceUrl);
		}
		// Assuming its an imgur albumn so parse through the html to find the img src
		else
		{
			log.info("html parse download" + sourceUrl);
			
			// Load the html code
			Document doc = Jsoup.connect(sourceUrl).get();
			
			// Parse out only the img tags which have a src attribute
			Elements links = doc.select("img[src]");
			
			// Loop through each link
			for(Element link : links){
				String imageURL = "http:" + link.attr("src").toString();
				// TODO: Hangle more than just imgur
				// If the img does not contain imgur its probably a header image or some other
				// unwanted image
				if(imageURL.contains("imgur")){
					log.info("  [x]: " + imageURL);
					downloadImage(imageURL);
				}//END: if(imageUrl.contains...
			}// END: for(Element link...	
		}// END: if(sourceUrl.contains...
	}// END: public void downloadImage...
	
	
	/**
	 * Download the image
	 * @param sourceUrl
	 */
	private void downloadImage(String imageURL){
		// Download the image
		BufferedImage image = null;
		try{
			URL url = new URL(imageURL);
			image = ImageIO.read(url);
			// If the ImageIO.read did not work then the image will be null so skip it
			if(image != null){
				// Replace the '/' chars in the url to create a temp filename
				String filename = imageURL.replace('/', '_').replace(':','_').substring(4);
				log.info("filename: " + filename);
				// Get the type off the end of the url
				String type = filename.substring(filename.length() - 3);
				log.info("type: " + type);
				// Write the image to the /tmp/ directory
				ImageIO.write(image, "png", new File("/tmp/images/" + filename));
				// TODO: Update the database to the file location
				// TODO: Find a better directory to save too
			}else{
				log.error("image was null " + imageURL);
			}
		}catch(IOException e){
			e.printStackTrace();
		}//END: try{...
	}// END: private void...
}
