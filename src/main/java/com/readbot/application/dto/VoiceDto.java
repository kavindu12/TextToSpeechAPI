package com.readbot.application.dto;

public class VoiceDto {
	
	private final String name;
	private final String gender;
	private final String language;
	
	
	public VoiceDto(String name, String gender, String language) {
		super();
		this.name = name;
		this.gender = gender;
		this.language = language;
	}


	public String getName() {
		return name;
	}


	public String getGender() {
		return gender;
	}


	public String getLanguage() {
		return language;
	}	

}
