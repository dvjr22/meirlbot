package com.tmoon8730;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
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
	public CommandLineRunner run() throws Exception {
		return args -> {
			UpvoteChecker upvoteChecker = new UpvoteChecker();
			upvoteChecker.CheckUpvotes("me_irl");
			
			
			//RedditAPI redditapi = new RedditAPI();
			//System.out.println("  [x] Attempting to delete the new post 58507224154dcb049f787ad7");
			//redditapi.deletePost("58507224154dcb049f787ad7");
			
			/*RedditPost post = redditapi.getById("582e14acce436b0617aabb35");
			System.out.println("Before put");
			System.out.println(post.toString());
			post.setMemeFlag(true);
			redditapi.putByRedditPost(post);
			post = redditapi.getById("582e14acce436b0617aabb35");
			System.out.println("After put");
			System.out.println(post.toString());
			*/
			/*RedditPost[] posts = redditapi.getAllPosts();
			for(RedditPost p : posts){
				System.out.println(p.toString());
			}*/
		};
	}
}
