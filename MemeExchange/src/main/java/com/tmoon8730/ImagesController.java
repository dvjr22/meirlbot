package com.tmoon8730;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class ImagesController {
	
	@RequestMapping("/images")
	public String images(){
		return "images";
	}
}
