package com.tmoon8730.creator;

import java.io.IOException;
import java.util.ArrayList;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.tmoon8730.api.RedditAPI;
import com.tmoon8730.api.RedditPost;

public class TesseractOCRProcessor {
	private static final Logger log = LoggerFactory.getLogger(TesseractOCRProcessor.class);
	
	private RedditAPI redditAPI;
	private KeywordProcessor keywordProcessor;
	
	public TesseractOCRProcessor(){
		redditAPI = new RedditAPI();
		keywordProcessor = new KeywordProcessor();
	}
	public void OCRProcess(){
		ArrayList<RedditPost> list = getList();
		ArrayList<String> textFiles = new ArrayList<String>();
		log.info("list length: " + list.size());
		for(RedditPost p : list){
			log.info("Processing file: " + p.getImageLocation());
			textFiles.add(processFile(p.getImageLocation()));
		}
		ArrayList<String> keywords = keywordProcessor.generateKeyTerm(textFiles);
		for(String key : keywords){
			System.out.println("keyword: " + key);
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
			log.info("Error processing file " + filename);
			e.printStackTrace();
		}
		return filename + ".txt";
	}
}
