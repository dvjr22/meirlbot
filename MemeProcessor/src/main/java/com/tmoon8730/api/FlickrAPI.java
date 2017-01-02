package com.tmoon8730.api;

import java.io.IOException;
import java.util.List;

import org.springframework.http.MediaType;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.collect.ImmutableList;

public class FlickrAPI {
	
	private FlickrURL flickrURL;
	private RestTemplate restTemplate;
	public FlickrAPI(){
		flickrURL = new FlickrURL();
		restTemplate = new RestTemplate(new HttpComponentsClientHttpRequestFactory());
	    List<HttpMessageConverter<?>> converters = restTemplate.getMessageConverters();
	    for (HttpMessageConverter<?> converter : converters) {
	        if (converter instanceof MappingJackson2HttpMessageConverter) {
	            MappingJackson2HttpMessageConverter jsonConverter = (MappingJackson2HttpMessageConverter) converter;
	            jsonConverter.setObjectMapper(new ObjectMapper());
	            jsonConverter.setSupportedMediaTypes(ImmutableList.of(new MediaType("*", "json", MappingJackson2HttpMessageConverter.DEFAULT_CHARSET), new MediaType("*", "javascript", MappingJackson2HttpMessageConverter.DEFAULT_CHARSET)));		        }
	    }
	}
	

	public String getForTerm(String searchTerm){
		String url = flickrURL.getSearchURL(searchTerm);
		String response = restTemplate.getForObject(url, String.class);
		// Trim off JSON-P structure by removing the first 14 characters and the last character
		response = response.substring(86);
		response = response.substring(0,response.length()-15);
		
		ObjectMapper mapper = new ObjectMapper();
		FlickrPhoto[] photos = null;
		try {
			photos = mapper.readValue(response, FlickrPhoto[].class);
			for(FlickrPhoto p : photos){
				System.out.println(p.toString());
			}
		} catch (JsonParseException e) {
			e.printStackTrace();
		} catch (JsonMappingException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		String imageURL = null;
		try{
			FlickrPhoto firstResult = photos[0];
			imageURL = flickrURL.getStaticImageURL(firstResult.getFarm(), firstResult.getServer(), firstResult.getId(), firstResult.getSecret());
		}catch(Exception e){
			e.printStackTrace();
		}
		System.out.println("  [x] returning: " + imageURL);
		return imageURL;
	}
}
