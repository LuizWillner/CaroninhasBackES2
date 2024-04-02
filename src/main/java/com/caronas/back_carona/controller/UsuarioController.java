package com.caronas.back_carona.controller;

import com.caronas.back_carona.model.Usuario;
import com.caronas.back_carona.service.UsuarioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController // Definindo a classe controladora que gerencia os endpoints relacionados a usuários

@RequestMapping("/usuarios") // Definindo o caminho base para todos os endpoints de "/usuarios"

public class UsuarioController {

    @Autowired // Injeção de dependência automática do serviço de usuário, dessa forma conseguimos utilizar o que está no service
    private UsuarioService usuarioService;

    @PostMapping("/cadastro") // Definindo o endpoint para cadastro de usuário em"/usuarios/cadastro"
    public ResponseEntity<?> cadastrarUsuario(@RequestBody Usuario usuario) {
        try {
            Usuario novoUsuario = usuarioService.salvarUsuario(usuario); // Chamada ao serviço para salvar o novo usuário no banco de dados
            novoUsuario.setSenha(null); // Removendo a senha do objeto de resposta para segurança
            return ResponseEntity.ok(novoUsuario); // Retorna o usuário salvo com status 200 (OK), com a senha removida do corpo
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(e.getMessage()); //Retorna um erro se estiver faltando algo
        }
    }

    @PostMapping("/login") // Definindo o endpoint para login "/usuarios/login"
    public ResponseEntity<?> login(@RequestParam String cpf, @RequestParam String senha) {

        boolean valido = usuarioService.validarLogin(cpf, senha); // Verifica as credenciais fornecidas com as armazenadas no banco
        if (valido) {
            return ResponseEntity.ok("Login bem-sucedido."); // Se as credenciais estiverem corretas, retorna uma mensagem de sucesso
        } else {
            return ResponseEntity.status(401).body("CPF ou senha inválidos."); // Se as credenciais estiverem incorretas, retorna status 401 (Unauthorized)
        }
    }
}
