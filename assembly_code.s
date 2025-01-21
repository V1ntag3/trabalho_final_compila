section .bss
    num resb 20
    num_len resb 1
    b resq 1
    a resq 1
    t4 resq 1
    t3 resq 1
    t2 resq 1
section .data
msg0: db "Valor de a:", 0xA, 0
msg1: db ".", 0xA, 0
msg2: db "igual a 10", 0xA, 0
section .text
    global _start

_start:
    mov qword [a], 0
    mov qword [b], 0
    mov qword [a], 50
L0:
    mov rax, [a]
    cmp rax, 0
    jl L1
    mov rax, 1
    mov rdi, 1
    mov rsi, msg0
    mov rdx, 12
    syscall
    mov rax, [a]
    call print_int
    mov rax, 1
    mov rdi, 1
    mov rsi, msg1
    mov rdx, 2
    syscall
    mov rax, [a]
    sub rax, 1
    mov [t3], rax
    mov [a], rax
    mov rax, [a]
    cmp rax, 10
    je L5
    jmp L6
L5:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg2
    mov rdx, 11
    syscall
L6:
    jmp L0
L1:
    mov rax, 60
    xor rdi, rdi
    syscall

print_int:
    mov rcx, num          ; Ponteiro para o buffer num
    add rcx, 20           ; Posiciona no final do buffer
    mov rbx, 10           ; Divisor para obter dígitos
    xor rdx, rdx          ; Limpa rdx

decimal_loop:
    xor rdx, rdx          ; Limpa rdx novamente
    div rbx               ; Divide rax por 10
    add dl, '0'           ; Converte dígito para ASCII
    dec rcx               ; Move o ponteiro para trás
    mov [rcx], dl         ; Armazena o dígito no buffer
    test rax, rax         ; Verifica se o quociente é 0
    jnz decimal_loop      ; Continua até terminar

    mov rbx, num          ; Calcula o comprimento
    add rbx, 20
    sub rbx, rcx          ; Comprimento = endereço final - ponteiro atual
    mov [num_len], bl     ; Armazena o comprimento

    mov rax, 1            ; syscall: write
    mov rdi, 1            ; stdout
    mov rsi, rcx          ; Ponteiro para o início do número
    mov rdx, rbx          ; Comprimento do número
    syscall

    ret                   ; Retorna ao chamador                    
                        