package com.tmoon8730.api;

import java.util.Arrays;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

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
	/**
	 * @return the id
	 */
	public String getId() {
		return id;
	}
	/**
	 * @param id the id to set
	 */
	public void setId(String id) {
		this.id = id;
	}
	/**
	 * @return the redditId
	 */
	public String getRedditId() {
		return redditId;
	}
	/**
	 * @param redditId the redditId to set
	 */
	public void setRedditId(String redditId) {
		this.redditId = redditId;
	}
	/**
	 * @return the upvotes
	 */
	public int getUpvotes() {
		return upvotes;
	}
	/**
	 * @param upvotes the upvotes to set
	 */
	public void setUpvotes(int upvotes) {
		this.upvotes = upvotes;
	}
	/**
	 * @return the upvoteTrend
	 */
	public int getUpvoteTrend() {
		return upvoteTrend;
	}
	/**
	 * @param upvoteTrend the upvoteTrend to set
	 */
	public void setUpvoteTrend(int upvoteTrend) {
		this.upvoteTrend = upvoteTrend;
	}
	/**
	 * @return the memeFlag
	 */
	public boolean isMemeFlag() {
		return memeFlag;
	}
	/**
	 * @param memeFlag the memeFlag to set
	 */
	public void setMemeFlag(boolean memeFlag) {
		this.memeFlag = memeFlag;
	}
	/**
	 * @return the imageUrl
	 */
	public String getImageUrl() {
		return imageUrl;
	}
	/**
	 * @param imageUrl the imageUrl to set
	 */
	public void setImageUrl(String imageUrl) {
		this.imageUrl = imageUrl;
	}
	/**
	 * @return the imageLocation
	 */
	public String getImageLocation() {
		return imageLocation;
	}
	/**
	 * @param imageLocation the imageLocation to set
	 */
	public void setImageLocation(String imageLocation) {
		this.imageLocation = imageLocation;
	}
	/**
	 * @return the memeLocation
	 */
	public String getMemeLocation() {
		return memeLocation;
	}
	/**
	 * @param memeLocation the memeLocation to set
	 */
	public void setMemeLocation(String memeLocation) {
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
