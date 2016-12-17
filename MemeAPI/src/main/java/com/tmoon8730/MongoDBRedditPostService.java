package com.tmoon8730;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
class MongoDBRedditPostService implements RedditPostService {
	
	private static final Logger log = LoggerFactory.getLogger(MongoDBRedditPostService.class);
	
	@Autowired
	RedditPostRepository repository;
	
	/**
	 * A method to create a new entry in the database
	 * @param post a RedditPost to create
	 */
	@Override
	public RedditPost create(RedditPost post) {
		log.info("In create with id value + " + post.getId() + " and post value" + post.toString());
		// New object to create
		RedditPost persisted = new RedditPost(  post.getId(),
												post.getRedditId(),
												post.getUpvotes(),
												post.getUpvoteTrend(),
												post.isMemeFlag(),
												post.getImageUrl(),
												post.getImageLocation(),
												post.getMemeLocation()
											);
		// Create the object using the RedditPostRepository
		persisted = repository.save(persisted);
		// Return the created post
		return persisted;
	}

	/**
	 * A method to delete an entry from the database
	 * @param id the id of the object to delete
	 */
	@Override
	public RedditPost delete(String id) {
		log.info("In delete with id value " + id);
		// Find the object to delete
		RedditPost deleted = findRedditPostById(id);
		// Delete the object by using the RedditPostRepository
		repository.delete(deleted);
		// Return the deleted object
		return deleted;
	}

	/**
	 * A method that returns a list of RedditPost objects 
	 * for all the entries in the database
	 */
	@Override
	public List<RedditPost> findAll() {
		log.info("In findAll");
		// Get a list of all the entries by using the RedditPostRepository
		List<RedditPost> redditEntries = findAllRedditPosts();
		// Return the list
		return redditEntries;
	}

	/**
	 * A method to update an existing entry in the database
	 * @param post the RedditPost of the object to update
	 */
	@Override
	public RedditPost update(RedditPost post) {
		// Local variable for the id of the updated post
		String id = post.getId();
		log.info("In update with id value " + id  + " and post value " + post.toString());
		// If the item exists then delete the existing item 
		// so that it wont have a duplicated record
		if(repository.exists(id)){
			// The element already exists so delete the existing element and add in the new element
			RedditPost updated = findRedditPostById(post.getId());
			repository.delete(updated);
		}
		// Save the entry using the RedditPostRepository
		post = repository.save(post);
		log.info("Update operation changed id from " + id + " to " + post.getId());
		return post;
	}
	
	/**
	 * A method to find a specific entry with a given id
	 * @param id the id of the post to find
	 */
	@Override
	public RedditPost findById(String id) {
		log.info("in findById with id value " + id);
		// Return the found entry
		return findRedditPostById(id);
	}
	
	/**
	 * A method to find a specific entry with a given redditId
	 * @param redditId the redditId of the post to find
	 */
	@Override
	public RedditPost findByRedditId(String redditId){
		log.info("In findByRedditId with redditId value " + redditId);
		// Find all the values to search for the given redditId
		List<RedditPost> posts = repository.findAll();
		// A new post to return
		RedditPost returnValue = new RedditPost();
		// Search through the posts for one matching the redditId
		for(RedditPost p : posts){
			boolean exit = false;
			if(p.getRedditId().equals(redditId))
			{
				returnValue = p;
				exit = true;
			}
			// Once an entry is found the exit and stop searching
			if(exit)
				break;
		}
		// TODO: If a value isn't found the throw an error
		return returnValue;
	}
	
	// Private methods
	public RedditPost findRedditPostById(String id){
		RedditPost result = repository.findOne(id);
		return result;
	}
	public List<RedditPost> findAllRedditPosts(){
		List<RedditPost> posts = repository.findAll();
		return posts;
	}
}
