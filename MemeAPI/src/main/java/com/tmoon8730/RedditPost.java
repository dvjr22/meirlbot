package com.tmoon8730;

import org.springframework.data.annotation.Id;

public class RedditPost {
	@Id private String id;
	private String redditId;
	private int upvotes;
	private int upvoteTrend;
	private boolean memeFlag;
	private String imageLocation;
	private String memeLocation;
	
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

}
