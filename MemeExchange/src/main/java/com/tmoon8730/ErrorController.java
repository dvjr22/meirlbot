package com.tmoon8730;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

public class ErrorController {
	@Controller
	public class ImagesController {
		
		@RequestMapping("/error")
		public String error(){
			return "error";
		}
	}

}
