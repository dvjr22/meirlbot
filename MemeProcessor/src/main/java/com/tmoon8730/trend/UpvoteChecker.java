package com.tmoon8730.trend;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.tmoon8730.MemeProcessorApplication;
import com.tmoon8730.api.RedditAPI;
import com.tmoon8730.api.RedditPost;

import net.dean.jraw.RedditClient;
import net.dean.jraw.fluent.FluentRedditClient;
import net.dean.jraw.fluent.SubredditReference;
import net.dean.jraw.http.NetworkException;
import net.dean.jraw.http.UserAgent;
import net.dean.jraw.http.oauth.Credentials;
import net.dean.jraw.http.oauth.OAuthData;
import net.dean.jraw.http.oauth.OAuthException;
import net.dean.jraw.models.Listing;
import net.dean.jraw.models.LoggedInAccount;
import net.dean.jraw.models.Submission;

public class UpvoteChecker {
	private static final Logger log = LoggerFactory.getLogger(UpvoteChecker.class);
	
	private UserAgent userAgent;
	private RedditClient redditClient;
	private Credentials credentials;
	private OAuthData authData = null;
	private RedditAPI redditAPI;
	
	// Conditions that verify a meme to be processed
	private static int UPVOTEEXIT = 1000;
	private static int UPVOTETRENDEXIT = 1;
	
	public UpvoteChecker(){
		// TODO: Remove these hardcoded values
		userAgent = UserAgent.of("desktop","net.tmoon8730","v0.1","yeahboi");
		redditClient = new RedditClient(userAgent);
		credentials = Credentials.script("bmeirl","meirlbot","9V5mrAQyleSHZw","pRjdSYjTsptnWoDM0RVlwSk38tY");
		try {
			authData = redditClient.getOAuthHelper().easyAuth(credentials);
		} catch (NetworkException | OAuthException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		redditAPI = new RedditAPI();
	}// END: public UpvoteChecker...
	
	/**
	 * CheckUpvotes runs through all the hot posts on a subreddit and determines if each
	 * submission is in the database already or not. If the submission is already in the
	 * database then check if the upvote number needs to be updated and if the memeFlag
	 * needs to be changed. If the submission is not in the database then post it to the
	 * api to be added.
	 * @param subreddit
	 */
	public void CheckUpvotes(String subreddit){
		if(authData != null){
			redditClient.authenticate(authData);
			LoggedInAccount loggedInAccount = redditClient.me();
			log.info(loggedInAccount.getFullName());
			
			FluentRedditClient fluent = new FluentRedditClient(redditClient);
			SubredditReference subredditReference = fluent.subreddit(subreddit);
			Listing<Submission> listings = subredditReference.fetch();
			for(Submission sub : listings){
				// Loop through all the submissions and check if they exist in the 
				// database already. If they do exist then check if the upvotes 
				// need to be updated. If they do not exist then add it to the
				// database
				
				log.info(sub.getUrl());
				String subId = sub.getId();
				
				RedditPost post = redditAPI.getPostForRedditId(subId);
				
				//RedditPost redditEmbedded = redditAPI.getPostForRedditId(subId);
				log.info("Checking RedditPost: " + post.toString());
				
				if(alreadyExists(post)){
					// The document already exists so update the upvote count
					int newUpvote = sub.getScore();
					// Set the new upvotes from the submission
					post.setUpvotes(newUpvote);
					// Increment the upvotetrend 
					//TODO: Check if the upvotes are actaully trending up
					post.setUpvoteTrend(post.getUpvoteTrend() + 1); 
					// If the meme passes the exit condition then set the memeFlag to true so the processor can run
					post.setMemeFlag(checkMemeStatus(post));
					// Post the modified object to the REST API for database writing
					redditAPI.updatePost(post);
					log.info("Updated: " + post.toString());
				}else{
					// The document does not exist to create a new one
					int upvote = sub.getScore();
					String redditId = sub.getId();
					String imageUrl = sub.getUrl();
					// String redditId, int upvotes, int upvoteTrend, boolean memeFlag, String imageLocation,String memeLocation
					RedditPost postValue = new RedditPost("12345",redditId,upvote,0,false,imageUrl,"",""); //TODO: Figure out the id situation
					redditAPI.createPost(postValue);
					log.info("Created: " + postValue.toString());
				}
			}// END: for(Submission sub...
		}// END: if(authData...
	}// END: public void CheckUpvotes...
	
	/**
	 * AlreadyExists will return true if a document with the specified redditId exists
	 * and false if it does not exist
	 * @param redditId
	 */
	private boolean alreadyExists(RedditPost redditPost){
		if(redditAPI.getPostForRedditId(redditPost.getRedditId()) != new RedditPost()){
			log.info(redditPost.toString() + " is empty");
			return false;
		}
		return true;
	}// END: private boolean alreadyExists...
	
	/**
	 * checkMemeStatus returns true if the RedditValue passes the upvote and upvotetrend exit conditions as defined
	 * byt the constant values UPVOTEEXIT and UPVOTETRENDEXIT
	 * @param redditValue
	 * @return boolean
	 */
	private boolean checkMemeStatus(RedditPost redditValue){
		if(redditValue.getUpvotes() >= UPVOTEEXIT && redditValue.getUpvoteTrend() >= UPVOTETRENDEXIT){
			return true;
		}
		return false;
	}
}// END: public class UpvoteChecker...
