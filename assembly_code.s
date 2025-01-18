section .bss
    num resb 20
    num_len resb 1
    y resq 1
    t3 resq 1
    x resq 1
    t2 resq 1
section .data
msg0: db " loop ", 0xA, 0
msg1: db "finalizou", 0xA, 0
section .text
    global _start

_start:
    mov qword [x], 0
    mov qword [y], 0
    mov qword [x], 40
L0:
    mov rax, [x]
    cmp rax, 0
    jl L1
    mov rax, [x]
    call print_int
    mov rax, 1
    mov rdi, 1
    mov rsi, msg0
    mov rdx, 7
    syscall
    mov rax, [x]
    sub rax, 2
    mov [t3], rax
    mov [x], rax
    jmp L0
L1:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg1
    mov rdx, 10
    syscall
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

                        