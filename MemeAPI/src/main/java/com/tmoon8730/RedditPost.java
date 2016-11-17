package com.tmoon8730;

import org.springframework.data.annotation.Id;

public class RedditPost {
	@Id private String id;
	
	private String redditId;
	private int upvote;
	private int upvoteTrend;
	private Boolean memeFlag;
	private String imageLocation;
	private String memeLocation;
	public String getRedditId() {
		return redditId;
	}
	public void setRedditId(String redditId) {
		this.redditId = redditId;
	}
	public int getUpvote() {
		return upvote;
	}
	public void setUpvote(int upvote) {
		this.upvote = upvote;
	}
	public int getUpvoteTrend() {
		return upvoteTrend;
	}
	public void setUpvoteTrend(int upvoteTrend) {
		this.upvoteTrend = upvoteTrend;
	}
	public Boolean getMemeFlag() {
		return memeFlag;
	}
	public void setMemeFlag(Boolean memeFlag) {
		this.memeFlag = memeFlag;
	}
	public String getImageLocation() {
		return imageLocation;
	}
	public void setImageLocation(String imageLocation) {
		this.imageLocation = imageLocation;
	}
	public String getMemeLocation() {
		return memeLocation;
	}
	public void setMemeLocation(String memeLocation) {
		this.memeLocation = memeLocation;
	}
}
