package com.tmoon8730;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/redditpost")
public class RedditPostController {
	@Autowired
	RedditPostService service;
	
	// Get Methods
	@RequestMapping(method = RequestMethod.GET)
	List<RedditPost> findAll(){
		return service.findAll();
	}
	@RequestMapping(value = "{id}", method = RequestMethod.GET)
	RedditPost findById(@PathVariable("id") String id){
		return service.findById(id);
	}
	
	// Delete Methods
	@RequestMapping(value = "{id}", method = RequestMethod.DELETE)
	RedditPost delete(@PathVariable("id") String id){
		return service.delete(id);
	}	
	
	// Post methods
	@RequestMapping(value="{id}", method = RequestMethod.POST)
	@ResponseStatus(HttpStatus.CREATED)
	ResponseEntity<RedditPost> create(@PathVariable("id") String id, @RequestBody RedditPost post){
		service.create(post);
		System.out.println(id);
		System.out.println(post.toString());
		
		return new ResponseEntity<RedditPost>(post, HttpStatus.OK);
	}
	
	// Put Methods
	@RequestMapping(value = "{id}", method = RequestMethod.PUT)
	ResponseEntity<RedditPost> update(@PathVariable("id") String id, @RequestBody RedditPost post){
		service.update(post);
		System.out.println(id);
		System.out.println(post.toString());
		
		return new ResponseEntity<RedditPost>(post, HttpStatus.OK);
	}
	
	@ExceptionHandler
	@ResponseStatus(HttpStatus.NOT_FOUND)
	public void handleRedditPostNotFound(RedditPostNotFoundException e){
	}
}
