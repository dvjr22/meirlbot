package com.tmoon8730.api;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpEntity;
import org.springframework.http.client.ClientHttpRequestFactory;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

public class RedditAPI {
	private static final Logger log = LoggerFactory.getLogger(RedditAPI.class);
	
	private final String APIURL = "http://127.0.0.1:8080/redditpost/";
	
	private RestTemplate restTemplate;
	
	public RedditAPI(){
		restTemplate = new RestTemplate();
	}

	public boolean getRedditPost(String redditId){
		String url = APIURL + "search/findByRedditId?redditId=" + redditId;
		log.info("using url " + url);
		RedditEmbedded post = restTemplate.getForObject(url, RedditEmbedded.class);
		if(post != null){
			log.info(post.toString());
			return true;
		}
		return false;
	}
	public boolean getRedditPost(){
		RedditEmbedded post = restTemplate.getForObject("http://127.0.0.1:8080/redditpost/", RedditEmbedded.class);
		if(post != null){
			log.info(post.toString());
			return true;
		}
		return false;
	}
	public void postRedditPost(RedditValue redditValue){
		ClientHttpRequestFactory requestFactory = getClientHttpRequestFactory();
		HttpEntity<RedditValue> request = new HttpEntity<>(redditValue);
		RedditValue returnedValue = restTemplate.postForObject(APIURL, request, RedditValue.class);
	}
	
	private ClientHttpRequestFactory getClientHttpRequestFactory(){
		 int timeout = 5000;
		    HttpComponentsClientHttpRequestFactory clientHttpRequestFactory =
		      new HttpComponentsClientHttpRequestFactory();
		    clientHttpRequestFactory.setConnectTimeout(timeout);
		    return clientHttpRequestFactory;
	}
}
