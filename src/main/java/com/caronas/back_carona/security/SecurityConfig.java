package com.caronas.back_carona.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    //Essa parte é para validar segurança do servidor, como estamos usando criptografia, ele estava bloqueando acessos, para nosso fim, liberei todos os acessos
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .csrf().disable() // Desabilita CSRF para desenvolvimento
                .authorizeRequests(authorize -> authorize
                        .anyRequest().permitAll()) // Permite todos os acessos
                .httpBasic().disable(); // Desabilita a autenticação básica HTTP
        return http.build();
    }
}
