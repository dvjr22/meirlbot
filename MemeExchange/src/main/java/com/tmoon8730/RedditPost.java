package com.tmoon8730;

import javax.persistence.Entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import lombok.Data;

@Data
@Entity
@JsonIgnoreProperties(ignoreUnknown = true)
public class RedditPost {
	private String id;
	private String redditId;
	private int upvotes;
	private int upvoteTrend;
	private boolean memeFlag;
	private String imageUrl;
	private String imageLocation;
	private String memeLocation;
		
	public RedditPost(){
		super();
		this.id = "0a";
		this.redditId = "0a";
		this.upvotes = 0;
		this.upvoteTrend = 0;
		this.memeFlag = false;
		this.imageUrl = "";
		this.imageLocation = "";
		this.memeLocation = "";
	}
	
	public RedditPost(String id, String redditId, int upvotes, int upvoteTrend, boolean memeFlag, String imageUrl,
			String imageLocation, String memeLocation) {
		super();
		this.id = id;
		this.redditId = redditId;
		this.upvotes = upvotes;
		this.upvoteTrend = upvoteTrend;
		this.memeFlag = memeFlag;
		this.imageUrl = imageUrl;
		this.imageLocation = imageLocation;
		this.memeLocation = memeLocation;
	}
	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return "RedditPost [id=" + id + ", redditId=" + redditId + ", upvotes=" + upvotes + ", upvoteTrend="
			+ upvoteTrend + ", memeFlag=" + memeFlag + ", imageUrl=" + imageUrl + ", imageLocation=" + imageLocation
			+ ", memeLocation=" + memeLocation+ "]";
	}
}
