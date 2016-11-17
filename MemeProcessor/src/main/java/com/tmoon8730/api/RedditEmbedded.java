package com.tmoon8730.api;

public class RedditEmbedded {
	private RedditPost _embedded;
	/**
	 * @return the _embedded
	 */
	public RedditPost get_embedded() {
		return _embedded;
	}

	/**
	 * @param _embedded the _embedded to set
	 */
	public void set_embedded(RedditPost _embedded) {
		this._embedded = _embedded;
	}
	
	@Override
	public String toString() {
		return "RedditEmbedded [_embedded=" + _embedded + "]";
	}
}
