package com.example.weatheraggregator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class WeatherAggregatorApplication {

	public static void main(String[] args) {
		SpringApplication.run(WeatherAggregatorApplication.class, args);
	}

}
