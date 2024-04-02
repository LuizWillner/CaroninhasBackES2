package com.caronas.back_carona.service;

import com.caronas.back_carona.repository.UsuarioRepository;
import com.caronas.back_carona.model.Usuario;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import java.time.LocalDate;
import java.time.Period;

@Service
public class UsuarioService {

    @Autowired
    private UsuarioRepository usuarioRepository;
    private BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder(); // Instância do codificador de senha BCrypt, utilizado para criptografar senhas.


    public Usuario salvarUsuario(Usuario usuario) { // Método para salvar um novo usuário, que inclui lógica de validação e criptografia de senha.
        if (Period.between(usuario.getDataNascimento(), LocalDate.now()).getYears() < 18) {
            throw new IllegalArgumentException("Usuário deve ser maior de 18 anos.");
        }

        usuario.setSenha(passwordEncoder.encode(usuario.getSenha())); // Criptografa a senha do usuário antes de salvá-lo no banco de dados.


        return usuarioRepository.save(usuario); // Salva o usuário no banco de dados e retorna o usuário salvo.
    }

    public boolean validarLogin(String cpf, String senha) { // Método para validar o login de um usuário, comparando o CPF e a senha fornecidos com os armazenados.
        // Busca um usuário pelo CPF. Se encontrado, compara a senha fornecida
        // com a senha criptografada armazenada. Retorna verdadeiro se corresponderem, falso caso contrário.
        return usuarioRepository.findByCpf(cpf)
                .map(usuarioEncontrado -> passwordEncoder.matches(senha, usuarioEncontrado.getSenha()))
                .orElse(false); // Se o usuário não for encontrado pelo CPF, retorna falso.
    }
}
