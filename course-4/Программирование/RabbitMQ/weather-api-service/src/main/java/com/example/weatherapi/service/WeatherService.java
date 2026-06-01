package com.example.weatherapi.service;

import com.example.weatherapi.dto.AggregatedWeatherReport;
import com.example.weatherapi.dto.WeatherMessage;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

@Service
@RequiredArgsConstructor
@Slf4j
public class WeatherService {

    private final RabbitTemplate rabbitTemplate;

    @Value("${rabbitmq.exchange.weather}")
    private String exchange;

    @Value("${rabbitmq.routing-key.request}")
    private String requestRoutingKey;

    private final ConcurrentHashMap<String, CompletableFuture<AggregatedWeatherReport>> pendingRequests = new ConcurrentHashMap<>();

    public AggregatedWeatherReport processWeatherRequest(List<String> cities) {
        String correlationId = UUID.randomUUID().toString();
        log.info("Processing request for cities: {} with correlationId: {}", cities, correlationId);

        CompletableFuture<AggregatedWeatherReport> future = new CompletableFuture<>();
        pendingRequests.put(correlationId, future);

        for (String city : cities) {
            WeatherMessage message = new WeatherMessage(city, correlationId, cities.size());
            rabbitTemplate.convertAndSend(exchange, requestRoutingKey, message);
        }

        try {
            // Wait for the aggregated report with a timeout (e.g., 60 seconds)
            return future.get(60, TimeUnit.SECONDS);
        } catch (InterruptedException | ExecutionException | TimeoutException e) {
            log.error("Error waiting for aggregated report", e);
            pendingRequests.remove(correlationId);
            throw new RuntimeException("Failed to get weather forecast", e);
        }
    }

    @RabbitListener(queues = "${rabbitmq.queue.aggregated}")
    public void receiveAggregatedReport(AggregatedWeatherReport report) {
        log.info("Received aggregated report for correlationId: {}", report.getCorrelationId());
        CompletableFuture<AggregatedWeatherReport> future = pendingRequests.remove(report.getCorrelationId());
        if (future != null) {
            future.complete(report);
        } else {
            log.warn("Received report for unknown or timed-out correlationId: {}", report.getCorrelationId());
        }
    }
}
