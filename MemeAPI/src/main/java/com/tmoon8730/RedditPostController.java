package com.tmoon8730;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/redditpost")
public class RedditPostController {
	private final RedditPostService service;
	
	@Autowired
	RedditPostController(RedditPostService service){
		this.service = service;
	}
	
	@RequestMapping(method = RequestMethod.POST)
	@ResponseStatus(HttpStatus.CREATED)
	RedditPost create(@RequestBody RedditPost post){
		return service.create(post);
	}
	
	@RequestMapping(value = "{id}", method = RequestMethod.DELETE)
	RedditPost delete(@PathVariable("id") String id){
		return service.delete(id);
	}
	
	@RequestMapping(method = RequestMethod.GET)
	List<RedditPost> findAll(){
		return service.findAll();
	}
	@RequestMapping(value = "{id}", method = RequestMethod.GET)
	RedditPost findById(@PathVariable("id") String id){
		return service.findById(id);
	}
	
	@RequestMapping(value = "{id}", method = RequestMethod.PUT)
	RedditPost update(@RequestBody RedditPost post){
		return service.update(post);
	}
	
	@ExceptionHandler
	@ResponseStatus(HttpStatus.NOT_FOUND)
	public void handleRedditPostNotFound(RedditPostNotFoundException e){
	}
}
