package com.example.weatheraggregator.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class AggregatedWeatherReport {
    private String correlationId;
    private Map<String, Object> weatherData;
}
