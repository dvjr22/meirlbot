package com.tmoon8730;

import org.springframework.data.rest.core.config.RepositoryRestConfiguration;
import org.springframework.data.rest.webmvc.config.RepositoryRestMvcConfiguration;

public class RepositoryConfig extends RepositoryRestMvcConfiguration{
	@Override
	protected  void configureRepositoryRestConfiguration(RepositoryRestConfiguration config){
		config.exposeIdsFor(RedditPost.class);
	}
}
