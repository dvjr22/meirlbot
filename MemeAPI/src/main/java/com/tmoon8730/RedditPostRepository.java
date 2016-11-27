package com.tmoon8730;

import java.util.List;
import java.util.Optional;

import org.springframework.data.repository.Repository;

interface RedditPostRepository extends Repository<RedditPost,String>{
	void delete(RedditPost deleted);		  // Delete a document
	List<RedditPost> findAll();               // Get all the documents
	Optional<RedditPost> findOne(String redditId);  // Find one document with the id
	RedditPost save(RedditPost saved); 		  // Save a document
}
