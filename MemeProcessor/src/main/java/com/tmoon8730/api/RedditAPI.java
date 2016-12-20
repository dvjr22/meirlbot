package com.tmoon8730.api;

import java.util.HashMap;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

public class RedditAPI {
	private static final Logger log = LoggerFactory.getLogger(RedditAPI.class);
	
	private final String APIURL = "http://127.0.0.1:8090/api/redditpost/";
	
	private RestTemplate restTemplate;
	
	public RedditAPI(){
		restTemplate = new RestTemplate();
	}
	
	
	// Post operation to create new post
	public RedditPost createPost(RedditPost post){
		log.info("Trying " + APIURL + post.getId());
		String uri = APIURL + "{id}";
		Map<String, String> params = new HashMap<String,String>();
		params.put("id", post.getId());
		RedditPost returnedPost = restTemplate.postForObject(uri, post, RedditPost.class, params);
		return returnedPost;
	}
	
	// Put operation
	public void updatePost(RedditPost post){
		log.info("Trying " + APIURL + post.getId());
		String uri = APIURL + "{id}";
		Map<String, String> params = new HashMap<String,String>();
		params.put("id", post.getId());
		restTemplate.put(uri, post, params);
	}
	
	// Get operation for one entry
	public RedditPost getPost(String id){
		log.info("Trying " + APIURL + id);
		return restTemplate.getForObject(APIURL + id, RedditPost.class);
	}
	public RedditPost getPostForRedditId(String redditId){
		log.info("Trying " + APIURL + "redditId/" + redditId);
		return restTemplate.getForObject(APIURL + "redditId/" + redditId, RedditPost.class);
	}
	
	// Get operation for all entries
	public RedditPost[] getAllPosts(){
		log.info("Trying " + APIURL);
		ResponseEntity<RedditPost[]> response = restTemplate.getForEntity(APIURL, RedditPost[].class);
		return response.getBody();
	}
	
	// Delete operation for one entry
	public void deletePost(String id){
		log.info("Tryign " + APIURL + id);
		restTemplate.delete(APIURL + id);
	}
}
