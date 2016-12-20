package com.tmoon8730;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.scheduling.annotation.EnableScheduling;

import com.tmoon8730.api.*;
import com.tmoon8730.creator.RedditDownloader;
import com.tmoon8730.trend.*;

@SpringBootApplication
@EnableScheduling
public class MemeProcessorApplication {
	private static final Logger log = LoggerFactory.getLogger(MemeProcessorApplication.class);
	public static void main(String[] args) {
		SpringApplication.run(MemeProcessorApplication.class);
	}
	
	/*private final UpvoteChecker upvoteChecker;
	
	public MemeProcessorApplication(UpvoteChecker upvoteChecker){
		this.upvoteChecker = upvoteChecker;
	}
	
	@Bean
	public CommandLineRunner run() throws Exception {
		return args -> {
		*/	
			
			//RedditDownloader rd = new RedditDownloader();
			//rd.download();
			
			/*RedditAPI api = new RedditAPI();
			RedditPost p = api.getPostForRedditId("5j5eb1");
			log.info(p.toString());*/
			
			//UpvoteChecker upvoteChecker = new UpvoteChecker();
			//upvoteChecker.CheckUpvotes("me_irl");
			
			
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
		//};
//	}
}
