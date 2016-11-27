package com.tmoon8730;

import java.util.List;

interface RedditPostService {
	RedditPost create(RedditPost post);
	RedditPost delete(String id);
	List<RedditPost> findAll();
	RedditPost findById(String redditId);
	RedditPost update(RedditPost post);
}
