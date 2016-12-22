package com.tmoon8730;


import java.util.Scanner;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import com.tmoon8730.creator.RedditDownloader;
import com.tmoon8730.creator.TesseractOCRProcessor;
import com.tmoon8730.trend.*;

@SpringBootApplication
public class MemeProcessorApplication {
	private static final Logger log = LoggerFactory.getLogger(MemeProcessorApplication.class);
	public static void main(String[] args) {
		SpringApplication.run(MemeProcessorApplication.class);
	}
	
	/*private final UpvoteChecker upvoteChecker;
	
	public MemeProcessorApplication(UpvoteChecker upvoteChecker){
		this.upvoteChecker = upvoteChecker;
	}
	*/
	@Bean
	public CommandLineRunner run() throws Exception {
		return args -> {
			// NOTE: This is a temporary interface
			// TODO: Schedule this instead of running this janky stupid interface
			int option = 0;
			
			while(option != 99){
				Scanner keyboard = new Scanner(System.in);
				System.out.println("Operations: \n1) Run UpvoteChecker\n2) Run RedditDownloader\n3) Run Tesseract \n99) Exit");
				System.out.println("Enter your testing operation: ");
			    option = keyboard.nextInt();
				
				
				switch(option){
					case 1:
						UpvoteChecker upvoteChecker = new UpvoteChecker();
						upvoteChecker.CheckUpvotes("me_irl");
					break;
					case 2:
						RedditDownloader rd = new RedditDownloader();
						rd.download();
					break;
					case 3:
						TesseractOCRProcessor tp = new TesseractOCRProcessor();
						tp.OCRProcess();
					break;
					default:
						System.out.println("Thats a stupid option");
				}
			}
			
			//Runtime rt = Runtime.getRuntime();
			//Process pr = rt.exec("/usr/local/bin/tesseract /tmp/images/test.png /tmp/images/memeprocessoroutput");
			
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
		};
	}
}
