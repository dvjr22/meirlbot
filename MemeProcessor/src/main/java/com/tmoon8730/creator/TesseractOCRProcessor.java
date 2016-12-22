package com.tmoon8730.creator;

import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;

import com.tmoon8730.api.RedditAPI;
import com.tmoon8730.api.RedditPost;

public class TesseractOCRProcessor {
	private RedditAPI redditAPI;
	
	private static final Logger log = LoggerFactory.getLogger(TesseractOCRProcessor.class);
	
	public TesseractOCRProcessor(){
		redditAPI = new RedditAPI();
	}
	public void OCRProcess(){
		RedditPost[] list = getList();
		log.info("list length: " + list.length);
		for(RedditPost p : list){
			log.info(p.toString());
			//log.info("Processing file: " + p.getImageLocation());
			//processFile(p.getImageLocation());
		}
	}
	private RedditPost[] getList(){
		RedditPost[] list = redditAPI.getAllPosts();
		RedditPost[] returnList = new RedditPost[list.length];
		int count = 0;
		for(RedditPost p : list){
			log.info("Checking " + !(p.getImageLocation().equals("")));
			if(!(p.getImageLocation().equals(""))){
				log.info("found post: " + p.toString());
				returnList[count] = p;
				count ++;
			}
		}
		return returnList;
	}
	private void processFile(String filename){
		
		Runtime rt = Runtime.getRuntime();
		try {
			rt.exec("/usr/local/bin/tesseract " + filename + " " + filename);
			log.info("Writing file to " + filename + ".txt");
		} catch (IOException e) {
			log.info("Error processing file " + filename);
			e.printStackTrace();
		}
	}
}
