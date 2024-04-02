package com.caronas.back_carona.repository;

import com.caronas.back_carona.model.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface UsuarioRepository extends JpaRepository<Usuario, Long> {

    Optional<Usuario> findByCpf(String cpf); // Encontrar um usuário pelo CPF, o JPA fará a busca utilizando a logica "find" pelo ... que no caso é cpf

    boolean existsByEmail(String email);  // Verificar a existência de um usuário pelo e-mail

}
