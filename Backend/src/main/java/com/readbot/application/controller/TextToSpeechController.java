package com.readbot.application.controller;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;

import javax.annotation.PreDestroy;

import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.google.api.gax.core.FixedCredentialsProvider;
import com.google.auth.oauth2.ServiceAccountCredentials;
import com.google.cloud.texttospeech.v1beta1.AudioConfig;
import com.google.cloud.texttospeech.v1beta1.AudioEncoding;
import com.google.cloud.texttospeech.v1beta1.ListVoicesRequest;
import com.google.cloud.texttospeech.v1beta1.ListVoicesResponse;
import com.google.cloud.texttospeech.v1beta1.SynthesisInput;
import com.google.cloud.texttospeech.v1beta1.SynthesizeSpeechResponse;
import com.google.cloud.texttospeech.v1beta1.TextToSpeechClient;
import com.google.cloud.texttospeech.v1beta1.TextToSpeechSettings;
import com.google.cloud.texttospeech.v1beta1.Voice;
import com.google.cloud.texttospeech.v1beta1.VoiceSelectionParams;
import com.google.protobuf.ByteString;
import com.readbot.application.config.AppConfig;
import com.readbot.application.dto.VoiceDto;
import com.readbot.application.textTospeech.ReadSummary;

@Controller
@CrossOrigin
@RequestMapping("/textToSpeech/")
public class TextToSpeechController {
	
	private TextToSpeechClient textToSpeechClient;
	
	private ReadSummary readSummary;
	
	public TextToSpeechController(AppConfig appConfig) {
		
		try {
			
			ServiceAccountCredentials credentials = ServiceAccountCredentials
			          .fromStream(Files.newInputStream(Paths.get(appConfig.getCredentialsPath())));
			      TextToSpeechSettings settings = TextToSpeechSettings.newBuilder()
			          .setCredentialsProvider(FixedCredentialsProvider.create(credentials)).build();
			      this.textToSpeechClient = TextToSpeechClient.create(settings);
			
		} catch (Exception e) {
			LoggerFactory.getLogger(TextToSpeechController.class)
	          .error("init TextToSpeechController", e);
		}
		
	}
	
	  @PreDestroy
	  public void destroy() throws Exception {
	    if (this.textToSpeechClient != null) {
	      this.textToSpeechClient.close();
	    }
	  }

	
	@GetMapping("/voice/")
	public List<VoiceDto> getAllVoices() {
	    ListVoicesRequest request = ListVoicesRequest.getDefaultInstance();
	    ListVoicesResponse listreponse = this.textToSpeechClient.listVoices(request);
	    return listreponse.getVoicesList().stream()
	        .map(voice -> new VoiceDto(getSupportedLanguage(voice), voice.getName(),
	            voice.getSsmlGender().name()))
	        .collect(Collectors.toList());
	    
	}
	
	  @PostMapping("/speak")
	  public void speak(@RequestBody String userData) throws Exception {

//	    SynthesisInput input = SynthesisInput.newBuilder().setText(text).build();
//
//	    VoiceSelectionParams voiceSelection = VoiceSelectionParams.newBuilder()
//	        .setLanguageCode(language).setName(voice).build();
//
//	    AudioConfig audioConfig = AudioConfig.newBuilder().setPitch(pitch)
//	        .setSpeakingRate(speakingRate).setAudioEncoding(AudioEncoding.MP3).build();
//
//	    SynthesizeSpeechResponse response = this.textToSpeechClient.synthesizeSpeech(input,
//	        voiceSelection, audioConfig);
	    
	    readSummary.saveAudio(userData);

	  }
	
	private static String getSupportedLanguage(Voice voice) {
		List<ByteString> languageCodes = voice.getLanguageCodesList().asByteStringList();
		for (ByteString languageCode : languageCodes) {
			return languageCode.toStringUtf8();
		}
		return null;
	}
	  

}
