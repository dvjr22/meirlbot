package com.tmoon8730;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class AboutController {

	@RequestMapping("/about")
	public String about(@RequestParam(value="name", required = false, defaultValue="world") String name, Model model){
		model.addAttribute("name",name);
		return "about";
	}
}
