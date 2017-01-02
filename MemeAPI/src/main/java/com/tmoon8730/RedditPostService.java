package com.tmoon8730;

import java.util.List;

interface RedditPostService {
	RedditPost create(RedditPost post);           // Create a new entry in the database
	RedditPost delete(String id);                 // Delete an entry
	List<RedditPost> findAll();                   // Return all the entries in the database
	RedditPost findById(String id);               // Find an entry by its id
	RedditPost findByRedditId(String redditId);   // Find an entry by its redditId tag
	RedditPost update(RedditPost post);           // Update an entry
}
