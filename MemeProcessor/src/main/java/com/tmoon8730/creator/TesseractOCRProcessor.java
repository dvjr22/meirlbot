package com.tmoon8730.creator;

import java.io.IOException;
import java.util.ArrayList;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.tmoon8730.api.FlickrAPI;
import com.tmoon8730.api.RedditAPI;
import com.tmoon8730.api.RedditPost;

public class TesseractOCRProcessor {
	private static final Logger log = LoggerFactory.getLogger(TesseractOCRProcessor.class);
	
	private RedditAPI redditAPI;
	private KeywordProcessor keywordProcessor;
	private FlickrAPI flickrAPI;
	private FlickrImageDownloader flickrImageDownloader;
	private TextWriter textWriter;
	
	public TesseractOCRProcessor(){
		redditAPI = new RedditAPI();
		keywordProcessor = new KeywordProcessor();
		flickrAPI = new FlickrAPI();
		flickrImageDownloader = new FlickrImageDownloader();
		textWriter = new TextWriter();
	}
	public void OCRProcess(){
		ArrayList<RedditPost> list = getList();
		ArrayList<String> textFiles = new ArrayList<String>();
		log.info("list length: " + list.size());
		for(RedditPost p : list){
			log.info("Processing file: " + p.getImageLocation());
			textFiles.add(processFile(p.getImageLocation()));
		}
		// Wait for the files to be finished writing too
		try{
			Thread.sleep(2000);
		}catch(InterruptedException ex){
			Thread.currentThread().interrupt();
		}
		// Process the generated text files
		ArrayList<String> keywords = keywordProcessor.generateKeyTerm(textFiles);
		for(String key : keywords){
			// Print out the results
			System.out.println("keyword: " + key);
			// Download a Flickr image using the first word from the key
			// TODO: There may be some need to play around with this to get good images to appear
			int index = key.indexOf(' '); // Get the index of the first space
			String word = key.substring(0, index);
			String url = flickrAPI.getForTerm(word);
			flickrImageDownloader.downloadImage(url);
			textWriter.writeText(url,key);
		}
		
	}
	private ArrayList<RedditPost> getList(){
		RedditPost[] list = redditAPI.getAllPosts();
		ArrayList<RedditPost> returnList = new ArrayList<RedditPost>();
		for(RedditPost p : list){
			log.info("Checking " + !(p.getImageLocation().equals("")));
			if(!(p.getImageLocation().equals(""))){
				log.info("found post: " + p.toString());
				returnList.add(p);
			}
		}
		return returnList;
	}
	private String processFile(String filename){
		
		Runtime rt = Runtime.getRuntime();
		try {
			rt.exec("/usr/local/bin/tesseract " + filename + " " + filename);
			log.info("Writing file to " + filename + ".txt");
		} catch (IOException e) {
			// print the log message
			log.info("Error processing file " + filename);
			e.printStackTrace();
		}
		return filename + ".txt";
	}
}
