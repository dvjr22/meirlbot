package com.tmoon8730.creator;

import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;

import javax.imageio.ImageIO;

public class TextWriter {
	public TextWriter(){
		
	}
	public void writeText(String imageLocation, String text){
		try {
			BufferedImage image = ImageIO.read(new URL(imageLocation));
			Graphics g = image.getGraphics();
			g.setFont(g.getFont().deriveFont(30f));
			g.drawString(text, 100, 100);
			g.dispose();
			
			String filename = imageLocation.replace('/', '_').replace(':','_').substring(4);
			ImageIO.write(image, "jpg", new File("/tmp/images/" + filename + "-final.jpg"));
			
		} catch (MalformedURLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
