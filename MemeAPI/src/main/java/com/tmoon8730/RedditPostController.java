package com.tmoon8730;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/redditpost")
public class RedditPostController {

	private static final Logger log = LoggerFactory.getLogger(RedditPostController.class);
	
	// Create the RedditPostService
	@Autowired
	RedditPostService service;
	
	// Get Methods
	@RequestMapping(method = RequestMethod.GET)
	List<RedditPost> findAll(){
		log.info("In findAll");
		return service.findAll();
	}
	
	// Get for entity with specific id
	@RequestMapping(value = "{id}", method = RequestMethod.GET)
	RedditPost findById(@PathVariable("id") String id){
		log.info("In findById with id value " + id);
		return service.findById(id);
	}
	
	// Get for entity with specific redditId
	@RequestMapping(value = "/redditId/{redditId}", method = RequestMethod.GET)
	RedditPost findByRedditId(@PathVariable("redditId") String redditId){
		log.info("In findById with redditId value " + redditId);
		return service.findByRedditId(redditId);
	}
	
	// Delete Methods
	@RequestMapping(value = "{id}", method = RequestMethod.DELETE)
	RedditPost delete(@PathVariable("id") String id){
		log.info("In delete with id value " + id);
		return service.delete(id);
	}	
	
	// Post methods
	@RequestMapping(value="{id}", method = RequestMethod.POST)
	@ResponseStatus(HttpStatus.CREATED)
	ResponseEntity<RedditPost> create(@PathVariable("id") String id, @RequestBody RedditPost post){
		log.info("In create with id value " + id + " and post value " + post.toString());
		service.create(post);
		return new ResponseEntity<RedditPost>(post, HttpStatus.OK);
	}
	
	// Put Methods
	@RequestMapping(value = "{id}", method = RequestMethod.PUT)
	ResponseEntity<RedditPost> update(@PathVariable("id") String id, @RequestBody RedditPost post){
		log.info("In update with id value " + id + " and post value " + post.toString());
		service.update(post);
		return new ResponseEntity<RedditPost>(post, HttpStatus.OK);
	}
}
