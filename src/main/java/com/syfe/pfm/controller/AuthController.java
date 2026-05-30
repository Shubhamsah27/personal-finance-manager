package com.syfe.pfm.controller;

import com.syfe.pfm.dto.LoginRequest;
import com.syfe.pfm.dto.MessageResponse;
import com.syfe.pfm.dto.RegisterRequest;
import com.syfe.pfm.dto.RegisterResponse;
import com.syfe.pfm.model.User;
import com.syfe.pfm.repository.UserRepository;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.context.SecurityContextRepository;
import org.springframework.web.bind.annotation.*;

/**
 * Controller handling user registration and session-based login.
 */
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final SecurityContextRepository securityContextRepository;

    public AuthController(UserRepository userRepository, 
                          PasswordEncoder passwordEncoder, 
                          AuthenticationManager authenticationManager,
                          SecurityContextRepository securityContextRepository) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.authenticationManager = authenticationManager;
        this.securityContextRepository = securityContextRepository;
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@Valid @RequestBody RegisterRequest request) {
        if (userRepository.existsByUsername(request.getUsername())) {
            // Return 409 Conflict
            return ResponseEntity.status(HttpStatus.CONFLICT)
                    .body(new MessageResponse("Username/Email already exists"));
        }

        User user = new User(
                request.getUsername(),
                passwordEncoder.encode(request.getPassword()),
                request.getFullName(),
                request.getPhoneNumber()
        );

        User savedUser = userRepository.save(user);

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new RegisterResponse("User registered successfully", savedUser.getId()));
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequest request, 
                                   HttpServletRequest httpRequest, 
                                   HttpServletResponse httpResponse) {
        // Authenticate credentials
        UsernamePasswordAuthenticationToken authToken = 
                new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword());
        
        Authentication authentication = authenticationManager.authenticate(authToken);
        
        // Save security context to context holder
        SecurityContext context = SecurityContextHolder.createEmptyContext();
        context.setAuthentication(authentication);
        SecurityContextHolder.setContext(context);
        
        // Save to Session context repository to persist cookie across requests
        securityContextRepository.saveContext(context, httpRequest, httpResponse);

        return ResponseEntity.ok(new MessageResponse("Login successful"));
    }
}
