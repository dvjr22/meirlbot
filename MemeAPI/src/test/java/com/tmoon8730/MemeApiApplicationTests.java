package com.tmoon8730;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.mockito.Mockito.atLeastOnce;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.content;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.ArrayList;
import java.util.List;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.runners.MockitoJUnitRunner;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultMatcher;

@RunWith(MockitoJUnitRunner.class)
//@SpringBootTest
public class MemeApiApplicationTests {
	
	private static final Logger log = LoggerFactory.getLogger(MemeApiApplicationTests.class);
	
	//@Autowired
	//private RedditPostController postController;
	
	//private MockMvc mockMvc;
	
	/*@Before
	public void setup(){
		// Setup anything that needs to be initialized before the testing begins
		
		// Setup the mockmvc object to use the controller
		this.mockMvc = MockMvcBuilders.standaloneSetup(postController).build();
	}*/
	
	
	
	@Mock private RedditPostRepository repository;
	@Spy private MongoDBRedditPostService service;
	@InjectMocks private RedditPostController controller;
	
	@Autowired
	private MockMvc mockMvc;
	
	@Test
	public void testFindById() throws Exception{
		// Mock a RedditPost object to be returned by the repository
		RedditPost returnPost = mock(RedditPost.class);
		
		// Mock method returns to avoid calling the database
		doReturn(returnPost).when(service).findRedditPostById("test123");
		
		// Mock the return of the test variable to see if the new object is passed
		when(returnPost.isMemeFlag()).thenReturn(true);
		
		// Call the controller
		RedditPost testResult = controller.findById("test123");
		
		// Assertions to see if it worked
		assertNotNull(testResult);
		assertEquals(true,testResult.isMemeFlag());
		
		// Verify that the method was called
		verify(service, atLeastOnce()).findRedditPostById("test123");
	}
	
	@Test
	public void testFindAll() throws Exception{
		// Mock a RedditPost object to be returned by the repository
		RedditPost post1 = mock(RedditPost.class);
		RedditPost post2 = mock(RedditPost.class);
		
		List<RedditPost> posts = new ArrayList<RedditPost>();
		
		posts.add(post1);
		posts.add(post2);
		
		// Mock method returns to avoid calling the database
		doReturn(posts).when(service).findAllRedditPosts();
		
		// Call the controller
		List<RedditPost> testResults = controller.findAll();
		
		// Assertions to see if it worked
		assertNotNull(testResults);
		assertEquals(2,testResults.size());
		
		// Verify that the method was called
		verify(service, atLeastOnce()).findAll();
	}
	
	@Test
	public void contextLoads() {
	}

}
