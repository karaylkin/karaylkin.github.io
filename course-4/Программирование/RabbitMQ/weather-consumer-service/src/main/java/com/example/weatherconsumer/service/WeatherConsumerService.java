package com.example.weatherconsumer.service;

import com.example.weatherconsumer.dto.OpenWeatherMapResponse;
import com.example.weatherconsumer.dto.WeatherMessage;
import com.example.weatherconsumer.dto.WeatherResponse;
import com.rabbitmq.client.Channel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.AmqpHeaders;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Service;

import java.io.IOException;

@Service
@RequiredArgsConstructor
@Slf4j
public class WeatherConsumerService {

    private final WeatherApiClient weatherApiClient;
    private final RabbitTemplate rabbitTemplate;

    @Value("${rabbitmq.exchange.weather}")
    private String exchange;

    @Value("${rabbitmq.routing-key.response}")
    private String responseRoutingKey;

    @Value("${weather.delay}")
    private long delay;

    @RabbitListener(queues = "${rabbitmq.queue.request}", ackMode = "MANUAL")
    public void consumeWeatherRequest(WeatherMessage message, Channel channel, @Header(AmqpHeaders.DELIVERY_TAG) long tag) {
        log.info("Received message: {}", message);
        try {
            // Simulate delay
            Thread.sleep(delay);

            OpenWeatherMapResponse apiResponse = weatherApiClient.getWeather(message.getCity());
            
            WeatherResponse response = new WeatherResponse();
            response.setCity(message.getCity());
            response.setCorrelationId(message.getCorrelationId());
            response.setTotalCities(message.getTotalCities());
            
            if (apiResponse != null) {
                if (apiResponse.getMain() != null) {
                    response.setTemperature(apiResponse.getMain().getTemp());
                }
                if (apiResponse.getWeather() != null && !apiResponse.getWeather().isEmpty()) {
                    response.setDescription(apiResponse.getWeather().get(0).getDescription());
                }
            }

            rabbitTemplate.convertAndSend(exchange, responseRoutingKey, response);
            channel.basicAck(tag, false);
            log.info("Processed message for city: {}", message.getCity());

        } catch (Exception e) {
            log.error("Error processing message for city: {}", message.getCity(), e);
            WeatherResponse errorResponse = new WeatherResponse();
            errorResponse.setCity(message.getCity());
            errorResponse.setCorrelationId(message.getCorrelationId());
            errorResponse.setTotalCities(message.getTotalCities());
            errorResponse.setError(e.getMessage());
            
            rabbitTemplate.convertAndSend(exchange, responseRoutingKey, errorResponse);
            
            try {
                // Ack even on error to avoid infinite loop, or use dead letter queue in production
                channel.basicAck(tag, false); 
            } catch (IOException ex) {
                log.error("Failed to ack message", ex);
            }
        }
    }
}
