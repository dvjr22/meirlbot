package com.tmoon8730.api;

public class FlickrURL {
	private String apiURL = "https://api.flickr.com/services/";
	private String apiKey = "api_key=3934f355f1e98b57778363c4712d8ce1"; //TODO: Change this from hard coded
	private String returnFormat = "format=json";
	private String searchMethod = "?method=flickr.photos.search";
	private String apiMethod = "rest";
	
	private String staticURL1 = "https://farm";
	private String staticURL2 = ".staticflickr.com/";
	private String fileExtension = ".jpg";
	
	public String getSearchURL(String searchTerm){
		// URL Format:
		// apiURL apiMethod / searchMethod & returnFormat & apiKey & text= searchTerm
		// Example:
		// https://api.flickr.com/services/rest/?method=flickr.photos.search&format=json&api_key=3934f355f1e98b57778363c4712d8ce1&text=cat
		StringBuilder sb = new StringBuilder();
		sb.append(apiURL);
		sb.append(apiMethod);
		sb.append('/');
		sb.append(searchMethod);
		sb.append('&');
		sb.append(returnFormat);
		sb.append('&');
		sb.append(apiKey);
		sb.append('&');
		sb.append("&text=");
		sb.append(searchTerm);
		
		System.out.println("  [x] Built a URL of " + sb.toString());
		return sb.toString();
	}
	
	public String getStaticImageURL(String farmId, String serverId, String imageId, String imageSecret){
		// URL Format:
		// staticURL1 farmId staticURL2 serverId / iamgeId _ imageSecret fileExtension
		// Example:
		// https://farm1.staticflickr.com/329/31077294984_622875c01b.jpg
		StringBuilder sb = new StringBuilder();
		sb.append(staticURL1);
		sb.append(farmId);
		sb.append(staticURL2);
		sb.append(serverId);
		sb.append('/');
		sb.append(imageId);
		sb.append('_');
		sb.append(imageSecret);
		sb.append(fileExtension);
		
		System.out.println("  [x] Build a URL of " + sb.toString());
		return sb.toString();
	}
}
