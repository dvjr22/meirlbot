package com.tmoon8730.creator;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;

public class KeywordProcessor {
	 public KeywordProcessor(){
		 
	 }
	 public ArrayList<String> generateKeyTerm(ArrayList<String> textFileNames){
		 // Main class for running through the files
		 ArrayList<String> data = new ArrayList<String>();
		 for(String s: textFileNames){
			 String rawData = loadFile(s); // Get the data from the text files
			 String cleanedData = cleanData(rawData); // Clean the data for junk text thrown in from the OCR
			 // Add the cleaned data to the array list only if its not equal to an empty string
			 if(!cleanedData.equals(""))
				 data.add(cleanedData);
		 }
		 return data;
	 }
	 private String loadFile(String filename){
		 // Read a text file from the parameter
		 String fileData = "";
		 try{
			 fileData = new String(Files.readAllBytes(Paths.get(filename)));
		 }catch(Exception e){
			 e.printStackTrace();
		 }
		 return fileData;
	 }
	 private String cleanData(String rawInput){
		 // Attempt to clean out junk text leftover from the OCR processor
		 String cleanedData = "";
		 // First remove the newline and return characters and replace them with spaces
		 cleanedData = rawInput.replaceAll("\\r\\n|\\r|\\n"," ");
		 // Second remove all special characters
		 cleanedData = cleanedData.replaceAll("[^\\p{Alnum}\\s]", "");
		 return cleanedData;
	 }
}
