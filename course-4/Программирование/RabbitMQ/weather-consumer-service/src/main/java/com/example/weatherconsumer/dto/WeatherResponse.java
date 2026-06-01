package com.example.weatherconsumer.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class WeatherResponse {
    private String city;
    private String correlationId;
    private int totalCities;
    private Double temperature;
    private String description;
    private String error;
}
