package com.tmoon8730;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import com.tmoon8730.api.*;
import com.tmoon8730.creator.RedditDownloader;
import com.tmoon8730.trend.*;

@SpringBootApplication
public class MemeProcessorApplication {
	private static final Logger log = LoggerFactory.getLogger(MemeProcessorApplication.class);
	public static void main(String[] args) {
		SpringApplication.run(MemeProcessorApplication.class);
	}
	
	@Bean
	public RedditAPI redditAPI(){
		return new RedditAPI();
	}
	
	@Bean
	public CommandLineRunner run(RedditAPI redditAPI) throws Exception {
		return args -> {
		/*	UpvoteChecker upvoteChecker = new UpvoteChecker();
			upvoteChecker.CheckUpvotes("me_irl");*/
			
		//	String sourceUrl = "http://imgur.com/7AvrWSW";
			RedditDownloader redditDownloader = new RedditDownloader();
			redditDownloader.download();
			
		};
	}
}
