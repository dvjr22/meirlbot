package com.tmoon8730.api;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class FlickrPhoto {
	private String id;
	private String owner;
	private String secret;
	private String server;
	private String farm;
	private String title;
	private String ispublic;
	public FlickrPhoto(String id, String owner, String secret, String server, String farm, String title,
			String ispublic) {
		super();
		this.id = id;
		this.owner = owner;
		this.secret = secret;
		this.server = server;
		this.farm = farm;
		this.title = title;
		this.ispublic = ispublic;
	}
	public FlickrPhoto(){
		
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
	 * @return the owner
	 */
	public String getOwner() {
		return owner;
	}
	/**
	 * @param owner the owner to set
	 */
	public void setOwner(String owner) {
		this.owner = owner;
	}
	/**
	 * @return the secret
	 */
	public String getSecret() {
		return secret;
	}
	/**
	 * @param secret the secret to set
	 */
	public void setSecret(String secret) {
		this.secret = secret;
	}
	/**
	 * @return the server
	 */
	public String getServer() {
		return server;
	}
	/**
	 * @param server the server to set
	 */
	public void setServer(String server) {
		this.server = server;
	}
	/**
	 * @return the farm
	 */
	public String getFarm() {
		return farm;
	}
	/**
	 * @param farm the farm to set
	 */
	public void setFarm(String farm) {
		this.farm = farm;
	}
	/**
	 * @return the title
	 */
	public String getTitle() {
		return title;
	}
	/**
	 * @param title the title to set
	 */
	public void setTitle(String title) {
		this.title = title;
	}
	/**
	 * @return the ispublic
	 */
	public String getIspublic() {
		return ispublic;
	}
	/**
	 * @param ispublic the ispublic to set
	 */
	public void setIspublic(String ispublic) {
		this.ispublic = ispublic;
	}
	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return "FlickrPhoto [id=" + id + ", owner=" + owner + ", secret=" + secret + ", server=" + server + ", farm="
				+ farm + ", title=" + title + ", ispublic=" + ispublic + "]";
	}


}
