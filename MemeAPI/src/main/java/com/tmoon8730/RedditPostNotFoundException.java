package com.tmoon8730;

public class RedditPostNotFoundException extends RuntimeException{
	public RedditPostNotFoundException(String id) {
        super(String.format("No redditpost entry found with id: <%s>", id));
    }
}
