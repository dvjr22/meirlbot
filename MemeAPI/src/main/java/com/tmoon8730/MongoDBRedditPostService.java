package com.tmoon8730;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
final class MongoDBRedditPostService implements RedditPostService {
	private final RedditPostRepository repository;
	@Autowired
	MongoDBRedditPostService(RedditPostRepository repository){
		this.repository = repository;
	}
	@Override
	public RedditPost create(RedditPost post) {
		RedditPost persisted = new RedditPost(  post.getId(),
												post.getRedditId(),
												post.getUpvotes(),
												post.getUpvoteTrend(),
												post.isMemeFlag(),
												post.getImageUrl(),
												post.getImageLocation(),
												post.getMemeLocation()
											);
		persisted = repository.save(persisted);
		return persisted;
	}

	@Override
	public RedditPost delete(String id) {
		RedditPost deleted = findRedditPostById(id);
		repository.delete(deleted);
		return deleted;
	}

	@Override
	public List<RedditPost> findAll() {
		List<RedditPost> redditEntries = repository.findAll();
		return redditEntries;
	}

	@Override
	public RedditPost update(RedditPost post) {
		String id = post.getId();
		if(repository.exists(id)){
			// The element already exists so delete the existing element and add in the new element
			RedditPost updated = findRedditPostById(post.getId());
			repository.delete(updated);
		}
		post = repository.save(post);
		System.out.println("  [x] Update operation changed id from " + id + " to " + post.getId());
		return post;
	}
	
	// Private methods
	private RedditPost findRedditPostById(String id){
		RedditPost result = repository.findOne(id);
		return result;
	}
	/*private RedditPost findRedditPost(String redditId){
		Optional<RedditPost> result = repository.findById(redditId);
		return result.orElseThrow(() -> new RedditPostNotFoundException(redditId));
	}*/
	@Override
	public RedditPost findById(String redditId) {
		return findRedditPostById(redditId);
	}
	
	@Override
	public RedditPost findByRedditId(String redditId){
		System.out.println("  [x] In findByRedditId");
		List<RedditPost> posts = repository.findAll();
		RedditPost returnValue = new RedditPost();
		for(RedditPost p : posts){
			System.out.println("  [x] Comparing " + p.getRedditId() + " " + redditId);
			boolean exit = false;
			if(p.getRedditId().equals(redditId))
			{
				returnValue = p;
				System.out.println("  [x] Found an item for the redditId " + redditId + " with the id of " + p.getId());
				exit = true;
			}
			if(exit)
				break;
		}
		return returnValue;
	}
}
