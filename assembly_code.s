section .bss
    num resb 20
    num_len resb 1
    t8 resq 1
    t4 resq 1
    b resq 1
    a resq 1
    t0 resq 1
section .data
msg0: db "Maior: ", 0xA, 0
msg1: db " ", 0xA, 0
msg2: db "a é igual a 50", 0xA, 0
msg3: db "a nao é igual a 50", 0xA, 0
msg4: db "Iguais!", 0xA, 0
section .text
    global _start

_start:
    mov qword [a], 0
    mov qword [b], 0
    mov qword [a], 50
    mov qword [b], 30
    mov rax, [a]
    cmp rax, [b]
    jg L1
    jmp L3
L1:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg0
    mov rdx, 8
    syscall
    mov rax, [a]
    call print_int
    mov rax, 1
    mov rdi, 1
    mov rsi, msg1
    mov rdx, 2
    syscall
    mov rax, [a]
    cmp rax, 50
    je L5
    jmp L7
L5:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg2
    mov rdx, 15
    syscall
    jmp L6
L7:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg3
    mov rdx, 19
    syscall
L6:
    jmp L2
L3:
    mov rax, [a]
    cmp rax, [b]
    jl L9
    jmp L11
L9:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg0
    mov rdx, 8
    syscall
    mov rax, [b]
    call print_int
    jmp L10
L11:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg4
    mov rdx, 8
    syscall
L10:
L2:
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
                        