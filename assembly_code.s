section .bss
    num resb 20
    num_len resb 1
    t0 resq 1
    y resq 1
    x resq 1
section .text
    global _start

_start:
    mov qword [x], 0
    mov qword [y], 0
    mov qword [x], 40
    mov rax, 40
    mov rbx, 2
    xor rdx, rdx
    idiv rbx
    mov [t0], rax
    mov [x], rax
    mov rax, [x]
    call print_int
    mov rax, 60
    xor rdi, rdi
    syscall

print_int:
    mov rcx, num        ; Ponteiro para o buffer num
    mov rbx, 10         ; Divisor para obter dígitos
    xor rdx, rdx        ; Limpa rdx para a divisão

decimal_loop:
    xor rdx, rdx        ; Limpa rdx
    div rbx             ; Divide rax por 10: quociente em rax, resto em rdx
    add dl, '0'         ; Converte o dígito (resto) em ASCII
    dec rcx             ; Move o ponteiro para trás
    mov [rcx], dl       ; Armazena o dígito no buffer
    test rax, rax       ; Verifica se o quociente é 0
    jnz decimal_loop    ; Continua se ainda há dígitos para processar

    ; Calcula o comprimento do número
    mov rbx, num
    sub rbx, rcx        ; Comprimento = endereço inicial - ponteiro atual
    mov [num_len], bl   ; Armazena o comprimento

    ; Imprime o número
    mov rax, 1          ; syscall: write
    mov rdi, 1          ; stdout
    mov rsi, rcx        ; Ponteiro para o início do número
    mov rdx, rbx        ; Comprimento do número
    syscall
    ret

string_to_int:
    ; rsi = endereço da string de entrada
    xor rax, rax       ; Limpa rax (acumulador do número)
    xor rcx, rcx       ; Limpa rcx (contador)
string_to_int_loop:
    movzx rdx, byte [rsi + rcx]  ; Pega o byte atual da string
    test rdx, rdx               ; Verifica se é o final da string
    jz string_to_int_done       ; Se for zero (fim), sai
    sub rdx, '0'                ; Converte de ASCII para valor numérico
    imul rax, rax, 10           ; Multiplica o acumulador por 10
    add rax, rdx                ; Adiciona o dígito ao acumulador
    inc rcx                     ; Incrementa o contador
    jmp string_to_int_loop      ; Repete o loop
string_to_int_done:
    ret
    
input_wait:
    ; Preparando para ler a entrada
    mov rax, 0          ; Syscall para leitura (0 - read)
    mov rdi, 0          ; stdin (entrada padrão)
    lea rsi, [num]      ; Endereço de armazenamento da entrada
    mov rdx, 20         ; Máximo de 20 bytes
    syscall             ; Executa a leitura

    ; Agora o código aguarda a entrada, o programa só continua quando pressionar "Enter"
    ; O código vai parar aqui até a entrada ser fornecida
    ret

                        