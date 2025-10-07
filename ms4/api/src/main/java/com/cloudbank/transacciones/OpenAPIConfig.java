package com.cloudbank.transacciones;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.servers.Server;
import io.swagger.v3.oas.models.tags.Tag;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class OpenAPIConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("MS4 - API de Transacciones Bancarias")
                        .version("1.0.0")
                        .description("Microservicio para gestión de transacciones bancarias con MongoDB")
                        .contact(new Contact()
                                .name("Cloud Bank Team")))
                .servers(List.of(
                        new Server().url("http://localhost:8004").description("Servidor local")
                ))
                .tags(List.of(
                        new Tag().name("Health").description("Endpoints de salud del servicio"),
                        new Tag().name("Transacciones").description("Operaciones de transacciones bancarias")
                ));
    }
}
