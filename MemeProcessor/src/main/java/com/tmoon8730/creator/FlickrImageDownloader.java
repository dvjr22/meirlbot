package com.tmoon8730.creator;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import javax.imageio.ImageIO;

public class FlickrImageDownloader{
	public FlickrImageDownloader(){
		
	}
	public void downloadImage(String url){
		BufferedImage image = null;
		try{
			URL Url = new URL(url);
			image = ImageIO.read(Url);
			if(image != null){
				String filename = url.replace('/', '_').replace(':','_').substring(4);
				ImageIO.write(image, "jpg", new File("/tmp/images/" + filename));
			}
		}catch(IOException e){
			e.printStackTrace();
		}
	}
}
