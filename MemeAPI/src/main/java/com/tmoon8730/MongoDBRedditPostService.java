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
		RedditPost updated = findRedditPostById(post.getRedditId());
		updated = repository.save(updated);
		return updated;
	}
	
	// Private methods
	private RedditPost findRedditPostById(String id){
		Optional<RedditPost> result = repository.findOne(id);
		return result.orElseThrow(() -> new RedditPostNotFoundException(id));
	}
	/*private RedditPost findRedditPost(String redditId){
		Optional<RedditPost> result = repository.findById(redditId);
		return result.orElseThrow(() -> new RedditPostNotFoundException(redditId));
	}*/
	@Override
	public RedditPost findById(String redditId) {
		return findRedditPostById(redditId);
	}
}
