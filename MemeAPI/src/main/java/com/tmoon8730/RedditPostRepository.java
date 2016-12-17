package com.tmoon8730;

import java.util.List;
import java.util.Optional;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
interface RedditPostRepository extends CrudRepository<RedditPost,String>{
	void delete(RedditPost deleted);		  // Delete a document
	List<RedditPost> findAll();               // Get all the documents
	RedditPost findOne(String redditId);  // Find one document with the id
	RedditPost save(RedditPost saved); 		  // Save a document
	boolean exists(String id); // Checks if an element exists or not
}
