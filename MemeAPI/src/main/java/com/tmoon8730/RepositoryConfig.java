package com.tmoon8730;

import org.springframework.data.rest.core.config.RepositoryRestConfiguration;
import org.springframework.data.rest.webmvc.config.RepositoryRestMvcConfiguration;

public class RepositoryConfig extends RepositoryRestMvcConfiguration{
	/**
	 * This override exposes the ID bean from the RedditPost 
	 * class. This allows for searching via the id.
	 */
	@Override
	protected  void configureRepositoryRestConfiguration(RepositoryRestConfiguration config){
		config.exposeIdsFor(RedditPost.class);
	}
}
