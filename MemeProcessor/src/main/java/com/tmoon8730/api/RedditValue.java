package com.tmoon8730.api;

import java.util.Arrays;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class RedditValue {
	private String redditId;
	private int upvotes;
	private int upvoteTrend;
	private boolean memeFlag;
	private String imageLocation;
	private String memeLocation;
	private Links _links;

    public RedditValue(String redditId, int upvotes, int upvoteTrend, boolean memeFlag, String imageLocation,
			String memeLocation) {
		super();
		this.redditId = redditId;
		this.upvotes = upvotes;
		this.upvoteTrend = upvoteTrend;
		this.memeFlag = memeFlag;
		this.imageLocation = imageLocation;
		this.memeLocation = memeLocation;
	}

	public RedditValue() {
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

	/**
	 * @return the _links
	 */
	public Links get_links() {
		return _links;
	}

	/**
	 * @param _links the _links to set
	 */
	public void set_links(Links _links) {
		this._links = _links;
	}

	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return "RedditValue [redditId=" + redditId + ", upvotes=" + upvotes + ", upvoteTrend=" + upvoteTrend
				+ ", memeFlag=" + memeFlag + ", imageLocation=" + imageLocation + ", memeLocation=" + memeLocation
				+ ", _links=" + _links + "]";
	}



}
