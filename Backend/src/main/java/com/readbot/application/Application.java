package com.readbot.application;

import java.io.FileOutputStream;
import java.io.OutputStream;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.google.cloud.texttospeech.v1beta1.AudioConfig;
import com.google.cloud.texttospeech.v1beta1.AudioEncoding;
import com.google.cloud.texttospeech.v1beta1.SsmlVoiceGender;
import com.google.cloud.texttospeech.v1beta1.SynthesisInput;
import com.google.cloud.texttospeech.v1beta1.SynthesizeSpeechResponse;
import com.google.cloud.texttospeech.v1beta1.TextToSpeechClient;
import com.google.cloud.texttospeech.v1beta1.VoiceSelectionParams;
import com.google.protobuf.ByteString;

@SpringBootApplication
public class Application {

	public static void main(String[] args) throws Exception {
		SpringApplication.run(Application.class, args);
//		startBot();
		
	}
	
	public static void startBot() throws Exception {
 
        String text = "What is a verb";
        String outputAudioFilePath = "C:\\Users\\kavindu\\Desktop\\application\\output.mp3";
 
        try (TextToSpeechClient textToSpeechClient = TextToSpeechClient.create()) {
            // Set the text input to be synthesized
            SynthesisInput input = SynthesisInput.newBuilder().setText(text).build();
 
            // Build the voice request; languageCode = "en_us"
            VoiceSelectionParams voice = VoiceSelectionParams.newBuilder().setLanguageCode("en-US")
                    .setSsmlGender(SsmlVoiceGender.FEMALE)
                    .build();
 
            // Select the type of audio file you want returned
            AudioConfig audioConfig = AudioConfig.newBuilder().setAudioEncoding(AudioEncoding.MP3) // MP3 audio.
                    .build();
 
            // Perform the text-to-speech request
            SynthesizeSpeechResponse response = textToSpeechClient.synthesizeSpeech(input, voice, audioConfig);
 
            // Get the audio contents from the response
            ByteString audioContents = response.getAudioContent();
 
            // Write the response to the output file.
            try (OutputStream out = new FileOutputStream(outputAudioFilePath)) {
                out.write(audioContents.toByteArray());
                System.out.println("Audio content written to file \"output.mp3\"");
            }
        }
    }


}
