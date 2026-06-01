package com.example.weatherconsumer.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class WeatherMessage {
    private String city;
    private String correlationId;
    private int totalCities;
}
