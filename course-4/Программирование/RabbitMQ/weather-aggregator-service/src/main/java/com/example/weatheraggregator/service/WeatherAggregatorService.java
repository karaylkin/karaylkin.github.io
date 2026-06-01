package com.example.weatheraggregator.service;

import com.example.weatheraggregator.dto.AggregatedWeatherReport;
import com.example.weatheraggregator.dto.WeatherResponse;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
@RequiredArgsConstructor
@Slf4j
public class WeatherAggregatorService {

    private final RabbitTemplate rabbitTemplate;

    @Value("${rabbitmq.exchange.weather}")
    private String exchange;

    @Value("${rabbitmq.routing-key.aggregated}")
    private String aggregatedRoutingKey;

    @Value("${aggregator.timeout}")
    private long timeoutSeconds;

    private final ConcurrentHashMap<String, AggregationContext> aggregationStore = new ConcurrentHashMap<>();

    @RabbitListener(queues = "${rabbitmq.queue.response}")
    public void aggregateWeatherResponse(WeatherResponse response) {
        log.info("Received response for city: {} with correlationId: {}", response.getCity(), response.getCorrelationId());

        aggregationStore.compute(response.getCorrelationId(), (key, context) -> {
            if (context == null) {
                context = new AggregationContext(response.getCorrelationId(), response.getTotalCities());
            }
            
            context.addResponse(response);

            if (context.isComplete()) {
                log.info("Aggregation complete for correlationId: {}", response.getCorrelationId());
                sendAggregatedReport(context);
                return null; // Remove from store
            }
            return context;
        });
    }

    private void sendAggregatedReport(AggregationContext context) {
        AggregatedWeatherReport report = new AggregatedWeatherReport(context.getCorrelationId(), context.getWeatherData());
        rabbitTemplate.convertAndSend(exchange, aggregatedRoutingKey, report);
    }

    @Scheduled(fixedRate = 10000) // Check every 10 seconds
    public void cleanupExpiredAggregations() {
        LocalDateTime now = LocalDateTime.now();
        aggregationStore.forEach((correlationId, context) -> {
            if (context.getStartTime().plusSeconds(timeoutSeconds).isBefore(now)) {
                log.warn("Aggregation timed out for correlationId: {}", correlationId);
                // Send partial result or error
                sendAggregatedReport(context);
                aggregationStore.remove(correlationId);
            }
        });
    }

    @Data
    private static class AggregationContext {
        private final String correlationId;
        private final int totalCities;
        private final Map<String, Object> weatherData = new HashMap<>();
        private final LocalDateTime startTime = LocalDateTime.now();

        public void addResponse(WeatherResponse response) {
            Map<String, Object> cityData = new HashMap<>();
            if (response.getError() != null) {
                cityData.put("error", response.getError());
            } else {
                cityData.put("temperature", response.getTemperature());
                cityData.put("description", response.getDescription());
            }
            weatherData.put(response.getCity(), cityData);
        }

        public boolean isComplete() {
            return weatherData.size() >= totalCities;
        }
    }
}
