package com.tmoon8730;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

@RepositoryRestResource(collectionResourceRel = "redditpost", path = "redditpost")
public interface RedditPostRepository extends MongoRepository<RedditPost, String> {

	List<RedditPost> findByRedditId(@Param("redditId") String redditId);
	List<RedditPost> findByMemeFlag(@Param("memeFlag") boolean memeFlag);
}
