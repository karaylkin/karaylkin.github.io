package com.example.weatherapi.controller;

import com.example.weatherapi.dto.AggregatedWeatherReport;
import com.example.weatherapi.dto.WeatherRequestDto;
import com.example.weatherapi.service.WeatherService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/weather")
@RequiredArgsConstructor
@CrossOrigin(origins = "*") // Allow frontend access
public class WeatherController {

    private final WeatherService weatherService;

    @PostMapping("/forecast")
    public ResponseEntity<AggregatedWeatherReport> getWeatherForecast(@RequestBody WeatherRequestDto request) {
        AggregatedWeatherReport report = weatherService.processWeatherRequest(request.getCities());
        return ResponseEntity.ok(report);
    }
}
