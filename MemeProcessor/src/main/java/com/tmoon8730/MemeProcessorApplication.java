package com.tmoon8730;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import com.tmoon8730.api.*;

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
			log.info("getRedditPost");
			redditAPI.getRedditPost();
			log.info("getRedditPost with id 5d37yh");
			redditAPI.getRedditPost("5d37yh");
			RedditValue testPost = new RedditValue("5d943s",6469,0,false,"","");
			log.info("putRedditPost " + testPost.toString());
			redditAPI.postRedditPost(testPost);
			
		};
	}
}
