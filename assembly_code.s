section .bss
    num resb 20
    num_len resb 1
    t4 resq 1
    b resq 1
    a resq 1
    t0 resq 1
section .data
msg0: db "Maior: ", 0xA, 0
msg1: db "Iguais!", 0xA, 0
section .text
    global _start

_start:
    mov qword [a], 0
    mov qword [b], 0
    mov qword [a], 60
    mov qword [b], 40
    mov rax, [a]
    cmp rax, [b]
    jl L1
    jmp L2
L1:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg0
    mov rdx, 8
    syscall
    mov rax, [a]
    call print_int
    jmp L2
L3:
    mov rax, [a]
    cmp rax, [b]
    jg L5
    jmp L6
L5:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg0
    mov rdx, 8
    syscall
    mov rax, [b]
    call print_int
    jmp L6
L7:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg1
    mov rdx, 8
    syscall
L6:
L2:
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

                        