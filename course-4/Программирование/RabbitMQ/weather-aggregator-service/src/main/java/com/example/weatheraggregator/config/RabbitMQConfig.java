package com.example.weatheraggregator.config;

import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {

    @Value("${rabbitmq.queue.aggregated}")
    private String aggregatedQueue;

    @Value("${rabbitmq.queue.response}")
    private String responseQueue;

    @Value("${rabbitmq.exchange.weather}")
    private String exchange;

    @Value("${rabbitmq.routing-key.aggregated}")
    private String aggregatedRoutingKey;

    @Bean
    public Queue aggregatedQueue() {
        return new Queue(aggregatedQueue);
    }

    @Bean
    public Queue responseQueue() {
        return new Queue(responseQueue);
    }

    @Bean
    public TopicExchange exchange() {
        return new TopicExchange(exchange);
    }

    @Bean
    public Binding aggregatedBinding() {
        return BindingBuilder
                .bind(aggregatedQueue())
                .to(exchange())
                .with(aggregatedRoutingKey);
    }

    @Bean
    public MessageConverter converter() {
        return new Jackson2JsonMessageConverter();
    }

    @Bean
    public AmqpTemplate amqpTemplate(ConnectionFactory connectionFactory) {
        RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory);
        rabbitTemplate.setMessageConverter(converter());
        return rabbitTemplate;
    }
}
