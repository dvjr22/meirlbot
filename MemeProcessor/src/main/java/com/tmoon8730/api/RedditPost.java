package com.tmoon8730.api;

import java.util.Arrays;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class RedditPost {
	private RedditValue[] redditpost;
	
	
	public RedditPost(){
	}
	
	/**
	 * @return the redditpost
	 */
	public RedditValue[] getRedditpost() {
		return redditpost;
	}

	/**
	 * @param redditpost the redditpost to set
	 */
	public void setRedditpost(RedditValue[] redditpost) {
		this.redditpost = redditpost;
	}

	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return "RedditPost [redditpost=" + Arrays.toString(redditpost) + "]";
	}
}
